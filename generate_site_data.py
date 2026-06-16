import json
import re
from collections import Counter, defaultdict
from pathlib import Path


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
OUT = SITE / "site-data.js"


TOPIC_DEFS = [
    ("术语基础", ["terminology", "术语", "abbreviation", "缩写", "price action", "价格行为", "交易语言"]),
    ("市场周期", ["market cycle", "市场周期", "cycle", "突破", "breakout", "channel", "通道", "trading range", "区间"]),
    ("K线与信号", ["signal bar", "entry bar", "candles", "candlestick", "k线", "信号", "入场k", "收盘", "尾巴"]),
    ("趋势与Always In", ["always in", "trend", "趋势", "strong trend", "ai long", "ai short", "ais", "ail"]),
    ("回调与数K", ["pullback", "bar counting", "high 1", "high 2", "low 1", "low 2", "回调", "数k", "二次入场"]),
    ("支撑阻力/磁力", ["support", "resistance", "magnet", "支撑", "阻力", "磁力", "关键水平", "opening price", "开盘价"]),
    ("突破", ["breakout", "突破", "follow-through", "跟随", "failed breakout", "突破失败"]),
    ("交易区间", ["trading range", "range", "区间", "buy low", "sell high", "买低", "卖高"]),
    ("通道", ["channel", "通道", "tight channel", "broad channel", "趋势线", "通道线"]),
    ("反转/MTR", ["reversal", "mtr", "major trend reversal", "反转", "主要趋势反转", "二次信号"]),
    ("楔形/三推", ["wedge", "楔形", "三推", "three pushes", "第三推"]),
    ("末端旗形/高潮", ["final flag", "climax", "末端旗", "高潮", "exhaustion", "耗尽"]),
    ("测量移动", ["measured move", "测量", "leg 1", "leg 2", "目标", "投射"]),
    ("订单与止损", ["order", "stop", "stop loss", "actual risk", "limit order", "market order", "订单", "止损", "实际风险", "保护止损"]),
    ("交易管理", ["management", "scale", "scalp", "swing", "profit target", "exit", "加仓", "减仓", "止盈", "出场", "波段", "剥头皮"]),
    ("开盘与日内", ["open", "opening", "middle of the day", "end of the day", "开盘", "早盘", "午盘", "尾盘", "日内"]),
    ("交易系统/心理", ["system", "psychology", "personality", "discipline", "mindset", "系统", "心理", "纪律", "执行", "复盘"]),
    ("外汇/品种", ["forex", "currency", "外汇", "点差", "期货", "stock", "股票", "crypto"]),
]


TOPIC_SUMMARY = {
    "术语基础": "建立 Brooks 价格行为语言：用趋势、区间、突破、信号K、概率和交易者方程来描述图表，而不是靠感觉命名形态。",
    "市场周期": "把行情放进突破、通道、交易区间的循环里读；先判断背景，再决定顺势、逆势或等待。",
    "K线与信号": "信号K需要位置、背景和后续入场K确认；单根漂亮K线不能脱离左侧结构使用。",
    "趋势与Always In": "Always In 用来判断当前控制权；强趋势中优先顺势，逆势必须等待结构破坏和二次证据。",
    "回调与数K": "High 1/2、Low 1/2 是趋势回调后的再入场语言，重点是逆势尝试失败后趋势方重新控盘。",
    "支撑阻力/磁力": "关键价位是订单聚集点，不是自动买卖点；要看价格到达后的突破、失败、测试和跟随。",
    "突破": "有效突破需要强K线和跟随；在区间内，很多突破会失败并给反向交易机会。",
    "交易区间": "区间里买低卖高、少在中间交易；边缘的失败突破通常比追突破更有交易者方程优势。",
    "通道": "通道是弱化趋势；紧密通道偏顺势，宽通道更像带方向的区间，边界反应很重要。",
    "反转/MTR": "主要趋势反转不是猜顶底，而是等待趋势线突破、测试失败和二次信号后的结构变化。",
    "楔形/三推": "三推表达动能衰减；第三推在磁力位或通道线附近失败时，常出现两段反向运动。",
    "末端旗形/高潮": "末端旗形和高潮都说明趋势可能过度延伸，但需要失败继续和反向跟随确认。",
    "测量移动": "市场常用前一段运动或区间高度投射目标；测量位是止盈、观望和反向试探的焦点。",
    "订单与止损": "订单类型、初始止损和实际风险决定交易能否执行；看对方向不等于能赚钱。",
    "交易管理": "入场后要按背景决定波段、剥头皮、减仓或保护止损；管理质量常比入场更重要。",
    "开盘与日内": "开盘阶段容易快速定调，也容易假突破；早盘、中盘、尾盘需要不同预期和目标。",
    "交易系统/心理": "把价格行为压缩成少数可重复的 setup、复盘表和统计样本，避免凭情绪切换方法。",
    "外汇/品种": "不同品种的点值、交易时段和波动特征会影响止损、目标和持仓方式。",
}


