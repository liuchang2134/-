const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const SOURCE_SITE = path.join(ROOT, "price-action-cn-encyclopedia");
const SOURCE_DATA = path.join(SOURCE_SITE, "data.js");
const TARGET = path.join(ROOT, "opening-session-encyclopedia");
const TARGET_ASSETS = path.join(TARGET, "assets", "charts");

const entryOrder = [
  "trend-from-the-open",
  "opening-range",
  "opening-reversal",
  "failed-breakout-yesterday-high-low",
  "opening-gap",
  "first-hour-control",
  "open-of-day",
  "middle-of-day-range",
  "end-of-day-magnet"
];

const guides = {
  "trend-from-the-open": {
    stage: "核心早盘",
    lesson: "趋势开盘",
    priority: 100,
    thesis: "开盘后很快选择方向，并且每一次逆势尝试都缺少跟随，这就是趋势开盘的核心。不要把注意力放在第一根K有多大，而要看后面几根是否继续站在同一方向、回调是否浅、反向信号是否马上失败。",
    readOrder: ["先标昨日高低点和开盘价", "看前5-10根K有没有连续同向实体", "检查第一次回调是浅回调还是深回调", "用开盘区间或第一段推进测量目标"],
    traps: ["只因为第一根K很大就追在极端", "强趋势里不断猜开盘反转", "没有跟随时还按趋势日持仓"],
    chartNotes: [
      "先看开盘后的连续性：真正的趋势日不是一根大K，而是突破后还有第二波、第三波跟随。",
      "回调浅、重叠少、反向信号马上失败，说明被困交易者正在帮顺势方推进。",
      "顺势入场通常等第一次小回调或突破回踩；如果价格回到开盘区间内部，要降低趋势日预期。",
      "目标优先看测量移动、昨日高低点、当日早盘高低点；止损放在早盘结构外，不要贴得太近。"
    ]
  },
  "opening-range": {
    stage: "核心早盘",
    lesson: "开盘区间",
    priority: 98,
    thesis: "开盘区间是早盘最重要的地图。Brooks 反复强调，开盘最初一段震荡不是噪音，它告诉你市场是在形成趋势、交易区间，还是等待假突破后的反向波段。",
    readOrder: ["把前5-20根K圈成开盘区间", "观察突破方向和突破后的跟随", "看回踩是否守住区间边缘", "若突破失败，改按区间边缘交易"],
    traps: ["还没形成区间就急着定义方向", "突破一出现就无条件追", "价格在区间中间还硬做信号K"],
    chartNotes: [
      "开盘区间先定义边界，再谈入场；边界不清楚时，最好的交易常常是等待。",
      "突破后如果立即回到区间，通常说明早盘还没有足够力量展开趋势。",
      "突破有跟随、回踩守住边缘，才更像趋势日或至少第一波顺势波段。",
      "区间中间的信号质量最低，边缘失败突破和回踩确认更值得关注。"
    ]
  },
  "opening-reversal": {
    stage: "关键陷阱",
    lesson: "开盘反转",
    priority: 94,
    thesis: "开盘反转不是看见大阴大阳就反着做，而是看市场是否快速测试了昨日高低点、开盘缺口、开盘价、均线或整数位，并且测试失败。真正的优势来自位置失败加反向跟随。",
    readOrder: ["找开盘测试的关键位", "看测试是否冲过后马上失败", "等待反向信号K和入场K", "目标先看开盘价或开盘区间另一侧"],
    traps: ["强趋势开盘硬做反转", "没有关键位也叫开盘反转", "反向第一根没有跟随后继续幻想大反转"],
    chartNotes: [
      "先问价格在测试什么：昨日高低点、缺口、开盘价或EMA附近的失败，比单根K形状更重要。",
      "反转需要反向跟随；如果只是一根长影线，下一根没有确认，通常还不是好交易。",
      "开盘反转的目标常先看回到开盘价、开盘区间中线或另一侧，而不是一上来期待全天趋势。",
      "如果反转失败并重新突破极端，原来的反转交易理由已经失效。"
    ]
  },
  "failed-breakout-yesterday-high-low": {
    stage: "关键陷阱",
    lesson: "昨日高低点失败",
    priority: 90,
    thesis: "昨日高点和昨日低点是早盘最常见的磁力位。开盘快速突破这些价位后如果没有跟随，回到昨日区间内，往往会触发反向订单和被困交易者止损。",
    readOrder: ["开盘前标出昨日高点和低点", "观察突破后是否收在区间外", "失败回到区间内才考虑反向", "目标先看开盘价、昨日区间中部或另一端"],
    traps: ["看到突破昨日高低点就立即反做", "突破有强跟随时逆势加仓", "忘记把止损放在失败突破极端外"],
    chartNotes: [
      "这类图先看昨日高低点，不先看K线名字；位置决定它是不是值得交易的失败突破。",
      "突破后没有连续收在区间外，反而快速回到昨日区间内，说明突破交易者可能被困。",
      "反向入场要看触发后的跟随，目标通常先保守看开盘价或区间中部。",
      "若突破后形成连续趋势K，就不要把它当失败突破。"
    ]
  },
  "opening-gap": {
    stage: "核心早盘",
    lesson: "开盘跳空",
    priority: 88,
    thesis: "跳空开盘会直接改变早盘磁力结构。关键问题不是缺口一定回补，而是缺口是否被守住、回补尝试是否失败、以及跳空方向有没有形成趋势日。",
    readOrder: ["比较开盘价和昨日收盘/高低点", "判断跳空是否在昨日区间外", "看回补尝试是否有跟随", "缺口守住时按顺势，快速回补时按失败处理"],
    traps: ["跳空后立刻赌回补", "忽略昨日区间边界", "缺口被回补后仍坚持原方向"],
    chartNotes: [
      "跳空开盘先判断缺口相对昨日区间的位置：区间外、区间内、还是卡在关键价位附近。",
      "缺口守住并继续同向推进，说明开盘控制权清楚；此时逆势回补交易风险大。",
      "如果快速回补并回到昨日区间，跳空方向的交易者可能被困，市场容易反向摆动。",
      "跳空日的目标常围绕昨日高低点、开盘价、测量移动和缺口本身。"
    ]
  },
  "first-hour-control": {
    stage: "核心早盘",
    lesson: "第一小时控制权",
    priority: 86,
    thesis: "第一小时不是为了预测全天，而是为了给当天定性：趋势日、区间日、双向波动日。Brooks 的重点是连续性和跟随，不是第一根K决定一切。",
    readOrder: ["记录开盘后第一波方向", "看第二波是否同向跟随", "观察回调深度和重叠程度", "决定用趋势目标还是区间目标"],
    traps: ["第一根K决定全天", "中间位置频繁追单", "已经变成区间还继续用趋势目标"],
    chartNotes: [
      "第一小时要看控制权是否清楚：强势方能否不断把价格推到新高或新低。",
      "如果双向大幅波动、影线多、重叠多，早盘更像交易区间，不适合追中间。",
      "第一小时高低点经常成为后续日内磁力位，后面突破或失败突破都要重新评估。",
      "当第一小时无法给出清晰方向，最重要的动作是缩小目标并等待边缘。"
    ]
  },
  "open-of-day": {
    stage: "磁力与价位",
    lesson: "开盘价磁力",
    priority: 82,
    thesis: "开盘价不是机械买卖点，而是日内控制权参考线。价格反复围绕开盘价上下穿越时，说明市场更接近交易区间；价格长时间站在开盘价一侧时，控制权更清楚。",
    readOrder: ["标出开盘价", "观察价格是在上方、下方还是反复穿越", "结合当日高低点判断磁力", "尾盘再看是否回吸开盘价"],
    traps: ["把开盘价当单独信号", "价格反复穿越还幻想单边趋势", "尾盘时间不够仍追远目标"],
    chartNotes: [
      "开盘价是控制权参考线：在上方停留更久偏多，在下方停留更久偏空，反复穿越偏区间。",
      "测试开盘价失败可以形成短线触发，但必须结合背景和信号K质量。",
      "尾盘价格常被开盘价吸引，尤其当天没有清晰趋势时更明显。",
      "不要只因为价格触碰开盘价就交易；要等失败、突破跟随或边缘结构。"
    ]
  },
  "middle-of-day-range": {
    stage: "日内延伸",
    lesson: "中盘降速",
    priority: 68,
    thesis: "中盘常从早盘冲动变成重叠和等待。它放在早盘专题里，是为了提醒你：早盘判断有效，不代表中盘还可以用同样目标和速度交易。",
    readOrder: ["看早盘趋势是否已经完成测量目标", "观察成交节奏是否变慢", "只在区间边缘找低买高卖", "等待新的强突破再切回趋势思路"],
    traps: ["中盘还用早盘趋势目标", "在区间中间追突破", "忽略成交节奏变慢"],
    chartNotes: [
      "中盘重叠变多，说明早盘动能在降速；这时目标要变小。",
      "区间中间不适合追单，边缘失败突破更有意义。",
      "如果重新出现强突破和跟随，才把市场从中盘区间假设切回趋势假设。",
      "中盘图表的重点是识别降速，而不是强行找早盘同级别机会。"
    ]
  },
  "end-of-day-magnet": {
    stage: "日内延伸",
    lesson: "尾盘磁力",
    priority: 62,
    thesis: "尾盘内容不是早盘交易本身，但它解释了为什么开盘价、当日高低点和第一小时高低点会持续影响全天。越接近收盘，时间本身就是风险。",
    readOrder: ["标开盘价和当日高低点", "看价格离磁力位的距离", "判断剩余时间是否足够", "只做时间允许的目标"],
    traps: ["尾盘还期待远距离目标", "忽略开盘价回吸", "把尾盘小突破当全天新趋势"],
    chartNotes: [
      "尾盘常围绕开盘价、当日高低点、整数位或均线形成磁力。",
      "剩余时间越少，目标越要现实；远距离测量目标通常不再值得追。",
      "如果价格反复靠近开盘价，说明当天多空控制权可能并不彻底。",
      "尾盘的价值在于复盘早盘关键价位如何影响全天，而不是强行开新仓。"
    ]
  }
};

