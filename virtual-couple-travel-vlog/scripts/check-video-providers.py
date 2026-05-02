import argparse
import os
from pathlib import Path


def first_env(names):
    for name in names:
        if os.environ.get(name):
            return name
    return ""


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
        home / ".agents" / "skills" / "topview",
        home / ".codex" / "skills" / "topview",
    ]
    return first_existing(candidates)


def print_table(rows):
    headers = ["Provider", "Connected", "Evidence", "Notes"]
    values = [
        [
            row["provider"],
            "yes" if row["connected"] else "no",
            row["evidence"],
            row["notes"],
        ]
        for row in rows
    ]
    widths = [max(len(str(row[i])) for row in ([headers] + values)) for i in range(len(headers))]
    print("  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("  ".join("-" * widths[i] for i in range(len(headers))))
    for row in values:
        print("  ".join(str(row[i]).ljust(widths[i]) for i in range(len(headers))))


def main():
    parser = argparse.ArgumentParser(description="Detect connected video generation providers.")
    parser.add_argument("--topview-skill", default="")
    args = parser.parse_args()

    topview_path = find_topview(args.topview_skill)
    providers = [
        {
            "provider": "Topview",
            "connected": bool(topview_path),
            "evidence": topview_path,
            "notes": "Use automated Omni Reference when the Topview skill is installed and authenticated.",
        },
        {
            "provider": "Seedance API",
            "connected": bool(first_env(["SEEDANCE_API_KEY", "ARK_API_KEY", "VOLCENGINE_ACCESS_KEY_ID"])),
            "evidence": first_env(["SEEDANCE_API_KEY", "ARK_API_KEY", "VOLCENGINE_ACCESS_KEY_ID"]),
            "notes": "Adapt exported prompts and reference images to the provider's reference workflow.",
        },
        {
            "provider": "Krea",
            "connected": bool(first_env(["KREA_API_KEY"])),
            "evidence": first_env(["KREA_API_KEY"]),
            "notes": "If no API is connected, use Krea manually with the exported assets.",
        },
        {
            "provider": "Lovart",
            "connected": bool(first_env(["LOVART_API_KEY"])),
            "evidence": first_env(["LOVART_API_KEY"]),
            "notes": "If no API is connected, use Lovart manually with the exported assets.",
        },
        {
            "provider": "LibTV",
            "connected": bool(first_env(["LIBTV_API_KEY", "LIBTV_TOKEN"])),
            "evidence": first_env(["LIBTV_API_KEY", "LIBTV_TOKEN"]),
            "notes": "If no API is connected, use LibTV manually with the exported assets.",
        },
    ]

    print_table(providers)
    if not any(row["connected"] for row in providers):
        print("\nNo connected video generation provider was detected.")
        print("Ask which platform the user wants to use, then provide manual upload instructions using:")
        print("- images/memory_sheet_01.png ... memory_sheet_04.png")
        print("- images/character_male.png")
        print("- images/character_female.png")
        print("- prompts/video_clip_01.txt ... video_clip_04.txt")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
