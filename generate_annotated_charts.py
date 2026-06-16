from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "assets" / "ab-charts"
OUT_DIR = ROOT / "assets" / "ab-charts-annotated"


def load_window_json(path: Path, name: str):
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"window\.{re.escape(name)}\s*=\s*(.*);\s*$", text, re.S)
    if not match:
        raise ValueError(f"Cannot find window.{name} in {path}")
    raw = match.group(1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        quoted_keys = re.sub(r"([{\[,]\s*)([A-Za-z_][\w]*)\s*:", r'\1"\2":', raw)
        return json.loads(quoted_keys)


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


FONT_TITLE = font(26, True)
FONT_BODY = font(20)
FONT_SMALL = font(17)
FONT_TINY = font(15)


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in str(text):
        candidate = current + char
        if current and text_width(draw, candidate, fnt) > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def first(value, fallback: str) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    if value:
        return str(value)
    return fallback


def short(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + "..."


def draw_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    max_width: int,
    label: str,
    body: str,
    accent: tuple[int, int, int],
    fill: tuple[int, int, int, int] = (255, 255, 255, 230),
) -> int:
    x, y = xy
    title = f"{label}："
    body_lines = wrap_text(draw, body, FONT_SMALL, max_width - 24)
    line_h = 22
    height = 40 + line_h * len(body_lines)
    draw.rounded_rectangle((x, y, x + max_width, y + height), radius=10, fill=fill, outline=accent, width=2)
    draw.text((x + 12, y + 9), title, font=FONT_SMALL, fill=accent)
    text_y = y + 34
    for line in body_lines:
        draw.text((x + 12, text_y), line, font=FONT_TINY, fill=(24, 34, 43))
        text_y += line_h
    return height


def annotate(pattern: dict, chart: dict, index: int) -> None:
    raw_src = ROOT / chart["src"]
    out_src = ROOT / chart["src"].replace("assets/ab-charts/", "assets/ab-charts-annotated/").replace(".jpg", "-annotated.jpg")
    out_src.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(raw_src) as image:
        image = image.convert("RGB")
        width, height = image.size
        header_h = 78
        footer_h = 118
        canvas = Image.new("RGB", (width, height + header_h + footer_h), (246, 248, 250))
        canvas.paste(image, (0, header_h))

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    accent = (15, 118, 110)
    dark = (20, 33, 43)

    draw.rectangle((0, 0, width, header_h), fill=dark)
    title = f"中文标注版｜{pattern['title']}｜胜率口径 {pattern.get('winRate', '条件型')}｜样本 {index + 1}/5"
    draw.text((22, 16), title, font=FONT_TITLE, fill=(255, 255, 255))
    source = f"{chart.get('source', '')} · p.{chart.get('page', '')}"
    draw.text((22, 50), source, font=FONT_TINY, fill=(201, 218, 224))

    best = short(first(pattern.get("best"), "先确认市场背景。"), 42)
    entry = short(first(pattern.get("entry"), "等待触发，不提前进场。"), 42)
    stop = short(first(pattern.get("stop"), "止损放在结构外。"), 34)
    target = short(first(pattern.get("target"), "先看 1R 或下一个磁力位。"), 34)
    trap = short(first(pattern.get("traps"), "背景不成立时放弃。"), 52)

    chart_top = header_h + 16
    chart_bottom = header_h + height - 16
    box_w = min(390, max(290, width // 3))
    draw_box(draw, (16, chart_top), box_w, "背景", best, accent)
    draw_box(draw, (width - box_w - 16, chart_top), box_w, "触发", entry, (37, 99, 168))
    draw_box(draw, (16, max(chart_top + 90, chart_bottom - 92)), box_w, "止损", stop, (201, 79, 54))
    draw_box(draw, (width - box_w - 16, max(chart_top + 90, chart_bottom - 92)), box_w, "目标", target, (169, 111, 23))

    footer_y = header_h + height
    draw.rectangle((0, footer_y, width, footer_y + footer_h), fill=(255, 255, 255))
    draw.line((0, footer_y, width, footer_y), fill=(219, 227, 234), width=2)
    draw.text((22, footer_y + 14), "读图顺序：1 背景 → 2 位置 → 3 信号K → 4 入场K → 5 风险收益 → 6 失效", font=FONT_BODY, fill=dark)
    trap_lines = wrap_text(draw, f"失效提醒：{trap}", FONT_SMALL, width - 44)
    y = footer_y + 50
    for line in trap_lines[:2]:
        draw.text((22, y), line, font=FONT_SMALL, fill=(82, 100, 121))
        y += 24
    draw.text((width - 215, footer_y + footer_h - 28), "保留原图，叠加中文学习标注", font=FONT_TINY, fill=(101, 115, 129))

    annotated = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    annotated.save(out_src, quality=88, optimize=True)


def main() -> None:
    patterns = load_window_json(ROOT / "encyclopedia-data.js", "PATTERN_ENCYCLOPEDIA")
    charts = load_window_json(ROOT / "ab-chart-assets.js", "AB_CHART_IMAGES")
    pattern_by_id = {pattern["id"]: pattern for pattern in patterns}

    total = 0
    missing = []
    for pattern_id, chart_items in charts.items():
        pattern = pattern_by_id.get(pattern_id)
        if not pattern:
            missing.append(pattern_id)
            continue
        for index, chart in enumerate(chart_items):
            annotate(pattern, chart, index)
            total += 1
    print(json.dumps({"annotated": total, "patterns": len(patterns), "missingPatterns": missing}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
