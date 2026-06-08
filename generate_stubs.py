"""
Generate .pyi stub files for synchronicity-wrapped route modules.

Instead of using synchronicity's Protocol-based stub pattern (which doesn't
resolve well in PyCharm/JetBrains IDEs), this generates simple method stubs
that directly declare sync method signatures.
"""

import ast
from pathlib import Path

ROUTES_DIR = Path("src/py_librenms/routes")


def generate_stub_from_async_source(async_source: str) -> str:
    """Parse an async implementation module and produce a .pyi stub with sync signatures."""
    tree = ast.parse(async_source)

    lines: list[str] = []
    imports_needed: set[str] = set()

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            lines.append(generate_class_stub(node, imports_needed))

    # Collect import statements from source (for model return types)
    import_lines: list[str] = ["from __future__ import annotations", ""]
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # Skip typing imports and __future__
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("__future__"):
                    continue
                if node.module and ("_synchronicity" in node.module):
                    continue
                if node.module and node.module.endswith("._base"):
                    continue
            # Filter out private utilities from _types imports (not needed in stubs)
            if isinstance(node, ast.ImportFrom) and node.module and "_types" in node.module:
                node.names = [alias for alias in node.names if not alias.name.startswith("_")]
                if not node.names:
                    continue
            import_lines.append(ast.unparse(node))

    import_lines.append("")
    import_lines.append("")

    return "\n".join(import_lines) + "\n".join(lines) + "\n"


def generate_class_stub(class_node: ast.ClassDef, imports_needed: set[str]) -> str:
    """Generate stub for a single class."""
    lines: list[str] = []

    # Class docstring
    docstring = ast.get_docstring(class_node)
    doc_part = ""
    if docstring:
        doc_part = f'\n    """{docstring}"""'

    lines.append(f"class {class_node.name}:{doc_part}")

    # Check if __init__ assigns self._client and add attribute annotation
    for node in ast.iter_child_nodes(class_node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "__init__":
            for arg in node.args.args:
                if arg.arg == "client" and arg.annotation:
                    ann = ast.unparse(arg.annotation)
                    lines.append(f"    _client: {ann}")
                    break
            break

    for node in ast.iter_child_nodes(class_node):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            stub = generate_method_stub(node, imports_needed)
            lines.append(stub)

    if len(lines) == 1:
        lines.append("    ...")

    return "\n".join(lines)


def generate_method_stub(
    func_node: ast.FunctionDef | ast.AsyncFunctionDef, imports_needed: set[str]
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
    signature = f"    def {func_node.name}({params_str}){return_ann}: ..."

    # Add docstring as a comment for IDE hover
    docstring = ast.get_docstring(func_node)
    if docstring:
        # Use a proper docstring in the stub
        doc_lines = docstring.strip().split("\n")
        if len(doc_lines) == 1:
            signature = f'    def {func_node.name}({params_str}){return_ann}:\n        """{doc_lines[0]}"""\n        ...'
        else:
            doc_body = "\n        ".join(doc_lines)
            signature = f'    def {func_node.name}({params_str}){return_ann}:\n        """{doc_body}"""\n        ...'

    return signature


def main():
    # Find all public route files (the non-underscore ones)
    route_files = sorted(
        f for f in ROUTES_DIR.glob("*.py") if not f.name.startswith("_")
    )

    # Remove old _*.pyi stubs
    for old_stub in ROUTES_DIR.glob("_*.pyi"):
        if old_stub.name != "__init__.pyi":
            old_stub.unlink()

    # Collect route metadata for __init__ generation
    route_entries: list[tuple[str, str, str]] = []  # (module, async_class, sync_class)

    for route_file in route_files:
        # alerts.py -> alerts.pyi (same name, includes both async class + sync class stub)
        stub_file = ROUTES_DIR / f"{route_file.stem}.pyi"

        print(f"Generating {stub_file.name} from {route_file.name}...")

        source = route_file.read_text(encoding="utf-8")
        stub_content = generate_stub_from_async_source(source)

        # Find the sync class name from the source (e.g. AlertsSync)
        import re

        match = re.search(
            r"^(\w+Sync)\s*=\s*synchronizer\.wrap\(", source, re.MULTILINE
        )
        if match:
            sync_name = match.group(1)
            # Add a sync class stub that mirrors the async class but with plain def
            stub_content += f"\nclass {sync_name}:\n"
            # Re-parse to get the class body for sync stub
            tree = ast.parse(source)
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.ClassDef):
                    stub_content += f'    """{node.name} (synchronous)."""\n'
                    # Add _client attribute annotation
                    for method in ast.iter_child_nodes(node):
                        if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) and method.name == "__init__":
                            for arg in method.args.args:
                                if arg.arg == "client" and arg.annotation:
                                    ann = ast.unparse(arg.annotation)
                                    stub_content += f"    _client: {ann}\n"
                                    break
                            break
                    for method in ast.iter_child_nodes(node):
                        if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            stub_content += generate_method_stub(method, set()) + "\n"
                    # Record for __init__ generation
                    route_entries.append((route_file.stem, node.name, sync_name))
                    break

        stub_file.write_text(stub_content, encoding="utf-8")

    # Generate __init__.py and __init__.pyi
    _generate_routes_init(route_entries)

    print(f"\nDone! Generated {len(route_files)} stub files + __init__.py + __init__.pyi.")


def _generate_routes_init(entries: list[tuple[str, str, str]]) -> None:
    """Generate routes/__init__.py and __init__.pyi from route metadata.

    Each entry is (module_name, async_class_name, sync_class_name).
    """
    import_lines: list[str] = []
    all_names: list[str] = []

    for module, async_class, sync_class in entries:
        async_alias = f"{async_class}Async" if not async_class.endswith("Async") else async_class
        # Determine the public alias: class name + "Async"
        # e.g. Alerts -> AlertsAsync, Arp -> ArpAsync
        async_alias = f"{async_class}Async"
        import_lines.append(f"from .{module} import {async_class} as {async_alias}")
        import_lines.append(f"from .{module} import {sync_class}")
        all_names.append(f'    "{async_alias}",')
        all_names.append(f'    "{sync_class}",')

    content = "\n".join(import_lines)
    content += "\n\n__all__ = [\n"
    content += "\n".join(all_names)
    content += "\n]\n"

    # Write __init__.py
    init_py = ROUTES_DIR / "__init__.py"
    init_py.write_text(content, encoding="utf-8")
    print(f"Generated __init__.py")

    # Write __init__.pyi (same content but with `as` aliases on sync imports for clarity)
    pyi_import_lines: list[str] = []
    for module, async_class, sync_class in entries:
        async_alias = f"{async_class}Async"
        pyi_import_lines.append(f"from .{module} import {async_class} as {async_alias}")
        pyi_import_lines.append(f"from .{module} import {sync_class} as {sync_class}")

    pyi_content = "\n".join(pyi_import_lines)
    pyi_content += "\n\n__all__ = [\n"
    pyi_content += "\n".join(all_names)
    pyi_content += "\n]\n"

    init_pyi = ROUTES_DIR / "__init__.pyi"
    init_pyi.write_text(pyi_content, encoding="utf-8")
    print(f"Generated __init__.pyi")


if __name__ == "__main__":
    main()
