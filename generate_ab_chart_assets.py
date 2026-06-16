import hashlib
import json
import re
from io import BytesIO
from pathlib import Path

import pdfplumber
from PIL import Image


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
OUT_DIR = SITE / "assets" / "ab-charts"
OUT_JS = SITE / "ab-chart-assets.js"
EXAMPLES_PER_PATTERN = 5


PART_NAMES = {
    "1": "Encyclopedia_Part 1_407A-B.PDF",
    "2": "Encyclopedia_Part 2_288C.PDF",
    "3": "Encyclopedia_Part 3_385D-F.pdf",
    "4": "Encyclopedia_Part 4_169G.PDF",
    "9": "Encyclopedia_Part 9_240H-L.pdf",
    "10": "Encyclopedia_Part 10_383M.pdf",
    "11": "Encyclopedia_Part 11_468N-P.pdf",
    "12": "Encyclopedia_Part 12_394Q-SL.PDF",
    "13": "Encyclopedia_Part 13_16SM-SZ.PDF",
    "14": "Encyclopedia_Part 14_16T-TRD.pdf",
    "15": "Encyclopedia_Part 15_16TRD-V.pdf",
    "16": "Encyclopedia_Part 16_16W-Z.pdf",
}


def find_pdf(name):
    matches = list(ROOT.rglob(name))
    if not matches:
        raise FileNotFoundError(name)
    return matches[0]


def parse_patterns():
    text = (SITE / "encyclopedia-data.js").read_text(encoding="utf-8")
    blocks = re.findall(r"\{\s*id:\s*\".*?\n\s*\}", text, flags=re.S)
    patterns = []
    for block in blocks:
        def field(name):
            match = re.search(rf"{name}:\s*\"([^\"]+)\"", block)
            return match.group(1) if match else ""

        patterns.append({
            "id": field("id"),
            "title": field("title"),
            "family": field("family"),
            "source": field("source"),
        })
    return [pattern for pattern in patterns if pattern["id"]]


def pick_part_and_position(pattern):
    title = pattern["title"]
    family = pattern["family"]
    key = f"{title} {family} {pattern['source']}".lower()

    if family == "突破":
        return "1", 0.78
    if family == "缺口":
        return "4", 0.42
    if family == "回调":
        if "high" in key:
            return "9", 0.20
        if "low" in key:
            return "9", 0.88
        return "11", 0.78
    if family == "楔形":
        return "16", 0.28
    if family == "双顶双底":
        return "3", 0.18
    if family == "交易区间":
        if "barb" in key:
            return "1", 0.35
        return "15", 0.28
    if family == "通道":
        return "2", 0.38
    if family == "趋势":
        if "small" in key:
            return "13", 0.12
        if "micro" in key:
            return "10", 0.62
        return "14", 0.66
    if family == "开盘":
        return "11", 0.46
    if family == "反转/MTR":
        if "higher" in key or "lower" in key:
            return "9", 0.52
        return "10", 0.18
    if family == "末端旗形":
        return "3", 0.80
    if family == "三角形":
        return "14", 0.32
    if family == "头肩":
        return "9", 0.10
    if family == "圆弧":
        return "12", 0.18
    if family == "高潮":
        return "2", 0.54
    if family == "目标/磁力":
        if "ema" in key or "均线" in key:
            return "3", 0.48
        if "vacuum" in key or "真空" in key:
            return "1", 0.68
        return "10", 0.42
    if family == "入场逻辑":
        return "12", 0.58
    if family == "失败形态":
        return "3", 0.70
    if family == "K线信号":
        if "inside" in key:
            return "9", 0.35
        if "outside" in key:
            return "11", 0.50
        return "12", 0.62
    if family == "交易管理":
        return "12", 0.72
    return "1", 0.50


def stable_offset(pattern_id, window=14):
    digest = hashlib.sha1(pattern_id.encode("utf-8")).hexdigest()
    return int(digest[:6], 16) % max(window, 1)


def choose_pages(pattern, page_count):
    _, position = pick_part_and_position(pattern)
    first_content_page = 4
    usable = max(page_count - first_content_page - 1, 1)
    base = first_content_page + int(usable * position)
    jitter = stable_offset(pattern["id"], 7) - 3
    offsets = [-18, -9, 0, 9, 18]
    pages = []
    for offset in offsets[:EXAMPLES_PER_PATTERN]:
        page_index = min(page_count - 1, max(first_content_page, base + offset + jitter))
        if page_index not in pages:
            pages.append(page_index)
    probe = 1
    while len(pages) < EXAMPLES_PER_PATTERN:
        for direction in (-1, 1):
            page_index = min(page_count - 1, max(first_content_page, base + (probe * 6 * direction) + jitter))
            if page_index not in pages:
                pages.append(page_index)
                if len(pages) >= EXAMPLES_PER_PATTERN:
                    break
        probe += 1
    return pages


def render_page_image(pdf, page_index, dest):
    page = pdf.pages[page_index]
    images = page.images
    if not images:
        return False
    full_page = max(images, key=lambda im: im["width"] * im["height"])
    raw = full_page["stream"].get_data()
    image = Image.open(BytesIO(raw)).convert("RGB")
    image.thumbnail((1080, 680), Image.Resampling.LANCZOS)
    image.save(dest, "JPEG", quality=84, optimize=True)
    return True


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for image in OUT_DIR.glob("*.jpg"):
        image.unlink()
    part_paths = {key: find_pdf(name) for key, name in PART_NAMES.items()}
    patterns = parse_patterns()
    grouped = {}
    for pattern in patterns:
        part_key, _ = pick_part_and_position(pattern)
        grouped.setdefault(part_key, []).append(pattern)

    assets = {}
    for part_key, part_patterns in grouped.items():
        source_path = part_paths[part_key]
        with pdfplumber.open(str(source_path)) as pdf:
            page_count = len(pdf.pages)
            for pattern in part_patterns:
                examples = []
                for example_index, page_index in enumerate(choose_pages(pattern, page_count), 1):
                    filename = f"{pattern['id']}-{example_index:02d}.jpg"
                    dest = OUT_DIR / filename
                    ok = render_page_image(pdf, page_index, dest)
                    if not ok:
                        continue
                    examples.append({
                        "src": f"assets/ab-charts/{filename}",
                        "source": source_path.name,
                        "page": page_index + 1,
                        "caption": f"AB 原图截图：{source_path.name} · page {page_index + 1}",
                    })
                if examples:
                    assets[pattern["id"]] = examples

    OUT_JS.write_text(
        "window.AB_CHART_IMAGES = " + json.dumps(assets, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    total_images = sum(len(examples) for examples in assets.values())
    print(f"generated {total_images} chart screenshots for {len(assets)} patterns")
    print(f"output: {OUT_DIR}")


if __name__ == "__main__":
    main()
