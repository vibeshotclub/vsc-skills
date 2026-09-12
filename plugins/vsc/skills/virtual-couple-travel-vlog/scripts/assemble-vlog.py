import argparse
import subprocess
import time
from pathlib import Path


def unique_output(path):
    if not path.exists():
        return path
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return path.with_name(f"{path.stem}_{stamp}{path.suffix}")


def ffmpeg_concat_path(path):
    resolved = path.resolve()
    text = resolved.as_posix()
    return text.replace("'", "'\\''")


def run_ffmpeg(args):
    return subprocess.run(["ffmpeg", *args]).returncode


def main():
    parser = argparse.ArgumentParser(description="Assemble ordered vlog clips with FFmpeg.")
    parser.add_argument("--clips", nargs="+", required=True, help="Ordered clip paths, for example clip_01.mp4 clip_02.mp4.")
    parser.add_argument("--music", default="", help="Optional music/audio file to mux into the final video.")
    parser.add_argument("--output", required=True, help="Final MP4 output path.")
    parser.add_argument("--work-dir", default="", help="Temporary work directory. Defaults to the output directory.")
    args = parser.parse_args()

    clips = [Path(clip) for clip in args.clips]
    for clip in clips:
        if not clip.exists():
            raise FileNotFoundError(f"Clip not found: {clip}")

    music = Path(args.music) if args.music else None
    if music and not music.exists():
        raise FileNotFoundError(f"Music file not found: {music}")

    output = unique_output(Path(args.output))
    output.parent.mkdir(parents=True, exist_ok=True)

    work_dir = Path(args.work_dir) if args.work_dir else output.parent
    work_dir.mkdir(parents=True, exist_ok=True)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    concat_list = work_dir / f"concat_list_{stamp}.txt"
    joined_video = work_dir / f"joined_silent_{stamp}.mp4"

    concat_lines = [f"file '{ffmpeg_concat_path(clip)}'" for clip in clips]
    concat_list.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")

    copy_args = ["-hide_banner", "-n", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(joined_video)]
    copy_exit = run_ffmpeg(copy_args)
    if copy_exit != 0 or not joined_video.exists():
        encode_args = [
            "-hide_banner",
            "-n",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(joined_video),
        ]
        encode_exit = run_ffmpeg(encode_args)
        if encode_exit != 0:
            raise RuntimeError("FFmpeg could not concatenate the clips.")

    if music:
        music_args = [
            "-hide_banner",
            "-n",
            "-i",
            str(joined_video),
            "-i",
            str(music),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output),
        ]
        music_exit = run_ffmpeg(music_args)
        if music_exit != 0:
            raise RuntimeError("FFmpeg could not add the music track.")
    else:
        final_args = ["-hide_banner", "-n", "-i", str(joined_video), "-c", "copy", str(output)]
        final_exit = run_ffmpeg(final_args)
        if final_exit != 0:
            raise RuntimeError("FFmpeg could not write the final video.")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
