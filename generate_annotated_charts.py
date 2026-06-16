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
FONT_MICRO = font(13)
FONT_NANO = font(12)


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


def zh_terms(text: str) -> str:
    replacements = [
        ("Always In Long", "Always In 多头"),
        ("Always In Short", "Always In 空头"),
        ("Always In", "Always In"),
        ("Brooks", "Brooks"),
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
        ("Signal Bar", "信号K"),
        ("Entry Bar", "入场K"),
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


def display_title(text: str) -> str:
    """Translate chart titles and remove duplicate bilingual remnants."""
    translated = zh_terms(text)
    parts = [part.strip() for part in re.split(r"\s*/\s*", translated) if part.strip()]
    unique: list[str] = []
    for part in parts:
        if part not in unique:
            unique.append(part)
    return " / ".join(unique) if unique else translated


def pa_cn(text: str) -> str:
    """Polish source notes into concise price-action Chinese."""
    result = zh_terms(text)
    replacements = [
        ("清晰支撑阻力、区间高低点或趋势线被突破", "关键支撑/阻力被有效突破"),
        ("突破K实体大，收盘靠近极端", "突破K实体大，收盘强"),
        ("后续1-3根K没有立刻回到原区间", "后续1-3根K不回到区间"),
        ("突破收盘后顺势入场", "突破收盘后顺势入场"),
        ("等待第一次小回调或突破回踩入场", "等第一次回调或突破回踩"),
        ("强趋势日可用小仓位追随", "强趋势日小仓位跟随"),
        ("突破前价位明显", "突破位明确"),
        ("突破后有跟随", "突破后有跟随"),
        ("回踩不深，且没有强反向收盘", "回踩浅，且无强反向收盘"),
        ("Always In 多头 清晰", "Always In 多头清晰"),
        ("Always In 空头 清晰", "Always In 空头清晰"),
        ("回调两段但没有破坏趋势", "两段回调未破坏趋势"),
        ("第二次向上触发买入", "第二次上破触发买入"),
        ("第二次向下触发卖出", "第二次下破触发卖出"),
        ("信号K高点上方买入", "突破信号K高点买入"),
        ("信号K低点下方卖出", "跌破信号K低点卖出"),
        ("用信号K高/低点触发", "突破信号K触发"),
        ("回踩突破点后顺突破方向入场", "回踩突破点后顺势入场"),
        ("回踩低/高点外", "回踩极点外"),
        ("回调低点下方", "回调低点下方"),
        ("回调高点上方", "回调高点上方"),
        ("通道低买/高卖取决于方向", "通道低买高卖要看方向"),
        ("觉得太高/太低就逆势", "只因觉得太高太低就逆势"),
        ("跌/突破旗形另一侧后入场", "破旗形另一侧后反向入场"),
        ("跌/突破信号K另一端", "破信号K另一侧后反向"),
        ("上方/下方有明显目标", "上下方有明显磁力位"),
        ("中间阻力/支撑少", "中间阻力或支撑少"),
        ("区间中线/另一侧", "区间中线或另一侧"),
        ("交易区间中间硬数H2", "交易区间中间不要硬数H2"),
        ("把区间中间波动当L2", "区间中间不要硬数L2"),
        ("突破K另一端", "突破K另一侧"),
        ("信号K另一端", "信号K另一侧"),
        ("缺口另一侧", "缺口另一侧"),
        ("突破点另一侧", "突破点另一侧"),
        ("测量移动", "测量目标"),
        ("下一个磁力位", "下一个磁力位"),
        ("至少先看1R，再根据跟随决定是否波段", "先看1R，再看跟随决定是否波段"),
        ("背景不成立时放弃，不在区间中间追单", "背景不成立就放弃，不在区间中间追单"),
        ("趋势已经坏掉仍买", "趋势结构已坏仍买入"),
        ("趋势结构坏掉仍买", "趋势结构已坏仍买入"),
        ("反弹已转多仍卖", "反弹转强仍卖出"),
        ("反弹转强仍卖", "反弹转强仍卖出"),
        ("信号K太大导致风险收益差", "信号K过大，盈亏比变差"),
        ("目标太近仍追单", "空间不足仍追单"),
        ("突破后没有跟随仍死扛", "突破无跟随仍死扛"),
        ("不要默认大波段", "不默认大波段"),
        ("EMA被当成魔法线", "不要把EMA当魔法线"),
        ("第三推失败后买入", "第三推失败后买入"),
        ("第三推失败后卖出", "第三推失败后卖出"),
        ("没有形成强多头跟随", "多头跟随不足"),
        ("若反弹突破趋势线并跟随则放弃", "反弹破线并跟随就放弃"),
        ("在支撑位上方空间不足", "支撑上方空间不足"),
    ]
    for old, new in replacements:
        result = result.replace(old, new)
    result = re.sub(r"\s+", " ", result).strip()
    result = result.replace(" ,", "，").replace(",", "，")
    return result


def compact_chart_note(text: str) -> str:
    """Short complete sentences for in-chart overlays."""
    result = pa_cn(text)
    replacements = [
        ("关键支撑/阻力被有效突破", "关键位被有效突破"),
        ("突破位明确", "突破位明确"),
        ("回踩浅，且无强反向收盘", "回踩浅，无强反向"),
        ("突破K实体大，收盘强", "突破K大，强收盘"),
        ("后续1-3根K不回到区间", "后续K线不回区间"),
        ("突破收盘后顺势入场", "突破收盘顺势入场"),
        ("等第一次回调或突破回踩", "等首次回调/回踩"),
        ("强趋势日小仓位跟随", "强趋势小仓位跟随"),
        ("Always In 多头清晰", "Always In 多头清晰"),
        ("Always In 空头清晰", "Always In 空头清晰"),
        ("两段回调未破坏趋势", "两段回调未破趋势"),
        ("反弹两段但没有形成强多头跟随", "两段反弹，多头跟随弱"),
        ("第二次上破信号K质量好", "二次上破信号K好"),
        ("第二次下破信号K质量好", "二次下破信号K好"),
        ("第二次上破触发买入", "二次上破买入"),
        ("第二次下破触发卖出", "二次下破卖出"),
        ("突破信号K高点买入", "上破信号K买入"),
        ("跌破信号K低点卖出", "下破信号K卖出"),
        ("交易区间中间不要硬数H2", "区间中段不硬数H2"),
        ("区间中间不要硬数L2", "区间中段不硬数L2"),
        ("趋势结构已坏仍买入", "趋势已坏仍买入"),
        ("反弹转强仍卖出", "反弹转强仍卖出"),
        ("信号K过大，盈亏比变差", "信号K过大，盈亏比差"),
        ("测量目标", "测量目标"),
        ("下一个磁力位", "下一磁力位"),
        ("先看1R，再看跟随决定是否波段", "先看1R，再看跟随"),
        ("区间中间的假突破", "区间中段假突破"),
        ("高潮末端追单", "高潮末端追价"),
        ("突破无跟随仍死扛", "突破无跟随仍硬扛"),
        ("破旗形另一侧后反向入场", "破旗形另一侧反向"),
        ("破信号K另一侧后反向", "破信号K另一侧反向"),
        ("通道低买高卖要看方向", "通道低买高卖看方向"),
        ("只因觉得太高太低就逆势", "凭感觉高低就逆势"),
        ("上下方有明显磁力位", "上下方有磁力位"),
        ("中间阻力或支撑少", "中间阻力/支撑少"),
        ("背景不成立就放弃，不在区间中间追单", "背景不成立就放弃"),
        ("顺趋势回调，背景比机械数K更重要", "顺趋势回调，背景比数K重要"),
        ("反转是过程，等破线、测试失败和二次信号", "反转要等破线、测试和二次信号"),
        ("三推只代表动能衰竭，仍要等触发", "三推提示衰竭，仍等触发"),
        ("关键看突破后的跟随，而不是只看突破K", "关键看突破后的跟随"),
        ("区间优先买低卖高，突破没有跟随就降级", "区间先买低卖高"),
    ]
    for old, new in replacements:
        result = result.replace(old, new)
    return result.rstrip("。；;，,").strip()


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


def is_chapter_cover_image(image: Image.Image) -> bool:
    arr = np.array(image.convert("RGB"))
    brightness = arr.mean(axis=2)
    maxc = arr.max(axis=2)
    minc = arr.min(axis=2)
    orange = (arr[:, :, 0] > 150) & (arr[:, :, 1] >= 50) & (arr[:, :, 1] <= 155) & (arr[:, :, 2] < 85) & ((arr[:, :, 0] - arr[:, :, 1]) > 45)
    dark = (brightness < 90) & ((maxc - minc) < 70)
    return float(orange.mean()) > 0.42 and float(dark.mean()) < 0.004


def clean_source_image(image: Image.Image, pattern: dict, chart: dict, index: int) -> Image.Image | None:
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

    if is_chapter_cover_image(image):
        return None

    return replace_english_with_chinese_panels(image, pattern, chart, index)


def as_list(value) -> list[str]:
    if isinstance(value, list):
        return [pa_cn(str(item)) for item in value if item]
    if value:
        return [pa_cn(str(value))]
    return []


def panel_lines(pattern: dict, kind: str) -> list[str]:
    best = as_list(pattern.get("best"))
    entry = as_list(pattern.get("entry"))
    stop = as_list(pattern.get("stop"))
    target = as_list(pattern.get("target"))
    traps = as_list(pattern.get("traps"))
    summary = pa_cn(pattern.get("summary", "先判断市场背景，再找信号K和入场K。"))

    if kind == "background":
        return chart_safe_lines(best[:2] or [summary], limit=2)
    if kind == "trigger":
        return chart_safe_lines(entry[:2] or ["等待信号K收盘确认，再考虑入场"], limit=2)
    if kind == "plan":
        return chart_safe_lines([
            f"止损：{stop[0] if stop else '放在结构外'}",
            f"目标：{target[0] if target else '先看1R或下一个磁力位'}",
        ], limit=2)
    if kind == "risk":
        return chart_safe_lines(traps[:2] or ["背景不成立时放弃，不在区间中间追单"], limit=2)
    if kind == "summary":
        return chart_safe_lines([family_chart_summary(pattern, summary)], limit=2)
    return ["用中文替换原图英文说明，按背景、触发、风险、目标阅读"]


def chart_safe_lines(lines: list[str], limit: int = 2) -> list[str]:
    cleaned = [compact_chart_note(line) for line in lines if line]
    cleaned = [line.rstrip("。；;，,") for line in cleaned]
    return cleaned[:limit] or ["先看背景，再等信号K触发"]


def family_chart_summary(pattern: dict, fallback: str) -> str:
    family = pattern.get("family", "")
    if family == "突破":
        return "关键看突破后的跟随，而不是只看突破K"
    if family == "回调":
        return "顺趋势回调，背景比机械数K更重要"
    if family == "交易区间":
        return "区间优先买低卖高，突破没有跟随就降级"
    if family == "通道":
        return "紧密通道顺势，宽通道按双向交易管理"
    if family == "反转/MTR":
        return "反转是过程，等破线、测试失败和二次信号"
    if family == "楔形":
        return "三推只代表动能衰竭，仍要等触发"
    if family == "缺口":
        return "缺口要看是否回补，未回补才有测量意义"
    if family == "K线信号":
        return "信号K必须服从背景和位置"
    return fallback


def footer_sections(pattern: dict) -> list[tuple[str, str]]:
    best = as_list(pattern.get("best"))
    entry = as_list(pattern.get("entry"))
    stop = as_list(pattern.get("stop"))
    target = as_list(pattern.get("target"))
    traps = as_list(pattern.get("traps"))
    return [
        ("背景", first(best, pa_cn(pattern.get("summary", "先判断市场背景")))),
        ("触发", first(entry, "等待信号K触发")),
        ("止损", first(stop, "放在结构外")),
        ("目标", first(target, "先看1R，再看磁力位")),
        ("失效", first(traps, "背景不成立就放弃")),
    ]


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
    max_width = max(80, x2 - x1 - pad * 2)
    max_height = max(20, y2 - y1 - 28)
    fnt, line_h, wrapped = fit_wrapped_lines(draw, lines, max_width, max_height)
    widths = [text_width(draw, f"{label}：", FONT_SMALL)]
    widths.extend(text_width(draw, line, fnt) for line in wrapped)
    bg_w = min(x2 - x1, max(widths, default=120) + pad * 2 + 8)
    bg_h = min(y2 - y1, 30 + max(1, len(wrapped)) * line_h + 6)
    draw.rectangle((x1 + 2, y1 + 1, x1 + 2 + bg_w, y1 + 1 + bg_h), fill=(255, 255, 255, 238))

    draw.text((x1 + pad, y1 + 4), f"{label}：", font=FONT_SMALL, fill=accent)
    text_y = y1 + 28
    for line in wrapped:
        draw.text((x1 + pad, text_y), line, font=fnt, fill=(24, 34, 43))
        text_y += line_h


def fit_wrapped_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    max_width: int,
    max_height: int,
) -> tuple[ImageFont.FreeTypeFont, int, list[str]]:
    candidates = [(FONT_TINY, 20), (FONT_MICRO, 17), (FONT_NANO, 15)]
    prepared = [compact_chart_note(line) for line in lines if line]
    for fnt, line_h in candidates:
        max_lines = max(1, max_height // line_h)
        selected: list[str] = []
        for line in prepared:
            wrapped = wrap_text(draw, line, fnt, max_width)
            if len(selected) + len(wrapped) <= max_lines:
                selected.extend(wrapped)
        if selected:
            return fnt, line_h, selected

    # Last-resort fallback uses a complete, compact note instead of cutting a
    # sentence in half.
    fnt, line_h = candidates[-1]
    fallback = compact_chart_note(prepared[0] if prepared else "先看背景，再等信号K触发")
    return fnt, line_h, wrap_text(draw, fallback, fnt, max_width)


def text_block_size(
    draw: ImageDraw.ImageDraw,
    label: str,
    lines: list[str],
    max_width: int,
    max_height: int,
) -> tuple[int, int]:
    pad = 8
    fnt, line_h, wrapped = fit_wrapped_lines(draw, lines, max_width - pad * 2, max_height - 28)
    widths = [text_width(draw, f"{label}：", FONT_SMALL)]
    widths.extend(text_width(draw, line, fnt) for line in wrapped)
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
        (0, int(height * 0.34), width, int(height * 0.66)),
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
        colored_text = dilate_mask(text_seed, radius=5)
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
                2 <= comp_w <= 72
                and 3 <= comp_h <= 34
                and area <= 620
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
    title = display_title(pattern.get("title", "价格行为形态"))

    # Replace the slide title/footer in place.
    draw.rectangle((0, 0, width, title_h), fill=(213, 102, 0, 255))
    draw.text((24, 12), f"{title}｜中文替换版｜样本 {index + 1}/5", font=FONT_TITLE, fill=(255, 255, 255))
    draw.rectangle((0, footer_top, width, height), fill=(213, 102, 0, 255))
    footer = f"来源：艾尔布鲁克斯图表百科｜第 {chart.get('page', '')} 页｜英文说明已用中文覆盖"
    draw.text((20, footer_top + 8), footer, font=FONT_TINY, fill=(255, 248, 235))

    candidate_panels = [
        ((0.035, 0.112, 0.560, 0.285), "背景", "background", (15, 118, 110)),
        ((0.555, 0.112, 0.965, 0.320), "触发", "trigger", (37, 99, 168)),
        ((0.035, 0.315, 0.545, 0.560), "背景", "background", (15, 118, 110)),
        ((0.535, 0.315, 0.965, 0.575), "风控", "plan", (169, 111, 23)),
        ((0.030, 0.545, 0.440, 0.780), "风险", "risk", (201, 79, 54)),
        ((0.430, 0.545, 0.965, 0.785), "结论", "summary", (15, 118, 110)),
        ((0.025, 0.760, 0.440, 0.930), "风险", "risk", (201, 79, 54)),
        ((0.335, 0.760, 0.880, 0.930), "结论", "summary", (15, 118, 110)),
    ]

    drawn_boxes: list[tuple[int, int, int, int]] = []
    drawn_kinds: set[str] = set()
    for ratio_box, label, kind, accent in candidate_panels:
        if kind in drawn_kinds:
            continue
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
        drawn_kinds.add(kind)

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


def footer_layout(draw: ImageDraw.ImageDraw, width: int, sections: list[tuple[str, str]]) -> tuple[int, list[dict]]:
    margin = 22
    gap = 12
    columns = 5 if width >= 980 else 3
    col_w = max(120, (width - margin * 2 - gap * (columns - 1)) // columns)
    line_h = 18
    label_h = 23
    top_y = 58
    layouts: list[dict] = []
    row_heights: list[int] = []

    for idx, (label, text) in enumerate(sections):
        row = idx // columns
        col = idx % columns
        wrapped = wrap_text(draw, pa_cn(text), FONT_MICRO, col_w)
        block_h = label_h + max(1, len(wrapped)) * line_h
        while len(row_heights) <= row:
            row_heights.append(0)
        row_heights[row] = max(row_heights[row], block_h)
        layouts.append({
            "row": row,
            "col": col,
            "label": label,
            "lines": wrapped,
            "block_h": block_h,
        })

    row_tops: list[int] = []
    y = top_y
    for row_h in row_heights:
        row_tops.append(y)
        y += row_h + 14

    for item in layouts:
        item["x"] = margin + item["col"] * (col_w + gap)
        item["y"] = row_tops[item["row"]]
        item["w"] = col_w

    footer_h = max(150, y + 18)
    return footer_h, layouts


def draw_structured_footer(
    draw: ImageDraw.ImageDraw,
    footer_y: int,
    width: int,
    footer_h: int,
    layouts: list[dict],
    pattern: dict,
) -> None:
    dark = (20, 33, 43)
    draw.rectangle((0, footer_y, width, footer_y + footer_h), fill=(255, 255, 255))
    draw.line((0, footer_y, width, footer_y), fill=(219, 227, 234), width=2)
    draw.text((22, footer_y + 14), "读图顺序：背景 → 位置 → 信号K → 入场K → 风险收益 → 失效", font=FONT_BODY, fill=dark)
    for item in layouts:
        x = item["x"]
        y = footer_y + item["y"]
        draw.text((x, y), f"{item['label']}：", font=FONT_SMALL, fill=(15, 118, 110))
        text_y = y + 23
        for line in item["lines"]:
            draw.text((x, text_y), line, font=FONT_MICRO, fill=(82, 100, 121))
            text_y += 18
    note = f"中文标注按 Brooks 价格行为语境整理；胜率口径：{pattern.get('winRate', '条件型')}。"
    draw.text((22, footer_y + footer_h - 26), note, font=FONT_TINY, fill=(101, 115, 129))


def annotate(pattern: dict, chart: dict, index: int) -> bool:
    raw_src = ROOT / chart["src"]
    out_src = ROOT / chart["src"].replace("assets/ab-charts/", "assets/ab-charts-annotated/").replace(".jpg", "-annotated.jpg")
    out_src.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(raw_src) as image:
        image = clean_source_image(image, pattern, chart, index)
        if image is None:
            if out_src.exists():
                out_src.unlink()
            return False
        width, height = image.size
        header_h = 78
        temp_footer = Image.new("RGB", (width, 10), (255, 255, 255))
        temp_draw = ImageDraw.Draw(temp_footer)
        footer_h, footer_items = footer_layout(temp_draw, width, footer_sections(pattern))
        canvas = Image.new("RGB", (width, height + header_h + footer_h), (246, 248, 250))
        canvas.paste(image, (0, header_h))

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    accent = (15, 118, 110)
    dark = (20, 33, 43)

    draw.rectangle((0, 0, width, header_h), fill=dark)
    pattern_title = display_title(pattern["title"])
    title = f"中文标注版｜{pattern_title}｜胜率口径 {pattern.get('winRate', '条件型')}｜样本 {index + 1}/5"
    draw.text((22, 16), title, font=FONT_TITLE, fill=(255, 255, 255))
    source = f"来源：图表百科 · 第 {chart.get('page', '')} 页"
    draw.text((22, 50), source, font=FONT_TINY, fill=(201, 218, 224))

    footer_y = header_h + height
    draw_structured_footer(draw, footer_y, width, footer_h, footer_items, pattern)

    annotated = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    annotated.save(out_src, quality=88, optimize=True)
    return True


def main() -> None:
    patterns = load_window_json(ROOT / "encyclopedia-data.js", "PATTERN_ENCYCLOPEDIA")
    charts = load_window_json(ROOT / "ab-chart-assets.js", "AB_CHART_IMAGES")
    pattern_by_id = {pattern["id"]: pattern for pattern in patterns}

    total = 0
    skipped_covers = 0
    missing = []
    for pattern_id, chart_items in charts.items():
        pattern = pattern_by_id.get(pattern_id)
        if not pattern:
            missing.append(pattern_id)
            continue
        for index, chart in enumerate(chart_items):
            if annotate(pattern, chart, index):
                total += 1
            else:
                skipped_covers += 1
    print(json.dumps({"annotated": total, "skippedCovers": skipped_covers, "patterns": len(patterns), "missingPatterns": missing}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
