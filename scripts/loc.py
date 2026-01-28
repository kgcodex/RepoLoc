import fnmatch
import os
from pathlib import Path

# Language Map
LANG_MAP = {
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".py": "Python",
    ".go": "Go",
    ".rs": "Rust",
}


def load_ignore_patterns(path="../locignore.txt") -> list:
    patterns = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def is_ignored(path: Path, patterns: list) -> bool:
    for p in patterns:
        p = p.rstrip("/")
        if fnmatch.fnmatch(path.name, p) or p in path.parts:
            return True
    return False


def is_multiline_comment_in_single_line(
    line: str, comment_pair: list[list[str, str]] = [["/*", "*/"], ["{/*", "*/}"]]
) -> bool:
    for start, end in comment_pair:
        if line.startswith(start) and line.endswith(end):
            return True
    return False


def count_file_loc(path: Path) -> int:
    loc = 0
    in_block_comment = False

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                # Single-line comments
                if line.startswith(("#", "//")):
                    continue

                # Multi-line comments
                if line.startswith(("/*", "{/*")):
                    if not is_multiline_comment_in_single_line(line):
                        in_block_comment = True
                    continue

                if in_block_comment:
                    if line.endswith(("*/", "*/}")):
                        in_block_comment = False
                    continue

                loc += 1
    except Exception:
        pass

    return loc


def calculate_repo_loc(repo_dir: Path, ignore_patterns) -> dict[str, int]:
    stats = {}

    for root, _, files in os.walk(repo_dir):
        root_path = Path(root)
        if is_ignored(root_path, ignore_patterns):
            continue

        for file in files:
            file_path = root_path / file
            if is_ignored(file_path, ignore_patterns):
                continue

            lang = LANG_MAP.get(file_path.suffix)

            if not lang:
                continue

            loc = count_file_loc(file_path)

            if loc == 0:
                continue

            stats[lang] = stats.get(lang, 0) + loc

    return stats