const timeline = [
  { time: "开盘前", title: "先画地图", body: "标出昨日高点、昨日低点、昨日收盘、开盘价、跳空方向、隔夜重要高低点。没有这些价位，早盘信号会失去背景。" },
  { time: "0-5根K", title: "不急着定性", body: "第一根K可以很夸张，但 Brooks 更看重后续跟随。先看第二、第三根是否确认，还是马上回到开盘区间。" },
  { time: "5-20根K", title: "形成开盘区间", body: "圈出早盘初始区间，观察突破、失败突破和回踩。趋势日和区间日通常在这里开始分叉。" },
  { time: "第一小时", title: "判断控制权", body: "连续同向实体、浅回调、反向失败，偏趋势日；影线多、重叠多、双向突破失败，偏交易区间日。" },
  { time: "中盘以后", title: "降速复盘", body: "早盘的高低点、开盘价和测量目标会继续影响全天，但中盘和尾盘目标要缩小，不能拿早盘节奏硬套。"}
];

const courseMap = [
  { id: "48A", title: "Trading the Open A", focus: "开盘框架、昨日关键位、早盘定调", status: "核心必看", weight: 100 },
  { id: "48B", title: "Trading the Open B", focus: "开盘后的强弱转换、信号K有效性", status: "核心必看", weight: 96 },
  { id: "48C", title: "Trading the Open C", focus: "开盘区间、失败突破、早盘反转", status: "核心必看", weight: 94 },
  { id: "48D", title: "Trading the Open D", focus: "开盘模式延伸、交易管理", status: "进阶", weight: 86 },
  { id: "48E", title: "Trading the Open E", focus: "不同开盘背景下的交易计划", status: "进阶", weight: 82 },
  { id: "48F", title: "Trading the Open F", focus: "开盘后确认与放弃条件", status: "进阶", weight: 78 },
  { id: "46", title: "Trading Opening Range Swings", focus: "开盘区间波段与早盘初始区间", status: "专题补充", weight: 88 },
  { id: "BV02", title: "Trading Patterns on the Open", focus: "开盘常见交易模式", status: "奖励课", weight: 84 },
  { id: "BV05", title: "Trading TTR on the Open", focus: "开盘密集交易区间", status: "奖励课", weight: 80 }
];

