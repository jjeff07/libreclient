"""
Generate .pyi stub files for synchronicity-wrapped route modules.

Instead of using synchronicity's Protocol-based stub pattern (which doesn't
resolve well in PyCharm/JetBrains IDEs), this generates simple method stubs
that directly declare sync method signatures.
"""

import ast
import re
from pathlib import Path

ROUTES_DIR = (
    Path(__file__).resolve().parent.parent / "src" / "libreclient" / "routes"
)


def collect_imports_from_async(source: str) -> list[str]:
    """Collect import lines needed for the stub from the async source module."""
    tree = ast.parse(source)
    import_lines: list[str] = ["from __future__ import annotations", ""]
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if (
                isinstance(node, ast.ImportFrom)
                and node.module
                and (
                    node.module.startswith("__future__")
                    or "_synchronicity" in node.module
                    or node.module.endswith("._base")
                )
            ):
                continue
            # Filter out private utilities from _types imports (not needed in stubs)
            if (
                isinstance(node, ast.ImportFrom)
                and node.module
                and "_types" in node.module
            ):
                node.names = [
                    alias
                    for alias in node.names
                    if not alias.name.startswith("_")
                ]
                if not node.names:
                    continue
            import_lines.append(ast.unparse(node))
    import_lines.append("")
    import_lines.append("")
    return import_lines


def collect_type_aliases(source: str) -> list[str]:
    """Collect module-level type alias assignments from the async source module.

    These are assignments like ``DeviceListType = typing.Literal[...]`` that need
    to be reproduced in the stub so that type references resolve correctly.
    """
    tree = ast.parse(source)
    alias_lines: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id[0].isupper()
        ) or (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.value
        ):
            alias_lines.append(ast.unparse(node))
    if alias_lines:
        alias_lines.append("")
        alias_lines.append("")
    return alias_lines


def generate_method_stub(
    func_node: ast.FunctionDef | ast.AsyncFunctionDef,
    imports_needed: set[str],
    source_filename: str = "",
) -> str:
    """Generate a sync method stub from an async function definition."""
    # Get the signature
    args = func_node.args
    params: list[str] = []

    # Process all arguments
    all_args = args.args
    defaults = args.defaults
    # defaults align to the END of positional args
    num_no_default = len(all_args) - len(defaults)

    for i, arg in enumerate(all_args):
        param_str = arg.arg
        # Add annotation if present
        if arg.annotation:
            ann = ast.unparse(arg.annotation)
            if "Optional" in ann or "|" in ann:
                imports_needed.add("typing")
            param_str += f": {ann}"

        # Add default if present
        default_idx = i - num_no_default
        if default_idx >= 0 and default_idx < len(defaults):
            default = ast.unparse(defaults[default_idx])
            param_str += f" = {default}"

        params.append(param_str)

    # Handle **kwargs
    if args.kwarg:
        kw_str = f"**{args.kwarg.arg}"
        if args.kwarg.annotation:
            kw_str += f": {ast.unparse(args.kwarg.annotation)}"
        params.append(kw_str)

    # Handle *args
    if args.vararg:
        va_str = f"*{args.vararg.arg}"
        if args.vararg.annotation:
            va_str += f": {ast.unparse(args.vararg.annotation)}"
        # Insert before kwargs
        if args.kwarg:
            params.insert(-1, va_str)
        else:
            params.append(va_str)

    # Return annotation
    return_ann = ""
    if func_node.returns:
        return_ann = f" -> {ast.unparse(func_node.returns)}"

    params_str = ", ".join(params)

    # Build the Better Highlights link comment for PyCharm navigation
    link_comment = ""
    if source_filename and func_node.name != "__init__":
        link_comment = f"  #  [[{source_filename}#{func_node.name}]]"

    signature = f"    def {func_node.name}({params_str}){return_ann}: ...{link_comment}"

    # Add docstring as a comment for IDE hover
    docstring = ast.get_docstring(func_node)
    if docstring:
        # Use a proper docstring in the stub
        doc_lines = docstring.strip().split("\n")
        if len(doc_lines) == 1:
            signature = f'    def {func_node.name}({params_str}){return_ann}:\n        """{doc_lines[0]}"""\n        ...{link_comment}'
        else:
            doc_body = "\n        ".join(doc_lines)
            signature = f'    def {func_node.name}({params_str}){return_ann}:\n        """{doc_body}"""\n        ...{link_comment}'

    return signature


