---
title: Documentation
description: How the documentation site is built and maintained
icon: lucide/book-text
render_macros: false
---

# Documentation

This project's documentation site is built with [Zensical](https://zensical.org/) and hosted on
GitHub Pages at [jjeff07.github.io/libreclient](https://jjeff07.github.io/libreclient/).

## How It Works

The docs follow a **single source of truth** philosophy — content is written once in the project root
(`README.md`, `CONTRIBUTING.md`, `COMMIT_TYPES.md`) and pulled into the docs site at build time using
a macros plugin. This means the repo-level docs and the website are always in sync.

### Architecture

```
Project Root                         Docs Site
─────────────                        ─────────
README.md            ──┐
CONTRIBUTING.md      ──┼──▶  scripts/zensical_macros.py  ──▶  docs/*.md  ──▶  Built Site
COMMIT_TYPES.md      ──┘
```

## Key Files

| File                         | Purpose                                                                       |
|------------------------------|-------------------------------------------------------------------------------|
| `zensical.toml`              | Site configuration (name, theme, extensions, features)                        |
| `scripts/zensical_macros.py` | Macros plugin that reads markdown files and exposes them as template variables |
| `docs/index.md`              | Homepage — renders `{{ README_MAIN }}`                                        |
| `docs/development.md`        | Dev guide — renders `{{ README_DEVELOPMENT }}` and `{{ README_CONTRIBUTING }}`|
| `docs/CONTRIBUTING.md`       | Contributing guide — renders `{{ CONTRIBUTING }}`                             |
| `docs/COMMIT_TYPES.md`       | Commit reference — renders `{{ COMMIT_TYPES }}`                               |
| `docs/support.md`            | Support & issues info, with `{{ SECURITY }}` appended at the bottom           |
| `docs/documentation.md`      | This page (written directly, not macro-generated)                             |

## Template Variables

The macros plugin (`scripts/zensical_macros.py`) exposes these variables for use in any docs page:

| Variable                    | Source                                                      |
|-----------------------------|-------------------------------------------------------------|
| `{{ README_MAIN }}`         | README.md without the Contributing and Development sections |
| `{{ README_CONTRIBUTING }}` | The `## Contributing` section extracted from README.md      |
| `{{ README_DEVELOPMENT }}`  | The `## Development` section extracted from README.md       |
| `{{ CONTRIBUTING }}`        | Full contents of CONTRIBUTING.md                            |
| `{{ COMMIT_TYPES }}`        | Full contents of COMMIT_TYPES.md                            |
| `{{ SECURITY }}`            | Full contents of SECURITY.md                                |

## Live Reload & Watch

The `zensical.toml` config includes a `watch` list so that changes to the source markdown files
trigger a live reload during local development:

```toml
watch = [
    "scripts/zensical_macros.py",
    "README.md",
    "COMMIT_TYPES.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
]
```

## Running Locally

To serve the docs site locally with live reload:

```bash
uv run zensical serve
```

To build a static version:

```bash
uv run zensical build
```

## Adding a New Page

1. Create a new `.md` file in the `docs/` directory.
2. Add front matter with a title and icon:
   ```markdown
   ---
   title: My New Page
   description: A brief description for SEO
   icon: lucide/icon-name
   ---
   ```
3. Write content directly, or use a macro variable if the content lives in a root-level file.
4. If using a new macro variable, add it to `scripts/zensical_macros.py` and update the `watch` list in `zensical.toml`
   if needed.
5. **Update the navigation** in `zensical.toml` under the `nav` array to include the new page.

### Navigation Configuration

The site uses explicit navigation defined in `zensical.toml`:

```toml
nav = [
    {"Getting Started" = "index.md"},
    {"Support" = "support.md"},
    {
        "Development" = [
            "development.md",
            "documentation.md",
            "CONTRIBUTING.md",
            "COMMIT_TYPES.md"
        ]
    },
    {"GitHub Repo" = "https://github.com/jjeff07/libreclient"}
]
```

Pages not listed in `nav` won't appear in the sidebar navigation.

### Link Compatibility

Root-level markdown files (like `README.md` and `CONTRIBUTING.md`) contain relative links such as
`[COMMIT_TYPES.md](COMMIT_TYPES.md)` or `[CONTRIBUTING.md](CONTRIBUTING.md)`. For these links to
work both on GitHub **and** in the docs site, the docs pages must use matching filenames:

| Root file link target | Docs file              |
|-----------------------|------------------------|
| `CONTRIBUTING.md`     | `docs/CONTRIBUTING.md` |
| `COMMIT_TYPES.md`     | `docs/COMMIT_TYPES.md` |

This way, when the macros inject content from root files into the docs, relative links resolve
correctly in both contexts without any rewriting.

## Adding Content via Macros

If you want to reuse content from a root-level markdown file:

1. Open `scripts/zensical_macros.py`.
2. Read the file and assign it to a variable:
   ```python
   with open(md_dir / "MY_FILE.md", "r", encoding="utf8") as f:
       env.variables["MY_FILE"] = f.read()
   ```
3. Use `{{ MY_FILE }}` in your docs page.
4. Add the source file to the `watch` list in `zensical.toml`.

## Theme & Features

The site uses Zensical's default theme with light/dark mode toggle and includes features like:

- Instant navigation with prefetching
- Code block copy buttons and annotations
- Content tabs and footnote tooltips
- Navigation sections, footer navigation, and breadcrumb paths
- Search with highlighting

These are configured in the `[project.theme]` section of `zensical.toml`.
