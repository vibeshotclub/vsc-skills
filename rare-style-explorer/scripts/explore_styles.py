#!/usr/bin/env python3
import argparse
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIBRARY_PATH = ROOT / "references" / "style_library.json"

BASE_CATEGORIES = {
    "电影、电视与影像类型",
    "动画、漫画与插画亚种",
    "摄影工艺与影像缺陷",
    "工艺、地域视觉与历史媒介",
    "数字、游戏、UI与计算机视觉",
}
SURFACE_CATEGORIES = {"材质与表面质感"}
FORMAT_CATEGORIES = {
    "平面设计、印刷与海报亚种",
    "玩具、产品与收藏品呈现",
}
SPACE_CATEGORIES = {"建筑、空间与场景气质"}
DEFECT_HINTS = ("缺陷", "复印", "扫描", "CRT", "VHS", "胶片", "噪点", "压缩", "印刷")
LIGHT_HINTS = ("光", "lighting", "light", "灯", "色彩", "霓虹", "horror lighting")
FASHION_CATEGORIES = {"时装、亚文化与人物造型"}

NEGATIVE = (
    "avoid generic modern minimalism, avoid random extra text, avoid messy symbols, "
    "avoid distorted hands/faces, avoid losing subject identity"
)


TEMPLATES = {
    "minimal": "{subject}, {base}, {support}, clear silhouette, strong visual identity, high detail, {negative}",
    "product": "Hero product shot of {subject}, {base}, {support}, premium composition, clean background, readable shape, no clutter, product remains recognizable, {negative}",
    "character": "{subject} as a character, {fashion}, {base}, {support}, expressive pose, clear face, 1-2 key accessories only, {negative}",
    "poster": "Poster for {subject}, {base}, {support}, bold composition, limited pseudo-typography, strong title area, print texture, no long readable text, {negative}",
    "scene": "{subject} in {space}, {base}, {support}, cinematic shot, foreground subject, environment supports the story, not overcrowded, {negative}",
    "material-series": "{subject}, same composition, surface rendered as {surface}, material only on surface, recognizable object silhouette, studio lighting, {negative}",
}


def load_library():
    with LIBRARY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def category(style):
    return style.get("类别", "")


def tokens(style):
    return style.get("English prompt tokens", "").strip()


def style_name(style):
    return style.get("中文风格名", "").strip()


def has_any(text, hints):
    lower = text.lower()
    return any(h.lower() in lower for h in hints)


def pools(styles):
    base = [s for s in styles if category(s) in BASE_CATEGORIES]
    surface = [s for s in styles if category(s) in SURFACE_CATEGORIES]
    fmt = [s for s in styles if category(s) in FORMAT_CATEGORIES]
    space = [s for s in styles if category(s) in SPACE_CATEGORIES]
    fashion = [s for s in styles if category(s) in FASHION_CATEGORIES]
    defect = [
        s for s in styles
        if has_any(" ".join([category(s), style_name(s), tokens(s), s.get("组合角色", "")]), DEFECT_HINTS)
    ]
    light = [
        s for s in styles
        if has_any(" ".join([style_name(s), tokens(s), s.get("材质/色彩/光线", "")]), LIGHT_HINTS)
        and category(s) not in SURFACE_CATEGORIES
    ]
    return {
        "base": base,
        "surface": surface,
        "format": fmt,
        "space": space,
        "fashion": fashion,
        "defect": defect,
        "light": light,
    }


def pick(rng, items):
    return rng.choice(items) if items else None


def forced_base(styles, style_id):
    if not style_id:
        return None
    for style in styles:
        if style.get("style_id", "").lower() == style_id.lower():
            return style
    raise SystemExit(f"style_id not found: {style_id}")


def support_for_mode(rng, mode, p):
    parts = []
    selected = []
    if mode == "material-series":
        surface = pick(rng, p["surface"])
        return tokens(surface), [surface]
    if mode == "scene":
        layer = pick(rng, p["light"] + p["defect"])
    elif mode == "poster":
        layer = pick(rng, p["format"] + p["defect"])
    elif mode == "product":
        layer = pick(rng, p["surface"] + p["light"])
    else:
        layer = pick(rng, p["surface"] + p["light"] + p["format"] + p["space"] + p["defect"])
    if layer:
        parts.append(tokens(layer))
        selected.append(layer)
    if rng.random() < 0.45 and mode not in {"minimal", "material-series"}:
        defect = pick(rng, p["defect"])
        if defect and defect not in selected:
            parts.append(tokens(defect) + ", defect intensity below 0.55")
            selected.append(defect)
    return ", ".join(parts), selected


def make_variant(subject, mode, rng, p, fixed_base=None):
    base = fixed_base or pick(rng, p["base"])
    support, support_styles = support_for_mode(rng, mode, p)
    fashion = pick(rng, p["fashion"]) if mode == "character" else None
    space = pick(rng, p["space"]) if mode == "scene" else None
    surface = support_styles[0] if mode == "material-series" and support_styles else None
    prompt = TEMPLATES[mode].format(
        subject=subject,
        base=tokens(base),
        support=support,
        fashion=tokens(fashion) if fashion else "",
        space=tokens(space) if space else "a concrete atmospheric space",
        surface=tokens(surface) if surface else support,
        negative=NEGATIVE,
    )
    prompt = ", ".join([part.strip() for part in prompt.split(",") if part.strip()])
    used = [s for s in [base if mode != "material-series" else None, fashion, space, surface] + support_styles if s]
    deduped = []
    seen = set()
    for s in used:
        sid = s.get("style_id")
        if sid not in seen:
            deduped.append(s)
            seen.add(sid)
    return {
        "prompt": prompt,
        "styles": [
            {
                "style_id": s.get("style_id"),
                "name": style_name(s),
                "tokens": tokens(s),
                "category": category(s),
                "risk": s.get("容易翻车", ""),
                "fix": s.get("补救提示", ""),
            }
            for s in deduped
        ],
    }


def render_markdown(subject, mode, variants):
    lines = [f"# Rare Style Exploration: {subject}", "", f"- mode: `{mode}`", ""]
    for i, variant in enumerate(variants, 1):
        lines.append(f"## Variant {i}")
        lines.append("")
        lines.append(variant["prompt"])
        lines.append("")
        lines.append("Styles:")
        for style in variant["styles"]:
            lines.append(
                f"- {style['style_id']} {style['name']}: {style['tokens']} ({style['category']})"
            )
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate rare AIGC style prompt variants.")
    parser.add_argument("subject")
    parser.add_argument("--mode", choices=sorted(TEMPLATES), default="minimal")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--style-id", help="Force a base style by style_id, e.g. F004")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    data = load_library()
    styles = data["styles"]
    p = pools(styles)
    rng = random.Random(args.seed)
    fixed = forced_base(styles, args.style_id)
    variants = [make_variant(args.subject, args.mode, rng, p, fixed) for _ in range(args.count)]

    if args.format == "json":
        print(json.dumps({"subject": args.subject, "mode": args.mode, "variants": variants}, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(args.subject, args.mode, variants))


if __name__ == "__main__":
    main()
