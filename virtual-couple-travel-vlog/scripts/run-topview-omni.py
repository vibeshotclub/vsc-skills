import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def default_topview_video_script() -> str:
    candidates = []
    env_skill = os.environ.get("TOPVIEW_SKILL")
    if env_skill:
        candidates.append(Path(env_skill) / "scripts" / "video_gen.py")
    home = Path.home()
    candidates.extend(
        [
            home / ".agents" / "skills" / "topview" / "scripts" / "video_gen.py",
            home / ".codex" / "skills" / "topview" / "scripts" / "video_gen.py",
        ]
    )
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(candidates[0] if candidates else Path("video_gen.py"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Topview Omni Reference with safe JSON argument passing.")
    parser.add_argument("--topview-video-script", default=default_topview_video_script())
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--male-card", required=True)
    parser.add_argument("--female-card", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--board-id", required=True)
    parser.add_argument("--model", default="Standard")
    parser.add_argument("--aspect-ratio", default="9:16")
    parser.add_argument("--resolution", default="720")
    parser.add_argument("--duration", default="15")
    parser.add_argument("--count", default="1")
    parser.add_argument("--sound", default="off", choices=("on", "off"))
    parser.add_argument("--timeout", default="1800")
    parser.add_argument("--interval", default="10")
    args = parser.parse_args()

    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    input_images = json.dumps(
        [
            {"fileId": str(Path(args.sheet)), "name": "Image1"},
            {"fileId": str(Path(args.male_card)), "name": "Image2"},
            {"fileId": str(Path(args.female_card)), "name": "Image3"},
        ],
        ensure_ascii=False,
    )

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        args.topview_video_script,
        "run",
        "--type",
        "omni",
        "--model",
        args.model,
        "--prompt",
        prompt,
        "--input-images",
        input_images,
        "--aspect-ratio",
        args.aspect_ratio,
        "--resolution",
        str(args.resolution),
        "--duration",
        str(args.duration),
        "--count",
        str(args.count),
        "--sound",
        args.sound,
        "--board-id",
        args.board_id,
        "--output-dir",
        args.output_dir,
        "--timeout",
        str(args.timeout),
        "--interval",
        str(args.interval),
    ]
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
