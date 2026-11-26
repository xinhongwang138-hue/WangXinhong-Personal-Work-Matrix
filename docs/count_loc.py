#!/usr/bin/env python3
"""统计本地仓库的源码行数、文件数与测试用例数。

用法：
    python docs/count_loc.py ../ecommerce-operation-assistant ../contract-approval ...

口径见 docs/VERIFY.md：按扩展名统计行数，排除依赖/构建目录与锁文件；
测试用例为静态匹配 `def test_` / `it(` / `test(`，不代表已通过。
"""

from __future__ import annotations

import os
import re
import sys

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "venv",
    ".pytest_cache",
    "coverage",
    ".turbo",
}
COUNT_EXT = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".vue",
    ".sql",
    ".css",
    ".html",
    ".ps1",
    ".sh",
}
TEST_DIR_RE = re.compile(r"(^|/)(tests?|__tests__)/")
TEST_FILE_RE = re.compile(r"(test_|_test|\.test\.|\.spec\.)")
PY_TEST_RE = re.compile(r"^\s*(?:async\s+)?def\s+test_", re.M)
JS_TEST_RE = re.compile(r"^\s*(?:it|test)\s*\(", re.M)


def walk(repo: str) -> dict:
    total = files = tests = test_files = 0
    by_ext: dict[str, int] = {}
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in COUNT_EXT or "lock" in name:
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            lines = text.count("\n") + 1
            total += lines
            files += 1
            by_ext[ext] = by_ext.get(ext, 0) + lines
            posix = path.replace(os.sep, "/")
            if TEST_DIR_RE.search(posix) or TEST_FILE_RE.search(name):
                test_files += 1
                tests += len(PY_TEST_RE.findall(text)) + len(JS_TEST_RE.findall(text))
    return {
        "loc": total,
        "files": files,
        "tests": tests,
        "test_files": test_files,
        "by_ext": by_ext,
    }


def main() -> int:
    targets = sys.argv[1:]
    if not targets:
        print(__doc__)
        return 1

    agg = {"loc": 0, "files": 0, "tests": 0}
    print(f"{'repo':38} {'LOC':>8} {'files':>6} {'tests':>6}")
    print("-" * 62)
    for repo in targets:
        if not os.path.isdir(repo):
            print(f"{repo:38} {'(not found)':>22}")
            continue
        r = walk(repo)
        name = os.path.basename(os.path.normpath(repo))
        print(f"{name:38} {r['loc']:>8,} {r['files']:>6} {r['tests']:>6}")
        for k in agg:
            agg[k] += r[k]
        detail = " · ".join(
            f"{ext} {n:,}" for ext, n in sorted(r["by_ext"].items(), key=lambda x: -x[1])
        )
        print(f"{'':38} {detail}")
    print("-" * 62)
    print(f"{'TOTAL':38} {agg['loc']:>8,} {agg['files']:>6} {agg['tests']:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
