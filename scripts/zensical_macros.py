"""Zensical macros plugin — exposes project markdown files as template variables.

Variables available in docs templates:
    {{ README_MAIN }}           - README without Contributing/Development sections
    {{ README_CONTRIBUTING }}   - The Contributing section from README
    {{ README_DEVELOPMENT }}    - The Development section from README
    {{ CONTRIBUTING }}          - Full CONTRIBUTING.md
    {{ COMMIT_TYPES }}          - Full COMMIT_TYPES.md
"""

import re
from pathlib import Path


def _extract_section(content: str, heading: str) -> str:
    """Extract a ## section from markdown, including its content up to the next ## heading or EOF."""
    pattern = (
        rf"(^---\s*\n\s*\n)?^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
    )
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    # Return content without the leading --- separator if present
    section = match.group(0).lstrip("-").lstrip("\n")
    return (
        f"## {heading}\n" + section.split("\n", 1)[-1]
        if section.startswith(f"## {heading}")
        else f"## {heading}\n{section}"
    )


def _remove_sections(content: str, headings: list[str]) -> str:
    """Remove ## sections (and any preceding --- separator) from markdown."""
    for heading in headings:
        pattern = (
            rf"(^---\s*\n\s*\n)?^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
        )
        content = re.sub(pattern, "", content, flags=re.MULTILINE | re.DOTALL)
    return content.rstrip("\n") + "\n"


def define_env(env):
    md_dir = Path(__file__).parent.parent
    readme_path = md_dir / "README.md"
    contributing_path = md_dir / "CONTRIBUTING.md"
    commit_path = md_dir / "COMMIT_TYPES.md"
    security_path = md_dir / "SECURITY.md"

    with open(readme_path, encoding="utf8") as f:
        readme_content = f.read()

    with open(contributing_path, encoding="utf8") as f:
        env.variables["CONTRIBUTING"] = f.read()

    with open(commit_path, encoding="utf8") as f:
        env.variables["COMMIT_TYPES"] = f.read()

    with open(security_path, encoding="utf8") as f:
        env.variables["SECURITY"] = f.read()

    # Parsed sections from README
    env.variables["README_CONTRIBUTING"] = _extract_section(
        readme_content, "Contributing"
    )
    env.variables["README_DEVELOPMENT"] = _extract_section(
        readme_content, "Development"
    )

    # README without Contributing and Development sections
    env.variables["README_MAIN"] = _remove_sections(
        readme_content, ["Contributing", "Development"]
    )