TOPIC_BULLETS = {
    "术语基础": ["先统一词汇，再看形态。", "每个术语都要落到方向、位置、触发、止损和目标。"],
    "市场周期": ["识别当前处在突破、通道还是区间。", "交易方式必须匹配周期，不能用一种入场打所有行情。"],
    "K线与信号": ["信号K只在合适背景里有意义。", "入场K如果没有跟随，要尽快降低预期。"],
    "趋势与Always In": ["强趋势里第一反转大多只是回调。", "Always In 是控制权判断，不是盲目持仓。"],
    "回调与数K": ["High 2/Low 2 的重点是两段回调失败。", "数K是辅助读行为，不是机械凑形状。"],
    "支撑阻力/磁力": ["关键价位提示注意力，而不是直接给方向。", "到位后的反应比价位本身更重要。"],
    "突破": ["强突破要看后续跟随。", "突破失败后，追单方会变成反向燃料。"],
    "交易区间": ["区间中间少做，边缘等待证据。", "区间里目标要务实，先看中线或另一侧。"],
    "通道": ["紧密通道少逆势，宽通道可看边界反应。", "通道终会变弱，但不能提前猜拐点。"],
    "反转/MTR": ["先有原趋势，再有趋势线突破和测试失败。", "早期MTR胜率不高，靠风险收益补偿。"],
    "楔形/三推": ["三推后看第三推质量和位置。", "楔形常至少带来两段回调，但不保证大反转。"],
    "末端旗形/高潮": ["趋势末端的继续形态失败，才是末端旗形核心。", "高潮后可能先横盘，不一定立刻反转。"],
    "测量移动": ["用Leg 1 = Leg 2或区间高度预估目标。", "测量目标附近要警惕止盈和反向压力。"],
    "订单与止损": ["实际风险可能大于理论止损。", "订单方式要和行情速度匹配。"],
    "交易管理": ["决定这笔是波段还是剥头皮。", "盈利后管理止损，亏损时尊重退出条件。"],
    "开盘与日内": ["开盘要关注昨日高低点、开盘价和快速失败。", "中盘降低趋势预期，尾盘注意磁力位。"],
    "交易系统/心理": ["只选少数setup反复练。", "用复盘表统计，而不是用记忆判断自己会不会。"],
    "外汇/品种": ["品种差异会改变止损距离和交易时段。", "同一形态在不同波动率下需要不同仓位。"],
}


MODULE_LABELS = [
    ("01、【核心视频课】", "核心视频课", "Al Brooks 原声/字幕核心课，是主线。"),
    ("02、课程PPT", "课程PPT", "与核心课配套的图文讲义，用来复习结构和术语。"),
    ("03、阿布交易书籍", "阿布交易书籍", "趋势、区间、反转和逐K阅读的系统书籍。"),
    ("04、阿布图表百科", "阿布图表百科", "大量 Brooks 图表示例，适合学完主线后按形态检索。"),
    ("05", "Louie 课程", "Louie 补充课，用中文化讲解帮助理解 Brooks 体系。"),
    ("06", "Louie 播放列表", "Louie 主题播放列表，适合按概念查漏补缺。"),
    ("07", "Steven 课程", "Steven 中文课，偏交易系统、支撑阻力和案例讲解。"),
    ("08", "老K课程", "老K补充内容，用来辅助理解和建立训练语境。"),
    ("09", "太妃课程", "太妃新版本课程和PPT，适合用作二次讲解。"),
    ("10", "AI翻译版", "AI翻译/英文原版补充，学习路线提示套餐二用户可降低优先级。"),
    ("AL Brooks 53课版", "AL Brooks 53课版", "另一个课程版本，用来对照主线结构。"),
    ("学习资料", "扩展学习资料", "心理、刻意练习、蜡烛图和其他交易书籍。"),
]


EXT_KIND = {
    ".mp4": "视频",
    ".srt": "字幕",
    ".pdf": "PDF",
    ".pptx": "PPT",
    ".ppt": "PPT",
    ".docx": "文档",
    ".epub": "电子书",
    ".xlsx": "表格",
    ".xls": "表格",
    ".csv": "表格",
    ".txt": "文本",
}

