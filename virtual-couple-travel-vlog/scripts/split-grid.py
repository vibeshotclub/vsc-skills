import argparse
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser(description="Split a 4x4 grid image into four 2x2 quadrant images.")
    parser.add_argument("--input-image", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--prefix", default="memory_sheet")
    args = parser.parse_args()

    input_path = Path(args.input_image)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(input_path).convert("RGB")
    width, height = image.size
    cell_w = width // 4
    cell_h = height // 4
    sheet_w = cell_w * 2
    sheet_h = cell_h * 2

    index = 1
    for row_block in range(2):
        for col_block in range(2):
            left = col_block * sheet_w
            top = row_block * sheet_h
            crop = image.crop((left, top, left + sheet_w, top + sheet_h))
            output_path = output_dir / f"{args.prefix}_{index:02d}.png"
            if output_path.exists():
                output_path = output_dir / f"{args.prefix}_{index:02d}_new.png"
            crop.save(output_path)
            print(output_path)
            index += 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
