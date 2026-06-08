"""Check for upstream LibreNMS API doc changes since our pinned tag.

Usage:
    python check_upstream.py              # Show latest tag vs pinned tag
    python check_upstream.py --diff       # Show file-level diff of API docs
    python check_upstream.py --full       # Show full content diff of changed files
    python check_upstream.py --bump       # Update pinned_tag to latest
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

TRACKING_FILE = Path(__file__).parent / "upstream_tracking.toml"


def load_config() -> dict:
    """Load upstream tracking config."""
    with open(TRACKING_FILE, "rb") as f:
        return tomllib.load(f)["upstream"]


def github_api(url: str) -> dict | list:
    """Make a GitHub API request (unauthenticated)."""
    req = Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urlopen(req) as resp:
        return json.loads(resp.read())


def get_latest_tag(repo: str) -> str:
    """Get the latest release tag from a GitHub repo."""
    data = github_api(f"https://api.github.com/repos/{repo}/releases/latest")
    return data["tag_name"]


def get_all_tags(repo: str, per_page: int = 10) -> list[str]:
    """Get recent tags from a GitHub repo."""
    data = github_api(
        f"https://api.github.com/repos/{repo}/tags?per_page={per_page}"
    )
    return [t["name"] for t in data]


def list_docs_at_tag(repo: str, tag: str, docs_path: str) -> dict[str, str]:
    """List API doc files at a given tag. Returns {filename: download_url}."""
    url = f"https://api.github.com/repos/{repo}/contents/{docs_path}?ref={tag}"
    data = github_api(url)
    return {
        item["name"]: item["download_url"]
        for item in data
        if item["type"] == "file"
    }


def get_file_content(url: str) -> str:
    """Download raw file content from a URL."""
    req = Request(url)
    with urlopen(req) as resp:
        return resp.read().decode("utf-8")


def compare_tags(
    repo: str, base_tag: str, head_tag: str, docs_path: str
) -> dict:
    """Compare API doc files between two tags.

    Returns dict with keys: added, removed, modified, unchanged.
    """
    base_files = list_docs_at_tag(repo, base_tag, docs_path)
    head_files = list_docs_at_tag(repo, head_tag, docs_path)

    base_names = set(base_files.keys())
    head_names = set(head_files.keys())

    added = sorted(head_names - base_names)
    removed = sorted(base_names - head_names)
    common = sorted(base_names & head_names)

    # For common files, use the GitHub compare API to detect changes
    # We'll use a simpler approach: compare via commits
    compare_url = (
        f"https://api.github.com/repos/{repo}/compare/{base_tag}...{head_tag}"
    )
    try:
        compare_data = github_api(compare_url)
        changed_files = {f["filename"] for f in compare_data.get("files", [])}
        modified = sorted(
            name for name in common if f"{docs_path}/{name}" in changed_files
        )
        unchanged = sorted(
            name
            for name in common
            if f"{docs_path}/{name}" not in changed_files
        )
    except HTTPError:
        # Fallback: mark all common as "unknown"
        modified = []
        unchanged = common
        print(
            "  (Could not fetch compare data; showing file lists only)",
            file=sys.stderr,
        )

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
        "base_files": base_files,
        "head_files": head_files,
    }


def bump_tag(new_tag: str) -> None:
    """Update the pinned_tag in upstream_tracking.toml."""
    content = TRACKING_FILE.read_text()
    import re

    updated = re.sub(
        r'pinned_tag\s*=\s*"[^"]*"',
        f'pinned_tag = "{new_tag}"',
        content,
    )
    TRACKING_FILE.write_text(updated)
    print(f"Updated pinned_tag: {new_tag}")


def main() -> None:  # noqa: S3776
    parser = argparse.ArgumentParser(
        description="Check upstream LibreNMS API doc changes."
    )
    parser.add_argument(
        "--diff", action="store_true", help="Show file-level changes"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Show full content diff of modified files",
    )
    parser.add_argument(
        "--bump", action="store_true", help="Bump pinned_tag to latest"
    )
    parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help="Compare against this tag (default: latest)",
    )
    args = parser.parse_args()

    config = load_config()
    repo = config["repo"]
    pinned = config["pinned_tag"]
    docs_path = config["docs_path"]

    print(f"Repo:       https://github.com/{repo}")
    print(f"Pinned tag: {pinned}")
    print(f"Docs path:  {docs_path}/")
    print()

    # Get latest tag
    latest = args.tag or get_latest_tag(repo)
    print(f"Latest tag: {latest}")

    if pinned == latest:
        print("\n✓ Already up to date — pinned tag matches latest release.")
        return

    print(f"\n⚠ Upstream has moved: {pinned} → {latest}")
    print(f"  Compare: https://github.com/{repo}/compare/{pinned}...{latest}")

    if args.bump:
        bump_tag(latest)
        return

    if args.diff or args.full:
        print(f"\nComparing API docs: {pinned} → {latest} ...")
        result = compare_tags(repo, pinned, latest, docs_path)

        if result["added"]:
            print(f"\n  New files ({len(result['added'])}):")
            for f in result["added"]:
                print(f"    + {f}")

        if result["removed"]:
            print(f"\n  Removed files ({len(result['removed'])}):")
            for f in result["removed"]:
                print(f"    - {f}")

        if result["modified"]:
            print(f"\n  Modified files ({len(result['modified'])}):")
            for f in result["modified"]:
                print(f"    ~ {f}")
        else:
            print("\n  No modified API doc files detected.")

        if result["unchanged"]:
            print(f"\n  Unchanged files: {len(result['unchanged'])}")

        if args.full and result["modified"]:
            print("\n" + "=" * 72)
            print("FULL DIFFS OF MODIFIED FILES")
            print("=" * 72)
            for name in result["modified"]:
                print(f"\n{'─' * 72}")
                print(f"FILE: {name}")
                print(f"{'─' * 72}")
                base_url = result["base_files"][name]
                head_url = result["head_files"][name]
                base_content = get_file_content(base_url)
                head_content = get_file_content(head_url)

                if base_content == head_content:
                    print(
                        "  (content identical — change may be in metadata only)"
                    )
                    continue

                # Simple line diff
                import difflib

                diff = difflib.unified_diff(
                    base_content.splitlines(keepends=True),
                    head_content.splitlines(keepends=True),
                    fromfile=f"a/{docs_path}/{name} ({pinned})",
                    tofile=f"b/{docs_path}/{name} ({latest})",
                )
                sys.stdout.writelines(diff)
    else:
        print(
            "\n  Run with --diff to see changed files, or --full for content diffs."
        )
        print("  Run with --bump to update pinned_tag to latest.")


if __name__ == "__main__":
    main()
