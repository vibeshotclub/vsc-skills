#!/usr/bin/env python3
import argparse
import json
import random
import re
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

STYLE_FAMILIES = {
    "film": {"电影、电视与影像类型"},
    "fashion": {"时装、亚文化与人物造型"},
    "product": {"玩具、产品与收藏品呈现", "材质与表面质感"},
    "photography": {"摄影工艺与影像缺陷"},
    "illustration": {"动画、漫画与插画亚种"},
    "graphic": {"平面设计、印刷与海报亚种"},
    "craft": {"工艺、地域视觉与历史媒介"},
    "digital": {"数字、游戏、UI与计算机视觉"},
    "space": {"建筑、空间与场景气质"},
    "material": {"材质与表面质感"},
}

GENERIC_WORDS = {
    "a",
    "and",
    "art",
    "cinema",
    "cinematic",
    "color",
    "colored",
    "design",
    "editorial",
    "film",
    "glossy",
    "high",
    "illustration",
    "light",
    "lighting",
    "low",
    "modern",
    "old",
    "photo",
    "photography",
    "poster",
    "render",
    "retro",
    "soft",
    "style",
    "surreal",
    "the",
    "vintage",
    "with",
}

NEGATIVE = (
    "避免泛化的现代极简风，避免随机多余文字，避免混乱符号，"
    "避免手部和面部畸形，避免丢失主体身份"
)


