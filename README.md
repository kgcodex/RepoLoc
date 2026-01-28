# RepoLoc

<div align="center">
  <img src="RepoLoc.gif" width="700" style="border-radius: 12px;" />
</div>

An incremental, cache-aware Lines of Code (LOC) analyzer for GitHub profiles, built with Python and GitHub Actions.

This project computes accurate, defensible LOC metrics across all repositories you own, while avoiding unnecessary recomputation, inflated counts, and CI overhead.

## Why RepoLoc?

Existing LOC tools either overcount generated code, recompute everything on each run, or don’t integrate cleanly with GitHub profiles. RepoLoc was built to provide an incremental, transparent, and portfolio-friendly LOC metric that reflects intentional code only.

## Features

- Counts LOC across owned GitHub repositories (excludes forks & archived repos)
- Incremental computation using commit-hash caching
- Automatically removes deleted repositories
- One-repo-at-a-time processing (low memory usage)
- Flexible, language-agnostic design via LANG_MAP
- Configurable ignores via locignore.txt
- Weekly scheduled runs + manual runs with fresh start option
- Outputs frontend-ready JSON
- Fully automated via GitHub Actions

## Output Files

1. repo.json (cache – internal)

   Stores per-repository LOC along with the commit hash used to compute it.

   repo.json is updated incrementally and should not be edited manually.
   This file allows:
   - skipping unchanged repositories
   - resuming safely after failures
   - detecting deleted repos

2. loc-summary.json (public / frontend-ready)

   Aggregated LOC across all repositories.

## GitHub Actions

Triggers

- Weekly (automatic)
- Manual (on demand) with optional fresh start flag

## Fresh vs Incremental Runs

Mode Behavior

- fresh=false (default) Only recomputes repos whose commit hash changed
- fresh=true Recomputes all repositories

## LOC Definition

A line is counted as code if:

- it is not empty
- it is not a single-line comment (#, //)
- it is not inside a block comment (/_ ... _/)
- it belongs to a language defined in LANG_MAP
- it is not ignored by locignore.txt

## Supported Languages

Languages are defined in LANG_MAP inside the script.
Example:

```json
LANG_MAP = {
".js": "JavaScript",
".jsx": "JavaScript",
".ts": "TypeScript",
".tsx": "TypeScript",
".py": "Python",
".java": "Java"
}
```

Adding a new language requires only one line.

## Ignore Rules

All exclusions are defined in locignore.txt.

Ignored categories include:

- dependencies (node_modules, venv)
- build outputs (dist, build, .next)
- assets (images, fonts)
- config files
- lock files
- generated files
- vendor files
- boilerplate
- UI scaffolding

This keeps LOC honest and defensible.

## Required Setup

Create a PAT with:

1. Create a Personal Access Token (PAT) with repository contents read & write access.

2. Add it as a repository secret: RepoLoc

## Using in a Portfolio

Fetch the summary directly:

```js
fetch(
  "https://raw.githubusercontent.com/<username>/RepoLoc/main/loc-summary.json",
);
```

Displays:

- total LOC
- per-language breakdown
- last updated time

## Transparency Statement

LOC metrics are computed using a custom Python analyzer, excluding dependencies, generated files, configuration files, markup, and styles, based on locignore.txt.
