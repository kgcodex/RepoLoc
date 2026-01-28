import requests
from constant import GITHUB_API, TOKEN, USERNAME


def github_get(url: str):
    req = requests.get(
        url,
        headers={"Authorization": f"token {TOKEN}"},
        timeout=30,
    )
    if req.status_code == 409:
        return None

    req.raise_for_status()
    return req.json()


def fetch_repos() -> dict[str, dict[str, str]]:
    repos = {}
    page = 1

    while True:
        data = github_get(
            f"{GITHUB_API}/users/{USERNAME}/repos?per_page=100&page={page}"
        )
        if not data:
            break

        for repo in data:
            if repo["fork"] or repo["archived"]:
                continue

            # Commit Head SHA
            commit_sha = github_get(
                f"{GITHUB_API}/repos/{USERNAME}/{repo['name']}/commits/{repo['default_branch']}"
            )
            if not commit_sha:
                continue

            repos[repo["name"]] = {
                "clone_url": repo["clone_url"],
                "default_branch": repo["default_branch"],
                "commit_sha": commit_sha["sha"],
            }
        page += 1

    return repos
