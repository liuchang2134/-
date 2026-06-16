from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
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


def zh_terms(text: str) -> str:
    replacements = [
        ("Always In Long", "多头控制"),
        ("Always In Short", "空头控制"),
        ("Always In", "控制权"),
        ("Breakout Mode", "突破模式"),
        ("Breakout Pullback", "突破回踩"),
        ("Breakout", "突破"),
        ("Pullback", "回调"),
        ("Follow-through", "跟随"),
        ("Measured Move", "测量移动"),
        ("Major Trend Reversal", "主要趋势反转"),
        ("Trading Range", "交易区间"),
        ("Tight Trading Range", "窄交易区间"),
        ("High 3", "第三次上破"),
        ("Low 3", "第三次下破"),
        ("High 2", "第二次上破"),
        ("Low 2", "第二次下破"),
        ("High 1", "第一次上破"),
        ("Low 1", "第一次下破"),
        ("Signal Bar", "信号蜡烛"),
        ("Entry Bar", "入场蜡烛"),
        ("Signal", "信号"),
        ("Entry", "入场"),
        ("Final Flag", "末端旗形"),
        ("Wedge", "楔形"),
        ("Climax", "高潮"),
        ("Gap", "缺口"),
        ("EMA", "均线"),
        ("MTR", "主要趋势反转"),
        ("BO", "突破"),
        ("PB", "回调"),
        ("TR", "交易区间"),
        ("TTR", "窄交易区间"),
        ("setup", "形态"),
        ("Setup", "形态"),
    ]
    result = str(text)
    for old, new in replacements:
        result = result.replace(old, new)
    return result


