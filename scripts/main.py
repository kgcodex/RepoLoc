import argparse
import subprocess
import tempfile
from pathlib import Path

import github_utils
import loc
import repo_cache


def main(fresh: bool):
    ignore_patterns = loc.load_ignore_patterns()
    repos = github_utils.fetch_repos()

    repo_names = repos.keys()
    cache = repo_cache.load_repo_cache()

    # Remove deleted repos
    for cached_repo in list(cache.keys()):
        if cached_repo.startswith("_"):
            continue

        if cached_repo not in repo_names:
            del cache[cached_repo]

    repo_cache.save_repo_cache(cache)

    for repo_name, repo_data in repos.items():
        cached = cache.get(repo_name)
        cached_sha = cached.get("_meta").get("commit") if cached else None
        head_sha = repo_data.get("commit_sha")

        if not fresh and cached and cached_sha == head_sha:
            continue

        print(f"Processing {repo_name}.....")

        with tempfile.TemporaryDirectory() as temp:
            repo_dir = Path(temp) / repo_name

            subprocess.run(
                ["git", "clone", repo_data["clone_url"], repo_dir],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )

            loc_stats = loc.calculate_repo_loc(repo_dir, ignore_patterns)

        cache[repo_name] = {
            "_meta": {"commit": head_sha},
            **loc_stats,
        }

        repo_cache.save_repo_cache(cache)

    repo_cache.aggregate(cache)

    print("LOC calculation complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh", default="false")
    args = parser.parse_args()

    main(args.fresh.lower() == "true")