def main():
    # Find all *_sync.py files (these contain the synchronizer.wrap() calls)
    sync_files = sorted(ROUTES_DIR.glob("*_sync.py"))

    # Collect route metadata for __init__ generation
    route_entries: list[
        tuple[str, str, str]
    ] = []  # (async_module, async_class, sync_class)

    for sync_file in sync_files:
        sync_source = sync_file.read_text(encoding="utf-8")

        # Find the sync class name (e.g. AlertsSync)
        match = re.search(
            r"^(\w+Sync)\s*=\s*synchronizer\.wrap\(", sync_source, re.MULTILINE
        )
        if not match:
            continue

        sync_name = match.group(1)

        # Determine the async module name from the import in the sync file
        # e.g. "from .alerts import Alerts" -> module="alerts", class="Alerts"
        import_match = re.search(
            r"from \.([a-zA-Z]\w*) import (\w+)", sync_source
        )
        if not import_match:
            continue

        async_module = import_match.group(1)
        async_class = import_match.group(2)

        # Read the async source to get method signatures and imports
        async_file = ROUTES_DIR / f"{async_module}.py"
        if not async_file.exists():
            print(f"  WARNING: {async_file.name} not found, skipping.")
            continue

        async_source = async_file.read_text(encoding="utf-8")

        # Generate stub file: alerts_sync.pyi
        stub_file = ROUTES_DIR / f"{sync_file.stem}.pyi"
        print(f"Generating {stub_file.name} from {async_file.name}...")

        # Build module docstring for the stub
        async_rel_path = f"src/libreclient/routes/{async_file.name}"
        module_doc = (
            f'"""\n'
            f"Auto-generated stub for {sync_file.stem} (synchronous API).\n"
            f"\n"
            f"This file provides type information for IDE support and static analysis.\n"
            f"The actual implementation is generated at runtime via synchronicity from:\n"
            f"    {async_rel_path}\n"
            f'"""\n\n'
        )

        # Collect imports from the async module
        import_lines = collect_imports_from_async(async_source)
        stub_content = module_doc + "\n".join(import_lines)

        # Collect module-level type aliases (e.g. Literal types)
        type_aliases = collect_type_aliases(async_source)
        if type_aliases:
            stub_content += "\n".join(type_aliases)

        # Generate sync class stub that mirrors the async class but with plain def
        stub_content += f"class {sync_name}:\n"
        tree = ast.parse(async_source)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef) and node.name == async_class:
                stub_content += f'    """{async_class} (synchronous)."""\n'
                # Add _client attribute annotation
                for method in ast.iter_child_nodes(node):
                    if (
                        isinstance(
                            method, (ast.FunctionDef, ast.AsyncFunctionDef)
                        )
                        and method.name == "__init__"
                    ):
                        for arg in method.args.args:
                            if arg.arg == "client" and arg.annotation:
                                ann = ast.unparse(arg.annotation)
                                stub_content += f"    _client: {ann}\n"
                                break
                        break
                for method in ast.iter_child_nodes(node):
                    if isinstance(
                        method, (ast.FunctionDef, ast.AsyncFunctionDef)
                    ):
                        stub_content += (
                            generate_method_stub(
                                method, set(), async_file.name
                            )
                            + "\n"
                        )
                # Record for __init__ generation
                route_entries.append((async_module, async_class, sync_name))
                break

        stub_file.write_text(stub_content, encoding="utf-8")

    # Generate __init__.py and __init__.pyi
    _generate_routes_init(route_entries)

    print(
        f"\nDone! Generated {len(sync_files)} stub files + __init__.py + __init__.pyi."
    )


def _generate_routes_init(entries: list[tuple[str, str, str]]) -> None:
    """Generate routes/__init__.py and __init__.pyi from route metadata.

    Each entry is (async_module, async_class_name, sync_class_name).
    """
    import_lines: list[str] = []
    all_names: list[str] = []

    for async_module, async_class, sync_class in entries:
        sync_module = f"{async_module}_sync"
        async_alias = f"{async_class}Async"
        import_lines.append(
            f"from .{async_module} import {async_class} as {async_alias}"
        )
        import_lines.append(f"from .{sync_module} import {sync_class}")
        all_names.append(f'    "{async_alias}",')
        all_names.append(f'    "{sync_class}",')

    content = "\n".join(import_lines)
    content += "\n\n__all__ = [\n"
    content += "\n".join(all_names)
    content += "\n]\n"

    # Write __init__.py
    init_py = ROUTES_DIR / "__init__.py"
    init_py.write_text(content, encoding="utf-8")
    print("Generated __init__.py")

    # Write __init__.pyi (same content but with explicit `as` aliases for type checkers)
    pyi_import_lines: list[str] = []
    for async_module, async_class, sync_class in entries:
        sync_module = f"{async_module}_sync"
        async_alias = f"{async_class}Async"
        pyi_import_lines.append(
            f"from .{async_module} import {async_class} as {async_alias}"
        )
        pyi_import_lines.append(
            f"from .{sync_module} import {sync_class} as {sync_class}"
        )

    pyi_content = "\n".join(pyi_import_lines)
    pyi_content += "\n\n__all__ = [\n"
    pyi_content += "\n".join(all_names)
    pyi_content += "\n]\n"

    init_pyi = ROUTES_DIR / "__init__.pyi"
    init_pyi.write_text(pyi_content, encoding="utf-8")
    print("Generated __init__.pyi")


if __name__ == "__main__":
    main()