function loadSourceData() {
  const code = fs.readFileSync(SOURCE_DATA, "utf8");
  const ctx = { window: {} };
  vm.createContext(ctx);
  vm.runInContext(code, ctx);
  return ctx.window.CN_PATTERN_DATA;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function copyChart(chart) {
  const filename = path.basename(chart.src);
  const src = path.join(SOURCE_SITE, chart.src.replace(/\//g, path.sep));
  const dest = path.join(TARGET_ASSETS, filename);
  fs.copyFileSync(src, dest);
  return `assets/charts/${filename}`;
}

function labelCourse(lesson) {
  const title = lesson.title || "";
  const match = title.match(/(48[A-K]|PAF\s?\d+[A-Z]?|HTT\s?\d+[A-Z]?)/i);
  return match ? match[1].replace(/\s+/g, " ") : title;
}

function build() {
  ensureDir(TARGET_ASSETS);
  const source = loadSourceData();
  const byId = new Map(source.patterns.map((item) => [item.id, item]));
  const entries = entryOrder.map((id, index) => {
    const original = byId.get(id);
    if (!original) throw new Error(`Missing pattern: ${id}`);
    const guide = guides[id];
    const lessons = (original.video?.lessons || []).slice(0, 12).map((lesson) => ({
      title: lesson.title,
      language: lesson.language,
      cueCount: lesson.cueCount,
      brief: lesson.brief || lesson.summary || "",
      module: lesson.module || labelCourse(lesson)
    }));
    return {
      id,
      rank: index + 1,
      title: original.title,
      stage: guide.stage,
      lesson: guide.lesson,
      winRate: original.winRate,
      score: original.probScore,
      importance: original.importance,
      difficulty: original.difficulty,
      source: original.source,
      summary: original.summary,
      thesis: guide.thesis,
      readOrder: guide.readOrder,
      traps: guide.traps,
      checklist: original.video?.checklist || [],
      lessons,
      charts: (original.charts || []).map((chart, chartIndex) => ({
        src: copyChart(chart),
        source: chart.source,
        page: chart.page,
        score: chart.score,
        note: guide.chartNotes[chartIndex] || guide.chartNotes[guide.chartNotes.length - 1],
        caption: `${original.title} · 样本 ${chartIndex + 1}`
      }))
    };
  });

  const stageOrder = ["核心早盘", "关键陷阱", "磁力与价位", "日内延伸"];
  const payload = {
    title: "早盘专题图表百科",
    author: "Karthus.Liu",
    generatedAt: new Date().toISOString(),
    source: "本地 Al Brooks 开盘课程、中文课件图表与字幕课总结",
    stats: {
      entries: entries.length,
      charts: entries.reduce((sum, item) => sum + item.charts.length, 0),
      coreCourses: courseMap.length
    },
    stageOrder,
    timeline,
    courses: courseMap,
    glossary: [
      { term: "Opening Range", cn: "开盘区间", body: "开盘后最初一段可识别的高低区间，后续突破或失败突破决定早盘交易计划。" },
      { term: "Trend From the Open", cn: "开盘趋势日", body: "开盘后快速形成单边控制权，回调浅、反向尝试失败、顺势跟随强。" },
      { term: "Opening Reversal", cn: "开盘反转", body: "开盘测试关键价位失败后反向，常见目标是开盘价、开盘区间另一侧或当日磁力位。" },
      { term: "Gap", cn: "跳空/缺口", body: "开盘相对昨日收盘或昨日区间产生距离，是否守住缺口决定早盘方向。" },
      { term: "First Hour", cn: "第一小时", body: "用于判断当天控制权和交易类型，不能只靠第一根K线定性。" }
    ],
    entries
  };

  const out = `window.OPENING_ATLAS_DATA = ${JSON.stringify(payload, null, 2)};\n`;
  fs.writeFileSync(path.join(TARGET, "data.js"), out, "utf8");
  console.log(`Built ${entries.length} entries and ${payload.stats.charts} charts at ${TARGET}`);
}

build();
