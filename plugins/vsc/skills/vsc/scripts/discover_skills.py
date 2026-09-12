#!/usr/bin/env python3
"""Discover locally available catalog members. Python 3.10+, standard library only."""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^name:\s*(['\"]?)([a-z0-9]+(?:-[a-z0-9]+)*)\1\s*(?:#.*)?$", re.M)


def default_roots(skill_dir: Path, home: Path, cwd: Path, env: dict) -> list[Path]:
    roots = [skill_dir.parent]
    # The nearest project owns project-local installs; do not scan other projects.
    for parent in (cwd, *cwd.parents):
        if (parent / ".git").exists() or any((parent / folder / "skills").is_dir() for folder in (".agents", ".claude", ".codex")):
            roots.extend(parent / folder / "skills" for folder in (".agents", ".codex", ".claude"))
            break
    codex_home = Path(env["CODEX_HOME"]).expanduser() if env.get("CODEX_HOME") else home / ".codex"
    roots.extend([home / ".agents" / "skills", codex_home / "skills", home / ".claude" / "skills"])
    return roots


def load_catalog(path: Path) -> dict:
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(catalog, dict) or catalog.get("schema_version") != 1 or not isinstance(catalog.get("skills"), list):
        raise ValueError("无效的 VSC 目录格式")
    names = set()
    for item in catalog["skills"]:
        if not isinstance(item, dict):
            raise ValueError("无效的 VSC 目录条目")
        name = item.get("name", "")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name == "vsc" or name in names:
            raise ValueError("VSC 目录包含无效或重复的技能名称")
        names.add(name)
        for key in ("description", "category", "distinction"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f"{name}: 缺少能力字段 {key}")
        outputs = item.get("deliverables")
        if not isinstance(outputs, list) or not outputs or any(
            not isinstance(value, str) or value not in {"prompt", "image", "video", "workflow", "archive"}
            for value in outputs
        ):
            raise ValueError(f"{name}: 无效的交付类型")
        if not isinstance(item.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            raise ValueError(f"{name}: 缺少内容校验值")
    return catalog


def discover(catalog: dict, roots: list[Path]) -> dict:
    roots = list(dict.fromkeys(root.expanduser().resolve() for root in roots))
    result = []
    for entry in catalog["skills"]:
        found, errors, seen = [], [], set()
        for root in roots:
            candidate = root / entry["name"] / "SKILL.md"
            if not candidate.exists() and not candidate.is_symlink() and not candidate.parent.is_symlink():
                continue
            try:
                path = candidate.resolve(strict=True)
                if path in seen:
                    continue
                seen.add(path)
                content = path.read_text(encoding="utf-8")
                header = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
                # Only the simple name scalar is needed at runtime. Full YAML is
                # parsed by the build tool; unsupported headers require review.
                names = NAME.findall(header[1]) if header else []
                if len(names) != 1 or names[0][1] != entry["name"]:
                    raise ValueError("frontmatter 名称不匹配或不支持该名称写法")
                digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
                found.append({"path": str(path), "sha256": digest})
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append({"path": str(candidate), "reason": str(exc)})
        item = {key: value for key, value in entry.items() if key != "sha256"}
        hashes = {hit["sha256"] for hit in found}
        if len(hashes) > 1:
            item.update(status="conflict", paths=[hit["path"] for hit in found])
        elif found:
            item.update(status="available", path=found[0]["path"],
                        needs_review=found[0]["sha256"] != entry["sha256"])
        else:
            item["status"] = "invalid" if errors else "missing"
        if errors:
            item["errors"] = errors
        result.append(item)
    return {"schema_version": 1, "skills": result}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, action="append", help="技能父目录；可重复指定，替换所有默认搜索目录")
    args = parser.parse_args()
    try:
        catalog = load_catalog(SKILL_DIR / "references" / "catalog.json")
        roots = args.root if args.root is not None else default_roots(SKILL_DIR, Path.home(), Path.cwd(), os.environ)
        print(json.dumps(discover(catalog, roots), ensure_ascii=False, indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"VSC 技能发现失败：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
