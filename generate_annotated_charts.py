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
        ("Brooks", "布鲁克斯"),
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


def clean_source_image(image: Image.Image, pattern: dict, chart: dict, index: int) -> Image.Image:
    """Replace embedded English slide text with non-overlapping Chinese panels."""
    image = image.convert("RGB")

    if looks_like_viewer_sidebar(image):
        width, height = image.size
        left = int(width * 0.23)
        top = int(height * 0.11)
        right = width - 8
        bottom = int(height * 0.875)
        image = image.crop((left, top, right, bottom))

    width, height = image.size

    if orange_slide_ratio(image) > 0.35:
        return draw_chinese_chapter_cover(image, pattern)

    return replace_english_with_chinese_panels(image, pattern, chart, index)


def as_list(value) -> list[str]:
    if isinstance(value, list):
        return [zh_terms(str(item)) for item in value if item]
    if value:
        return [zh_terms(str(value))]
    return []


def panel_lines(pattern: dict, kind: str) -> list[str]:
    best = as_list(pattern.get("best"))
    entry = as_list(pattern.get("entry"))
    stop = as_list(pattern.get("stop"))
    target = as_list(pattern.get("target"))
    traps = as_list(pattern.get("traps"))
    summary = zh_terms(pattern.get("summary", "先判断市场背景，再找信号K和入场K。"))

    if kind == "background":
        return best[:2] or [summary]
    if kind == "trigger":
        return entry[:2] or ["等待信号K收盘确认，再考虑入场"]
    if kind == "plan":
        return [
            f"止损：{stop[0] if stop else '放在结构外'}",
            f"目标：{target[0] if target else '先看1R或下一个磁力位'}",
        ]
    if kind == "risk":
        return traps[:2] or ["背景不成立时放弃，不在区间中间追单"]
    if kind == "summary":
        return [summary]
    return ["用中文替换原图英文说明，按背景、触发、风险、目标阅读"]