def looks_like_viewer_sidebar(image: Image.Image) -> bool:
    """Detect screenshots that include a PDF/video outline panel on the left."""
    width, height = image.size
    left_probe = image.crop((0, 0, min(230, width), min(120, height))).convert("RGB")
    center_probe = image.crop((width // 3, 0, width - 8, min(120, height))).convert("RGB")

    def avg_brightness(region: Image.Image) -> float:
        arr = np.array(region, dtype=np.float32)
        return float(arr.mean())

    left_bright = avg_brightness(left_probe)
    center_bright = avg_brightness(center_probe)
    return left_bright > 205 and center_bright < 205


def orange_slide_ratio(image: Image.Image) -> float:
    arr = np.array(image.convert("RGB"))
    orange = (arr[:, :, 0] > 165) & (arr[:, :, 1] >= 55) & (arr[:, :, 1] <= 140) & (arr[:, :, 2] < 45)
    return float(orange.mean())


def clean_source_image(image: Image.Image, pattern: dict) -> Image.Image:
    """Hide embedded English slide text while preserving the chart structure."""
    image = image.convert("RGB")

    if looks_like_viewer_sidebar(image):
        width, height = image.size
        left = int(width * 0.23)
        top = int(height * 0.11)
        right = width - 8
        bottom = int(height * 0.875)
        image = image.crop((left, top, right, bottom))

    width, height = image.size
    cleaned = image.convert("RGBA")
    mask = Image.new("RGBA", cleaned.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    white = (255, 255, 255, 255)

    if orange_slide_ratio(image) > 0.35:
        draw.rectangle((0, 0, width, height), fill=(213, 102, 0, 255))
        card = (int(width * 0.09), int(height * 0.24), int(width * 0.91), int(height * 0.73))
        draw.rounded_rectangle(card, radius=18, fill=(255, 255, 255, 255), outline=(255, 255, 255, 255), width=2)
        card_draw = ImageDraw.Draw(mask)
        x = card[0] + 28
        y = card[1] + 30
        card_draw.text((x, y), f"中文章节封面：{zh_terms(pattern.get('title', '价格行为形态'))}", font=FONT_TITLE, fill=(20, 33, 43))
        y += 44
        card_draw.text((x, y), "原英文标题已隐藏，本页作为章节入口保留。", font=FONT_BODY, fill=(82, 100, 121))
        y += 36
        card_draw.text((x, y), "请继续查看同一形态下的其它K线样本。", font=FONT_BODY, fill=(82, 100, 121))
        return Image.alpha_composite(cleaned, mask).convert("RGB")

    # Brooks slides place most English prose in predictable zones: title bar,
    # upper explanatory text blocks, lower captions, and footer/page metadata.
    zones = [
        (0, 0, width, int(height * 0.105)),
        (int(width * 0.02), int(height * 0.095), int(width * 0.60), int(height * 0.245)),
        (int(width * 0.62), int(height * 0.095), int(width * 0.98), int(height * 0.305)),
        (int(width * 0.26), int(height * 0.805), int(width * 0.78), int(height * 0.94)),
        (0, int(height * 0.94), width, height),
    ]
    for zone in zones:
        draw.rectangle(zone, fill=white)

    cleaned = Image.alpha_composite(cleaned, mask).convert("RGB")
    cleaned = remove_colored_english_annotations(cleaned)
    return scrub_slide_text_zones(cleaned)


def remove_colored_english_annotations(image: Image.Image) -> Image.Image:
    """Drop colored slide annotations; keep the black/white price bars."""
    arr = np.array(image.convert("RGB"))
    maxc = arr.max(axis=2).astype(np.int16)
    minc = arr.min(axis=2).astype(np.int16)
    brightness = arr.mean(axis=2)
    colored = ((maxc - minc) > 42) & (brightness > 55)
    arr[colored] = [255, 255, 255]
    return Image.fromarray(arr, "RGB")


def scrub_slide_text_zones(image: Image.Image) -> Image.Image:
    """Clear common prose areas after color removal, preserving dark candles."""
    arr = np.array(image.convert("RGB"))
    height, width = arr.shape[:2]

    zones = [
        (0, 0, width, int(height * 0.12)),
        (int(width * 0.02), int(height * 0.10), int(width * 0.62), int(height * 0.38)),
        (int(width * 0.56), int(height * 0.10), int(width * 0.99), int(height * 0.40)),
        (int(width * 0.00), int(height * 0.36), int(width * 0.68), int(height * 0.64)),
        (int(width * 0.02), int(height * 0.54), int(width * 0.80), int(height * 0.83)),
        (int(width * 0.18), int(height * 0.65), int(width * 0.86), int(height * 0.92)),
        (0, int(height * 0.88), width, height),
    ]

    for x1, y1, x2, y2 in zones:
        x1 = max(0, min(width, x1))
        x2 = max(0, min(width, x2))
        y1 = max(0, min(height, y1))
        y2 = max(0, min(height, y2))
        if x1 >= x2 or y1 >= y2:
            continue

        region = arr[y1:y2, x1:x2]
        maxc = region.max(axis=2).astype(np.int16)
        minc = region.min(axis=2).astype(np.int16)
        brightness = region.mean(axis=2)

        # Candles and wicks are the only original pixels kept in prose zones.
        # Faint anti-aliased text, colored notes, EMA lines and captions become white.
        dark_neutral = (brightness < 82) & ((maxc - minc) < 48)
        very_dark = brightness < 52
        keep_price_marks = dark_neutral | very_dark
        keep_price_marks = remove_tiny_components(keep_price_marks)
        region[~keep_price_marks] = [255, 255, 255]

    return Image.fromarray(arr, "RGB")


def remove_tiny_components(mask: np.ndarray) -> np.ndarray:
    """Remove dust-like leftovers from anti-aliased text in scrubbed zones."""
    height, width = mask.shape
    visited = np.zeros(mask.shape, dtype=bool)
    cleaned = mask.copy()

    for y in range(height):
        for x in range(width):
            if visited[y, x] or not mask[y, x]:
                continue

            stack = [(x, y)]
            visited[y, x] = True
            pixels: list[tuple[int, int]] = []
            min_x = max_x = x
            min_y = max_y = y

            while stack:
                px, py = stack.pop()
                pixels.append((px, py))
                if px < min_x:
                    min_x = px
                elif px > max_x:
                    max_x = px
                if py < min_y:
                    min_y = py
                elif py > max_y:
                    max_y = py

                for nx in (px - 1, px, px + 1):
                    for ny in (py - 1, py, py + 1):
                        if nx == px and ny == py:
                            continue
                        if nx < 0 or nx >= width or ny < 0 or ny >= height:
                            continue
                        if visited[ny, nx] or not mask[ny, nx]:
                            continue
                        visited[ny, nx] = True
                        stack.append((nx, ny))

            comp_w = max_x - min_x + 1
            comp_h = max_y - min_y + 1
            area = len(pixels)
            likely_text_dust = area <= 24 or (area <= 70 and comp_h <= 9) or (area <= 90 and comp_w <= 5)
            if likely_text_dust:
                for px, py in pixels:
                    cleaned[py, px] = False

    return cleaned


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
        image = clean_source_image(image, pattern)
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
    pattern_title = zh_terms(pattern["title"])
    title = f"中文标注版｜{pattern_title}｜胜率口径 {pattern.get('winRate', '条件型')}｜样本 {index + 1}/5"
    draw.text((22, 16), title, font=FONT_TITLE, fill=(255, 255, 255))
    source = f"来源：图表百科 · 第 {chart.get('page', '')} 页"
    draw.text((22, 50), source, font=FONT_TINY, fill=(201, 218, 224))

    best = short(zh_terms(first(pattern.get("best"), "先确认市场背景。")), 42)
    entry = short(zh_terms(first(pattern.get("entry"), "等待触发，不提前进场。")), 42)
    stop = short(zh_terms(first(pattern.get("stop"), "止损放在结构外。")), 34)
    target = short(zh_terms(first(pattern.get("target"), "先看 1R 或下一个磁力位。")), 34)
    trap = short(zh_terms(first(pattern.get("traps"), "背景不成立时放弃。")), 52)

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
    draw.text((22, footer_y + 14), "读图顺序：1 背景 → 2 位置 → 3 信号蜡烛 → 4 入场蜡烛 → 5 风险收益 → 6 失效", font=FONT_BODY, fill=dark)
    trap_lines = wrap_text(draw, f"失效提醒：{trap}", FONT_SMALL, width - 44)
    y = footer_y + 50
    for line in trap_lines[:2]:
        draw.text((22, y), line, font=FONT_SMALL, fill=(82, 100, 121))
        y += 24
    draw.text((max(22, width - 295), footer_y + footer_h - 28), "原图英文说明已遮盖，保留价格结构", font=FONT_TINY, fill=(101, 115, 129))

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
