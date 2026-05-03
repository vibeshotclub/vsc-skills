import argparse
import importlib.util
import os
import shutil
from pathlib import Path


def command_result(name, required=False, install_hint=""):
    found = shutil.which(name)
    return {
        "tool": name,
        "required": required,
        "found": bool(found),
        "path": found or "",
        "install_hint": "" if found else install_hint,
    }


def module_result(module_name, required=False, install_hint=""):
    found = importlib.util.find_spec(module_name) is not None
    return {
        "tool": f"python-module:{module_name}",
        "required": required,
        "found": found,
        "path": "available" if found else "",
        "install_hint": "" if found else install_hint,
    }


def first_existing(paths):
    for path in paths:
        if path and Path(path).exists():
            return str(Path(path))
    return ""


def find_topview(topview_skill):
    home = Path.home()
    candidates = [
        topview_skill,
        os.environ.get("TOPVIEW_SKILL", ""),
        str(home / ".agents" / "skills" / "topview"),
        str(home / ".codex" / "skills" / "topview"),
    ]
    return first_existing(candidates)


def find_remotion_skill():
    home = Path.home()
    candidates = [
        home / ".codex" / "plugins" / "cache" / "openai-curated" / "remotion",
        home / ".codex" / "skills" / "remotion-best-practices",
        home / ".agents" / "skills" / "remotion-best-practices",
    ]
    return first_existing(str(path) for path in candidates)


def print_table(results):
    headers = ["Tool", "Required", "Found", "Path"]
    rows = [
        [
            item["tool"],
            "yes" if item["required"] else "no",
            "yes" if item["found"] else "no",
            item["path"],
        ]
        for item in results
    ]
    widths = [
        max(len(str(row[i])) for row in ([headers] + rows))
        for i in range(len(headers))
    ]
    print("  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("  ".join("-" * widths[i] for i in range(len(headers))))
    for row in rows:
        print("  ".join(str(row[i]).ljust(widths[i]) for i in range(len(headers))))


def main():
    parser = argparse.ArgumentParser(description="Check cross-platform dependencies for the virtual couple travel vlog skill.")
    parser.add_argument("--topview-skill", default="")
    parser.add_argument("--show-install-hints", action="store_true")
    args = parser.parse_args()

    topview_path = find_topview(args.topview_skill)
    remotion_skill_path = find_remotion_skill()

    results = [
        command_result("python", True, "Install Python 3.10+ from python.org or your OS package manager."),
        module_result("PIL", True, "python -m pip install Pillow"),
        command_result("ffmpeg", True, "Install FFmpeg from ffmpeg.org or your OS package manager."),
        command_result("ffprobe", True, "Install FFmpeg/FFprobe from ffmpeg.org or your OS package manager."),
        command_result("node", True, "Install Node.js LTS from nodejs.org or your OS package manager."),
        command_result("npm", True, "Install Node.js LTS from nodejs.org or your OS package manager."),
        command_result("npx", True, "Install Node.js LTS from nodejs.org or your OS package manager."),
        command_result("remotion", False, "Optional global CLI. If missing, use npx remotion inside a Remotion project."),
        {
            "tool": "remotion-plugin",
            "required": True,
            "found": bool(remotion_skill_path),
            "path": remotion_skill_path,
            "install_hint": "Install or enable the Remotion plugin/skill before using Remotion assembly.",
        },
        {
            "tool": "topview-skill",
            "required": False,
            "found": bool(topview_path),
            "path": topview_path,
            "install_hint": "Optional. Install/connect Topview only if this user wants automated Topview generation.",
        },
    ]

    print_table(results)

    if args.show_install_hints:
        missing = [item for item in results if item["required"] and not item["found"]]
        if missing:
            print("\nMissing required dependencies. Ask the user before installing:")
            for item in missing:
                print(f"- {item['tool']}: {item['install_hint']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