def draw_chinese_chapter_cover(image: Image.Image, pattern: dict) -> Image.Image:
    width, height = image.size
    cleaned = image.convert("RGBA")
    overlay = Image.new("RGBA", cleaned.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.rectangle((0, 0, width, height), fill=(213, 102, 0, 255))
    card = (int(width * 0.09), int(height * 0.24), int(width * 0.91), int(height * 0.73))
    draw.rounded_rectangle(card, radius=18, fill=(255, 255, 255, 255), outline=(255, 255, 255, 255), width=2)
    x = card[0] + 28
    y = card[1] + 30
    draw.text((x, y), f"中文章节封面：{zh_terms(pattern.get('title', '价格行为形态'))}", font=FONT_TITLE, fill=(20, 33, 43))
    y += 44
    draw.text((x, y), "原英文标题已替换为中文，本页作为章节入口保留。", font=FONT_BODY, fill=(82, 100, 121))
    y += 36
    draw.text((x, y), "请继续查看同一形态下的其它K线样本。", font=FONT_BODY, fill=(82, 100, 121))
    return Image.alpha_composite(cleaned, overlay).convert("RGB")


def box_from_ratio(width: int, height: int, ratio_box: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = ratio_box
    return (int(width * x1), int(height * y1), int(width * x2), int(height * y2))


def zone_has_colored_text(image: Image.Image, box: tuple[int, int, int, int]) -> bool:
    x1, y1, x2, y2 = box
    region = np.array(image.crop((x1, y1, x2, y2)).convert("RGB"))
    if region.size == 0:
        return False
    maxc = region.max(axis=2).astype(np.int16)
    minc = region.min(axis=2).astype(np.int16)
    brightness = region.mean(axis=2)
    colored = ((maxc - minc) > 38) & (brightness > 70)
    dark_letters = (brightness < 125) & ((maxc - minc) > 14)
    # Keep this sensitive: it is better to add a Chinese replacement panel than
    # leave a readable English sentence in the chart.
    return int(colored.sum() + dark_letters.sum() * 0.45) > max(45, region.shape[0] * region.shape[1] * 0.0025)


def draw_translation_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    label: str,
    lines: list[str],
    accent: tuple[int, int, int],
) -> None:
    x1, y1, x2, y2 = box
    pad = 8
    # No visible box: the background is cleaned before this step, so only text
    # is drawn here.
    draw.text((x1 + pad, y1 + 4), f"{label}：", font=FONT_SMALL, fill=accent)

    max_width = max(80, x2 - x1 - pad * 2)
    max_height = max(20, y2 - y1 - 28)
    line_h = 20
    max_lines = max(1, max_height // line_h)
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(wrap_text(draw, line, FONT_TINY, max_width))
    if len(wrapped) > max_lines:
        wrapped = wrapped[:max_lines]
        wrapped[-1] = short(wrapped[-1], max(1, len(wrapped[-1]) - 1))

    text_y = y1 + 28
    for line in wrapped:
        draw.text((x1 + pad, text_y), line, font=FONT_TINY, fill=(24, 34, 43))
        text_y += line_h


def text_block_size(
    draw: ImageDraw.ImageDraw,
    label: str,
    lines: list[str],
    max_width: int,
    max_height: int,
) -> tuple[int, int]:
    pad = 8
    line_h = 20
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(wrap_text(draw, line, FONT_TINY, max_width - pad * 2))
    max_lines = max(1, (max_height - 28) // line_h)
    wrapped = wrapped[:max_lines]
    widths = [text_width(draw, f"{label}：", FONT_SMALL)]
    widths.extend(text_width(draw, line, FONT_TINY) for line in wrapped)
    block_w = min(max_width, max(widths, default=120) + pad * 2)
    block_h = min(max_height, 28 + line_h * max(1, len(wrapped)))
    return max(120, block_w), max(48, block_h)


def find_clear_text_box(
    image: Image.Image,
    search_box: tuple[int, int, int, int],
    target_w: int,
    target_h: int,
    existing: list[tuple[int, int, int, int]],
) -> tuple[int, int, int, int]:
    arr = np.array(image.convert("RGB"))
    height, width = arr.shape[:2]
    sx1, sy1, sx2, sy2 = search_box
    sx1, sy1 = max(0, sx1), max(0, sy1)
    sx2, sy2 = min(width, sx2), min(height, sy2)
    target_w = min(target_w, max(1, sx2 - sx1))
    target_h = min(target_h, max(1, sy2 - sy1))
    if sx1 >= sx2 or sy1 >= sy2:
        return (sx1, sy1, sx1 + target_w, sy1 + target_h)

    brightness = arr.mean(axis=2)
    dark = brightness < 115
    best: tuple[float, tuple[int, int, int, int]] | None = None
    step = 16
    max_y = max(sy1 + 1, sy2 - target_h + 1)
    max_x = max(sx1 + 1, sx2 - target_w + 1)
    for y in range(sy1, max_y, step):
        for x in range(sx1, max_x, step):
            candidate = (x, y, x + target_w, y + target_h)
            if any(boxes_overlap(candidate, old) for old in existing):
                continue
            region = dark[y : y + target_h, x : x + target_w]
            dark_ratio = float(region.mean()) if region.size else 1.0
            center_penalty = abs((x + target_w / 2) - (sx1 + sx2) / 2) / max(1, sx2 - sx1)
            score = dark_ratio * 10 + center_penalty
            if best is None or score < best[0]:
                best = (score, candidate)

    if best:
        return best[1]
    return (sx1, sy1, sx1 + target_w, sy1 + target_h)


def remove_colored_text_pixels_preserve_candles(image: Image.Image) -> Image.Image:
    """Hide colored English notes without touching black/white candlesticks."""
    arr = np.array(image.convert("RGB"))
    height, width = arr.shape[:2]
    zones = [
        (0, int(height * 0.105), width, int(height * 0.36)),
        (0, int(height * 0.60), width, int(height * 0.955)),
        (int(width * 0.14), int(height * 0.26), int(width * 0.86), int(height * 0.56)),
    ]

    for x1, y1, x2, y2 in zones:
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(width, x2), min(height, y2)
        if x1 >= x2 or y1 >= y2:
            continue

        region = arr[y1:y2, x1:x2]
        maxc = region.max(axis=2).astype(np.int16)
        minc = region.min(axis=2).astype(np.int16)
        brightness = region.mean(axis=2)

        # Colored slide prose is high-chroma. Black/white candles, wicks and
        # neutral EMA fragments are protected explicitly; this avoids the old
        # full-chart scrub that could delete small bars during translation.
        seed = ((maxc - minc) > 48) & (brightness > 70)
        text_seed = colored_text_component_mask(seed)
        colored_text = dilate_mask(text_seed, radius=3)
        preserve_price_marks = (brightness < 86) & ((maxc - minc) < 60)
        region[colored_text & ~preserve_price_marks] = [255, 255, 255]

    return Image.fromarray(arr, "RGB")


def colored_text_component_mask(mask: np.ndarray) -> np.ndarray:
    """Keep only small colored components that look like letters, not chart lines."""
    height, width = mask.shape
    visited = np.zeros(mask.shape, dtype=bool)
    text_mask = np.zeros(mask.shape, dtype=bool)

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
            fill_ratio = area / max(1, comp_w * comp_h)
            likely_letter = (
                2 <= comp_w <= 32
                and 3 <= comp_h <= 34
                and area <= 260
                and fill_ratio <= 0.78
            )
            likely_small_punctuation = area <= 18 and comp_w <= 12 and comp_h <= 12

            if likely_letter or likely_small_punctuation:
                for px, py in pixels:
                    text_mask[py, px] = True

    return text_mask


def dilate_mask(mask: np.ndarray, radius: int = 1) -> np.ndarray:
    height, width = mask.shape
    expanded = mask.copy()
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            y_src1 = max(0, -dy)
            y_src2 = min(height, height - dy)
            x_src1 = max(0, -dx)
            x_src2 = min(width, width - dx)
            y_dst1 = max(0, dy)
            y_dst2 = min(height, height + dy)
            x_dst1 = max(0, dx)
            x_dst2 = min(width, width + dx)
            expanded[y_dst1:y_dst2, x_dst1:x_dst2] |= mask[y_src1:y_src2, x_src1:x_src2]
    return expanded


def replace_english_with_chinese_panels(image: Image.Image, pattern: dict, chart: dict, index: int) -> Image.Image:
    width, height = image.size
    result = remove_colored_text_pixels_preserve_candles(image).convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    title_h = max(54, int(height * 0.105))
    footer_top = int(height * 0.955)
    title = zh_terms(pattern.get("title", "价格行为形态"))

    # Replace the slide title/footer in place.
    draw.rectangle((0, 0, width, title_h), fill=(213, 102, 0, 255))
    draw.text((24, 12), f"{title}｜中文替换版｜样本 {index + 1}/5", font=FONT_TITLE, fill=(255, 255, 255))
    draw.rectangle((0, footer_top, width, height), fill=(213, 102, 0, 255))
    footer = f"来源：艾尔布鲁克斯图表百科｜第 {chart.get('page', '')} 页｜英文说明已用中文覆盖"
    draw.text((20, footer_top + 8), footer, font=FONT_TINY, fill=(255, 248, 235))

    candidate_panels = [
        ((0.035, 0.112, 0.530, 0.245), "背景", "background", (15, 118, 110)),
        ((0.580, 0.112, 0.965, 0.300), "触发", "trigger", (37, 99, 168)),
        ((0.620, 0.305, 0.960, 0.440), "风控", "plan", (169, 111, 23)),
        ((0.025, 0.665, 0.335, 0.900), "风险", "risk", (201, 79, 54)),
        ((0.335, 0.785, 0.770, 0.930), "结论", "summary", (15, 118, 110)),
    ]

    drawn_boxes: list[tuple[int, int, int, int]] = []
    for ratio_box, label, kind, accent in candidate_panels:
        search_box = box_from_ratio(width, height, ratio_box)
        if not zone_has_colored_text(image, search_box):
            continue
        lines = panel_lines(pattern, kind)
        search_w = search_box[2] - search_box[0]
        search_h = search_box[3] - search_box[1]
        text_w, text_h = text_block_size(draw, label, lines, min(search_w, 420), search_h)
        box = find_clear_text_box(result.convert("RGB"), search_box, text_w, text_h, drawn_boxes)
        draw_translation_panel(draw, box, label, lines, accent)
        drawn_boxes.append(box)

    if not drawn_boxes:
        search_box = box_from_ratio(width, height, (0.035, 0.115, 0.530, 0.255))
        lines = panel_lines(pattern, "background")
        text_w, text_h = text_block_size(draw, "背景", lines, min(search_box[2] - search_box[0], 420), search_box[3] - search_box[1])
        fallback = find_clear_text_box(result.convert("RGB"), search_box, text_w, text_h, [])
        draw_translation_panel(draw, fallback, "背景", lines, (15, 118, 110))

    return Image.alpha_composite(result, overlay).convert("RGB")


def boxes_overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1


def annotate(pattern: dict, chart: dict, index: int) -> None:
    raw_src = ROOT / chart["src"]
    out_src = ROOT / chart["src"].replace("assets/ab-charts/", "assets/ab-charts-annotated/").replace(".jpg", "-annotated.jpg")
    out_src.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(raw_src) as image:
        image = clean_source_image(image, pattern, chart, index)
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

    trap = short(zh_terms(first(pattern.get("traps"), "背景不成立时放弃。")), 52)

    footer_y = header_h + height
    draw.rectangle((0, footer_y, width, footer_y + footer_h), fill=(255, 255, 255))
    draw.line((0, footer_y, width, footer_y), fill=(219, 227, 234), width=2)
    draw.text((22, footer_y + 14), "读图顺序：1 背景 → 2 位置 → 3 信号蜡烛 → 4 入场蜡烛 → 5 风险收益 → 6 失效", font=FONT_BODY, fill=dark)
    trap_lines = wrap_text(draw, f"失效提醒：{trap}", FONT_SMALL, width - 44)
    y = footer_y + 50
    for line in trap_lines[:2]:
        draw.text((22, y), line, font=FONT_SMALL, fill=(82, 100, 121))
        y += 24
    draw.text((max(22, width - 345), footer_y + footer_h - 28), "原图英文说明已用中文覆盖，避免重叠", font=FONT_TINY, fill=(101, 115, 129))

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
