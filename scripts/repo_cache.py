import json
import os
from datetime import datetime

from constant import OUTPUT, REPO_CACHE_FILE


def load_repo_cache():
    if not os.path.exists(REPO_CACHE_FILE):
        return {"_meta": {"version": 1}}
    with open(REPO_CACHE_FILE) as f:
        return json.load(f)


def save_repo_cache(cache):
    cache["_meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(REPO_CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def aggregate(cache):
    total = {}

    for repo, data in cache.items():
        if repo.startswith("_"):
            continue

        for lang, loc in data.items():
            if lang == "_meta":
                continue
            total[lang] = total.get(lang, 0) + loc

    summary = {
        "total": total,
        "repos_counted": len([repo for repo in cache if not repo.startswith("_")]),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }

    with open(OUTPUT, "w") as f:
        json.dump(summary, f, indent=2)
