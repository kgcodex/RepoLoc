# RepoLoc

Utility to provide total LOC across Github Repos, forked excluded.

GitHub LOC Dashboard

An incremental, cache-aware Lines of Code (LOC) analyzer for GitHub profiles, built with Python and GitHub Actions.

This project computes accurate, defensible LOC metrics across all repositories you own, while avoiding unnecessary recomputation, inflated counts, and CI overhead.

✨ Features

✅ Counts LOC across owned GitHub repositories (excludes forks & archived repos)

✅ Incremental computation using commit-hash caching

✅ Automatically removes deleted repositories

✅ One-repo-at-a-time processing (low memory usage)

✅ Flexible, language-agnostic design via LANG_MAP

✅ Configurable ignores via ignore.txt

✅ Weekly scheduled runs + manual runs with fresh option

✅ Outputs frontend-ready JSON

✅ Fully automated via GitHub Actions

📦 Output Files
repo.json (cache – internal)

Stores per-repository LOC along with the commit hash used to compute it.

{
"\_meta": {
"version": 1,
"last_updated": "2026-01-27T12:00:00Z"
},
"quiz-app": {
"\_meta": { "commit": "a1b2c3" },
"TypeScript": 4200,
"JavaScript": 1800
}
}

This file allows:

skipping unchanged repositories

resuming safely after failures

detecting deleted repos

loc-summary.json (public / frontend-ready)

Aggregated LOC across all repositories.

{
"total": {
"TypeScript": 4200,
"JavaScript": 1800,
"Python": 5100
},
"repos_counted": 3,
"generated_at": "2026-01-27T12:00:00Z"
}

👉 This is the file your portfolio frontend should consume.

🧠 How It Works (High Level)

Fetch all owned GitHub repositories via GitHub API

Load repo.json cache (if present)

Remove repos that no longer exist

For each repo:

fetch latest commit hash

skip if unchanged (unless --fresh)

clone repo (shallow clone)

calculate LOC

update cache immediately

Aggregate cache → loc-summary.json

Commit results back to the repo

🚀 GitHub Actions
Triggers

Weekly (automatic)

Manual (on demand) with optional fresh flag

on:
workflow_dispatch:
inputs:
fresh:
description: "Recalculate all repositories"
default: "false"
schedule: - cron: "0 0 \* \* 0"

Manual Run

Go to Actions

Select the workflow

Click Run workflow

(Optional) Set fresh = true

🔁 Fresh vs Incremental Runs
Mode Behavior
fresh=false (default) Only recomputes repos whose commit hash changed
fresh=true Recomputes all repositories
🧮 LOC Definition

A line is counted as code if:

it is not empty

it is not a single-line comment (#, //)

it is not inside a block comment (/_ ... _/)

it belongs to a language defined in LANG_MAP

it is not ignored by ignore.txt

Inline block comments after code still count as code.

🌍 Supported Languages

Languages are defined in LANG_MAP inside the script.

Example:

LANG_MAP = {
".js": "JavaScript",
".jsx": "JavaScript",
".ts": "TypeScript",
".tsx": "TypeScript",
".py": "Python",
".java": "Java"
}

👉 Adding a new language requires only one line.

🛑 Ignore Rules

All exclusions are defined in ignore.txt.

Ignored categories include:

dependencies (node_modules, venv)

build outputs (dist, build, .next)

assets (images, fonts)

config files

lock files

generated files

This keeps LOC honest and defensible.

🔐 Required Setup
GitHub Token

Create a token with:

repo access

Add it as a repository secret:

GH_TOKEN

📊 Using in a Portfolio

Fetch the summary directly:

fetch(
"https://raw.githubusercontent.com/<username>/<repo>/main/loc-summary.json"
)

Display:

total LOC

per-language breakdown

last updated time

🧑‍💼 Transparency Statement (Recommended)

LOC metrics are computed using a custom Python analyzer, excluding dependencies, generated files, configuration files, markup, and styles, based on ignore.txt.

🛠 Design Philosophy

This project prioritizes:

correctness over vanity

incremental computation over brute force

clarity over magic

config over hard-coding

It is intentionally not a compiler or cloc replacement — it is a portfolio-grade engineering metric.