TEMPLATES = {
    "minimal": "{subject}，{base}，{support}，主体轮廓清晰，视觉识别度强，高细节，{negative}",
    "product": "商业产品主视觉，主体是{subject}，{base}，{support}，高级构图，干净背景，造型可读，无杂物，产品保持可识别，{negative}",
    "character": "{subject}角色设计，{fashion}，{base}，{support}，姿态有表现力，面部清晰，只保留1-2个关键配饰，{negative}",
    "poster": "{subject}海报，{base}，{support}，大胆构图，少量伪文字，明确标题区域，印刷质感，不要长段可读文字，{negative}",
    "scene": "{subject}置于{space}，{base}，{support}，电影感镜头，主体在前景，环境服务叙事，不要过度拥挤，{negative}",
    "material-series": "{subject}，保持同一构图，表面呈现{surface}，材质只作用在表面，物体轮廓保持可识别，棚拍光线，{negative}",
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


def visual_dna(style):
    return style.get("视觉DNA / 关键词", "").strip()


def style_prompt(style):
    if not style:
        return ""
    name = style_name(style)
    dna = visual_dna(style)
    return f"{name}，{dna}" if dna else name


def clean_prompt(text):
    return "，".join(
        part.strip(" ，,")
        for part in text.replace(",", "，").split("，")
        if part.strip(" ，,")
    )


def has_any(text, hints):
    lower = text.lower()
    return any(h.lower() in lower for h in hints)


def pools(styles, style_family=None):
    family_categories = STYLE_FAMILIES.get(style_family or "", set())
    base_categories = family_categories or BASE_CATEGORIES
    base = [s for s in styles if category(s) in base_categories]
    if not base:
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


def meaningful_terms(style):
    words = re.findall(r"[a-z0-9]+", tokens(style).lower())
    return {w for w in words if len(w) > 2 and w not in GENERIC_WORDS}


def too_similar(style, seen_term_sets):
    terms = meaningful_terms(style)
    if not terms:
        return False
    for seen in seen_term_sets:
        shared = terms & seen
        if len(shared) >= 2 and len(shared) / max(1, min(len(terms), len(seen))) >= 0.5:
            return True
    return False


def style_weight(style, freshness="normal", avoid_generic=True):
    weight = 1.0
    terms = meaningful_terms(style)
    if freshness == "high":
        if style.get("来源批次"):
            weight *= 3.0
        if len(terms) >= 4:
            weight *= 1.4
    if avoid_generic:
        token_count = max(1, len(re.findall(r"[a-z0-9]+", tokens(style).lower())))
        specificity = len(terms) / token_count
        if len(terms) <= 1 or specificity < 0.35:
            weight *= 0.25
    return weight


def weighted_pick(rng, items, freshness="normal", avoid_generic=True):
    if not items:
        return None
    weights = [style_weight(s, freshness, avoid_generic) for s in items]
    total = sum(weights)
    if total <= 0:
        return rng.choice(items)
    threshold = rng.random() * total
    current = 0.0
    for style, weight in zip(items, weights):
        current += weight
        if current >= threshold:
            return style
    return items[-1]


def pick_unique(rng, items, state, freshness="normal", avoid_generic=True):
    if not items:
        return None

    def eligible(relax_category=False, relax_similarity=False, relax_used=False):
        result = []
        for style in items:
            sid = style.get("style_id")
            if not relax_used and sid in state["used_ids"]:
                continue
            if not relax_category and state["last_category"] == category(style):
                continue
            if not relax_similarity and too_similar(style, state["term_sets"]):
                continue
            result.append(style)
        return result

    candidates = eligible()
    if not candidates:
        candidates = eligible(relax_category=True)
    if not candidates:
        candidates = eligible(relax_category=True, relax_similarity=True)
    if not candidates:
        candidates = eligible(relax_category=True, relax_similarity=True, relax_used=True)

    style = weighted_pick(rng, candidates, freshness, avoid_generic)
    if style:
        state["used_ids"].add(style.get("style_id"))
        terms = meaningful_terms(style)
        if terms:
            state["term_sets"].append(terms)
        state["last_category"] = category(style)
    return style


def forced_base(styles, style_id):
    if not style_id:
        return None
    for style in styles:
        if style.get("style_id", "").lower() == style_id.lower():
            return style
    raise SystemExit(f"style_id not found: {style_id}")


def support_for_mode(rng, mode, p, state, freshness="normal", avoid_generic=True):
    parts = []
    selected = []
    if mode == "material-series":
        surface = pick_unique(rng, p["surface"], state, freshness, avoid_generic)
        return style_prompt(surface), [surface]
    if mode == "scene":
        layer = pick_unique(rng, p["light"] + p["defect"], state, freshness, avoid_generic)
    elif mode == "poster":
        layer = pick_unique(rng, p["format"] + p["defect"], state, freshness, avoid_generic)
    elif mode == "product":
        layer = pick_unique(rng, p["surface"] + p["light"], state, freshness, avoid_generic)
    else:
        layer = pick_unique(
            rng,
            p["surface"] + p["light"] + p["format"] + p["space"] + p["defect"],
            state,
            freshness,
            avoid_generic,
        )
    if layer:
        parts.append(style_prompt(layer))
        selected.append(layer)
    if rng.random() < 0.45 and mode not in {"minimal", "material-series"}:
        defect = pick_unique(rng, p["defect"], state, freshness, avoid_generic)
        if defect and defect not in selected:
            parts.append(style_prompt(defect) + "，媒介缺陷强度低于0.55")
            selected.append(defect)
    return ", ".join(parts), selected


def make_variant(subject, mode, rng, p, state, fixed_base=None, freshness="normal", avoid_generic=True):
    base = fixed_base or pick_unique(rng, p["base"], state, freshness, avoid_generic)
    if fixed_base:
        state["used_ids"].add(fixed_base.get("style_id"))
        terms = meaningful_terms(fixed_base)
        if terms and terms not in state["term_sets"]:
            state["term_sets"].append(terms)
        state["last_category"] = category(fixed_base)
    support, support_styles = support_for_mode(rng, mode, p, state, freshness, avoid_generic)
    fashion = (
        pick_unique(rng, p["fashion"], state, freshness, avoid_generic)
        if mode == "character" and category(base) not in FASHION_CATEGORIES
        else None
    )
    space = (
        pick_unique(rng, p["space"], state, freshness, avoid_generic)
        if mode == "scene" and category(base) not in SPACE_CATEGORIES
        else None
    )
    surface = support_styles[0] if mode == "material-series" and support_styles else None
    prompt = TEMPLATES[mode].format(
        subject=subject,
        base=style_prompt(base),
        support=support,
        fashion=style_prompt(fashion) if fashion else "",
        space=style_prompt(space) if space else "具体且有氛围的空间",
        surface=style_prompt(surface) if surface else support,
        negative=NEGATIVE,
    )
    prompt = clean_prompt(prompt)
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
                "source_batch": s.get("来源批次", ""),
            }
            for s in deduped
        ],
    }


def render_markdown(subject, mode, variants):
    lines = [f"# 稀有风格探索：{subject}", "", f"- mode: `{mode}`", ""]
    for i, variant in enumerate(variants, 1):
        lines.append(f"## Variant {i}")
        lines.append("")
        lines.append(variant["prompt"])
        lines.append("")
        lines.append("风格来源:")
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
    parser.add_argument("--freshness", choices=["normal", "high"], default="normal")
    parser.add_argument("--style-family", choices=sorted(STYLE_FAMILIES))
    parser.add_argument("--avoid-generic", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    data = load_library()
    styles = data["styles"]
    p = pools(styles, args.style_family)
    rng = random.Random(args.seed)
    fixed = forced_base(styles, args.style_id)
    state = {"used_ids": set(), "term_sets": [], "last_category": None}
    variants = [
        make_variant(
            args.subject,
            args.mode,
            rng,
            p,
            state,
            fixed,
            args.freshness,
            args.avoid_generic,
        )
        for _ in range(args.count)
    ]

    if args.format == "json":
        print(json.dumps({"subject": args.subject, "mode": args.mode, "variants": variants}, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(args.subject, args.mode, variants))


if __name__ == "__main__":
    main()
