import os

# Creadentials
GITHUB_API = "https://api.github.com"
USERNAME = os.getenv("GITHUB_ACTOR")
TOKEN = os.getenv("RepoLoc")

OUTPUT = "loc-summary.json"
REPO_CACHE_FILE = "repo.json"