TRANS = str.maketrans({"": "-", "": "-", "_": " "})


def read_text(path):
    data = path.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "gb18030", "utf-8"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("utf-8", errors="ignore")


def clean_srt(text):
    lines = []
    cues = 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.isdigit():
            continue
        if "-->" in line:
            cues += 1
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return " ".join(lines), cues


def module_name_from_path(path):
    for part in path.relative_to(ROOT).parts:
        for marker, label, _ in MODULE_LABELS:
            if part.startswith(marker) or marker in part:
                return label
    return "根目录资料"


def module_note(label):
    for _, name, note in MODULE_LABELS:
        if name == label:
            return note
    return "当前文件夹中的补充材料。"


def short_title(path):
    title = path.stem.translate(TRANS)
    title = re.sub(r"\.en$|\.cn$", "", title, flags=re.I)
    title = re.sub(r"\b(?:EN|CN)\b", "", title, flags=re.I)
    title = re.sub(r"DownSub\.com", "", title, flags=re.I)
    title = re.sub(r"\s+-\s+-\s+\d{4}.*$", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"Brooks Trading Course", "", title, flags=re.I).strip(" -")
    title = re.sub(r"BTC\s+", "", title, flags=re.I).strip()
    title = re.sub(r"Video\s+", "", title, flags=re.I).strip()
    return title or path.stem


def detect_language(path, text):
    name = path.name.lower()
    if ".en.srt" in name or "-en.srt" in name:
        return "英文"
    if ".cn.srt" in name or "-cn.srt" in name:
        return "中文"
    sample = text[:8000]
    cn = len(re.findall(r"[\u4e00-\u9fff]", sample))
    en = len(re.findall(r"[A-Za-z]", sample))
    return "中文" if cn >= max(20, en * 0.18) else "英文"


def score_topics(text, title):
    hay = (title + " " + text[:180000]).lower()
    scored = []
    for topic, keys in TOPIC_DEFS:
        score = sum(hay.count(key.lower()) for key in keys)
        if score:
            scored.append((topic, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:4] or [("价格行为总论", 1)]


def summary_for(topics, module):
    main = topics[0]
    base = TOPIC_SUMMARY.get(main, "本课围绕价格行为读图、概率判断和交易执行展开，重点是把图表语言转成可操作规则。")
    if "Steven" in module:
        return f"Steven 中文补充课：{base} 这类内容更适合用来把 Brooks 概念转成自己的交易系统和案例复盘。"
    if "AI翻译" in module:
        return f"AI翻译/原版补充：{base} 学习路线中此模块优先级较低，适合主线学完后对照。"
    if "核心视频课" in module:
        return f"核心课：{base} 本节应作为主线学习材料，先理解概念，再用后面的图解和训练表验证。"
    return f"{module}：{base}"


def practice_for(topics):
    topic = topics[0]
    table = {
        "交易区间": "找10张区间图，只标区间高低点、中线和失败突破，不在区间中间设交易。",
        "趋势与Always In": "找20段趋势，标出Always In方向切换点，并写出切换前后的证据。",
        "反转/MTR": "收集30个MTR候选，只统计是否有趋势线突破、回测失败和二次信号。",
        "突破": "把每次突破分成有跟随和无跟随两类，观察追单方是否被套。",
        "回调与数K": "只练High 2/Low 2或Low 2，记录两段回调是否真的失败。",
        "订单与止损": "每笔模拟交易写下理论止损、实际风险、目标和是否仍满足交易者方程。",
        "开盘与日内": "复盘最近20个交易日开盘30分钟，标出开盘价、昨日高低点和第一次失败突破。",
    }
    return table.get(topic, "把本课只压缩成一个可执行setup：背景、触发、止损、目标、放弃条件各写一句。")


def bullets_for(topics):
    bullets = []
    for topic in topics[:3]:
        bullets.extend(TOPIC_BULLETS.get(topic, []))
    unique = []
    for bullet in bullets:
        if bullet not in unique:
            unique.append(bullet)
    return unique[:5] or ["先判断背景，再看信号。", "每个形态都要转成风险、目标和退出规则。"]


def unit_key(title):
    key = title.lower()
    key = re.sub(r"\b(en|cn|v\d+)\b", "", key)
    key = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", key)
    return re.sub(r"\s+", " ", key).strip()


def build_video_lessons():
    video_lessons = []
    topic_counter = Counter()
    module_counter = Counter()
    language_counter = Counter()
    unique_units = set()

    for idx, path in enumerate(sorted(ROOT.rglob("*.srt"), key=lambda p: str(p).lower()), 1):
        text, cues = clean_srt(read_text(path))
        title = short_title(path)
        language = detect_language(path, text)
        module = module_name_from_path(path)
        scored = score_topics(text, title)
        topics = [topic for topic, _ in scored]
        for topic, score in scored:
            topic_counter[topic] += score
        module_counter[module] += 1
        language_counter[language] += 1
        unique_units.add(unit_key(title))
        word_units = len(re.findall(r"[A-Za-z]+|[\u4e00-\u9fff]", text))
        minutes = max(1, round(cues / 18)) if cues else max(1, round(word_units / 220))
        video_lessons.append({
            "id": idx,
            "title": title,
            "module": module,
            "section": path.parent.name,
            "language": language,
            "topics": topics,
            "topicScores": [{"topic": topic, "score": int(score)} for topic, score in scored],
            "summary": summary_for(topics, module),
            "bullets": bullets_for(topics),
            "practice": practice_for(topics),
            "minutesEstimate": int(minutes),
            "cueCount": int(cues),
            "wordUnits": int(word_units),
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        })

    return video_lessons, topic_counter, module_counter, language_counter, unique_units


def build_materials():
    file_rows = []
    module_stats = defaultdict(lambda: {"files": 0, "bytes": 0, "kinds": Counter(), "samples": []})
    ext_counter = Counter()
    skip_suffixes = {".js", ".css", ".html"}

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if "al-brooks-pattern-dashboard" in path.parts and path.suffix.lower() in skip_suffixes:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        module = module_name_from_path(path)
        ext = path.suffix.lower() or "无扩展名"
        kind = EXT_KIND.get(ext, ext.lstrip(".").upper() or "文件")
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        module_stats[module]["files"] += 1
        module_stats[module]["bytes"] += size
        module_stats[module]["kinds"][kind] += 1
        ext_counter[kind] += 1
        if len(module_stats[module]["samples"]) < 8 and ext in {".pdf", ".docx", ".pptx", ".epub", ".srt"}:
            module_stats[module]["samples"].append({"name": path.name, "kind": kind, "path": rel})
        file_rows.append({"name": path.name, "kind": kind, "module": module, "bytes": size, "path": rel})

    material_modules = []
    for label, stat in module_stats.items():
        material_modules.append({
            "name": label,
            "note": module_note(label),
            "files": int(stat["files"]),
            "sizeGB": round(stat["bytes"] / (1024 ** 3), 2),
            "kinds": [{"kind": kind, "count": int(count)} for kind, count in stat["kinds"].most_common()],
            "samples": stat["samples"],
        })
    material_modules.sort(key=lambda row: row["sizeGB"], reverse=True)
    return file_rows, material_modules, ext_counter


def main():
    video_lessons, topic_counter, module_counter, language_counter, unique_units = build_video_lessons()
    file_rows, material_modules, ext_counter = build_materials()
    source_keys = [
        "学习路线", "学习路径", "10种最佳", "阿布缩写", "How to trade price action manual",
        "AL Brooks 知识体系", "高级趋势", "高级反转", "高级波段", "区间篇", "趋势篇", "反转篇",
        "百科幻灯片2024.4.1", "百科幻灯片-0.pdf", "百科幻灯片-1.pdf",
    ]
    important_sources = sorted(
        [row for row in file_rows if any(key in row["name"] for key in source_keys)],
        key=lambda row: (row["module"], row["name"]),
    )[:80]
    chart_references = sorted(
        [row for row in file_rows if "阿布图表百科" in row["path"] and row["kind"] == "PDF"],
        key=lambda row: row["path"],
    )[:80]
    stats = {
        "subtitleFiles": len(video_lessons),
        "uniqueCourseUnits": len(unique_units),
        "modules": len(material_modules),
        "totalFiles": len(file_rows),
        "totalGB": round(sum(row["bytes"] for row in file_rows) / (1024 ** 3), 2),
        "languages": dict(language_counter),
        "subtitleModules": dict(module_counter),
        "topTopics": [{"topic": topic, "score": int(score)} for topic, score in topic_counter.most_common(18)],
        "fileKinds": [{"kind": kind, "count": int(count)} for kind, count in ext_counter.most_common(12)],
    }
    payload = {
        "stats": stats,
        "videoLessons": video_lessons,
        "materialModules": material_modules,
        "importantSources": important_sources,
        "chartReferences": chart_references,
        "generatedAt": "2026-06-15",
    }
    OUT.write_text("window.SITE_DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
