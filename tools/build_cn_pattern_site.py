#!/usr/bin/env python3
"""Build a standalone Chinese visual encyclopedia from local Al Brooks PDFs.

The generated site lives in price-action-cn-encyclopedia/. It reuses the
existing pattern encyclopedia and subtitle summaries, extends them with
additional Brooks concepts, and renders chart pages from the local Chinese
PDF course/book folder.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF_DIR = Path(r"E:\价格行为学\价格行为学文字资料")
DEFAULT_OUT = ROOT / "price-action-cn-encyclopedia"
TMP_DIR = ROOT / "tmp"
PDF_INDEX_CACHE = TMP_DIR / "cn_pdf_page_index.json"
NODE_EXE = Path(r"C:\Users\liuch\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
PDFTOPPM_EXE = Path(
    r"C:\Users\liuch\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe"
)


FAMILY_TERMS = {
    "突破": ["breakout", "breakouts", "bo", "follow-through", "突破", "跟随", "突破回撤", "breakout pullback"],
    "回调": ["pullback", "pullbacks", "high 2", "low 2", "h2", "l2", "bar counting", "回调", "数K", "二次入场"],
    "交易区间": ["trading range", "range", "tr", "tight trading range", "交易区间", "区间", "买低卖高"],
    "通道": ["channel", "channels", "tight channel", "broad channel", "通道", "微通道"],
    "趋势": ["trend", "trends", "always in", "always-in", "趋势", "总在场内"],
    "反转/MTR": ["major trend reversal", "mtr", "reversal", "反转", "主要趋势反转"],
    "楔形": ["wedge", "wedges", "three pushes", "三推", "楔形"],
    "末端旗形": ["final flag", "final flags", "末端旗形", "最终旗形"],
    "双顶双底": ["double top", "double bottom", "dt", "db", "双顶", "双底"],
    "三角形": ["triangle", "triangles", "三角形", "扩张三角形"],
    "头肩": ["head and shoulders", "头肩"],
    "圆弧": ["rounding", "rounded", "圆弧"],
    "高潮": ["climax", "climaxes", "buy climax", "sell climax", "高潮"],
    "缺口": ["gap", "gaps", "measuring gap", "breakaway gap", "缺口"],
    "开盘": ["open", "opening", "opening range", "开盘", "早盘"],
    "市场周期": ["market cycle", "cycle", "trend", "channel", "trading range", "市场周期", "趋势", "通道", "交易区间"],
    "时间/周期": ["bar count", "bar counting", "open", "middle of day", "end of day", "bar 18", "bar 40", "时间", "K线编号", "早盘", "中盘", "尾盘"],
    "目标/磁力": ["magnet", "measured move", "support", "resistance", "磁力", "测量运动", "支撑", "阻力"],
    "支撑阻力/磁力": ["support", "resistance", "magnet", "test", "prior high", "prior low", "支撑", "阻力", "磁力", "测试", "前高", "前低"],
    "K线信号": ["signal bar", "entry bar", "outside bar", "inside bar", "信号棒", "入场棒", "外包棒", "内包棒"],
    "失败形态": ["failed", "failure", "trap", "失败", "陷阱"],
    "入场逻辑": ["entry", "entries", "order", "stop order", "limit order", "入场", "订单"],
    "订单/执行": ["order", "entry", "stop", "limit", "market order", "订单", "执行", "止损单", "限价单"],
    "交易管理": ["management", "scalp", "swing", "actual risk", "risk", "管理", "风险", "刮头皮"],
    "交易心理": ["psychology", "trapped traders", "discipline", "pain trade", "心理", "被困交易者", "纪律"],
}

GENERIC_TERMS = {
    "high",
    "low",
    "bull",
    "bear",
    "buy",
    "sell",
    "trend",
    "bar",
    "bars",
    "price",
    "action",
    "多头",
    "空头",
    "趋势",
    "做多",
    "做空",
    "价格",
    "行为",
}

SPECIAL_TERMS = {
    "high-2-bull-flag": ["High 2", "H2", "高点 2", "高 2", "二次入场", "两段回调"],
    "low-2-bear-flag": ["Low 2", "L2", "低点 2", "低 2", "二次入场", "两段回调"],
    "high-1-low-1": ["High 1", "Low 1", "H1", "L1", "高点 1", "低点 1"],
    "high-3-low-3": ["High 3", "Low 3", "H3", "L3", "高点 3", "低点 3"],
    "two-legged-pullback-to-ema": ["two legged pullback", "TBTL", "EMA", "两段回调", "均线"],
    "major-trend-reversal-top": ["Major Trend Reversal", "MTR Top", "LH MTR", "主要趋势反转"],
    "major-trend-reversal-bottom": ["Major Trend Reversal", "MTR Bottom", "HL MTR", "主要趋势反转"],
    "wedge-bull-flag": ["Wedge Bull Flag", "楔形多头旗形", "三推回调"],
    "wedge-bear-flag": ["Wedge Bear Flag", "楔形空头旗形", "三推回调"],
}


EXTRA_CONCEPTS = [
    {
        "id": "bar-count",
        "title": "Bar Count 日内K线编号",
        "family": "时间/周期",
        "aliases": ["K线编号", "Bar 18", "Bar 40", "Bar 48", "Bar 70"],
        "source": "PAF 09 Pullbacks and Bar Counting / PAF 47-48 Intraday Timing",
        "summary": "把日内5分钟K线按开盘后顺序编号，用来判断早盘、中盘、尾盘和高周期收盘的时间压力。",
        "terms": ["bar count", "bar counting", "high 1, 2, 3", "low 1, 2, 3", "K线编号", "开盘"],
        "best": ["5分钟日内图", "需要判断当前处在早盘、中盘还是尾盘", "结合开盘价、昨日高低点和EMA"],
        "entry": ["不直接入场，只用来给setup定时间背景", "在关键bar附近等待价格行为确认"],
        "stop": ["按对应形态止损，不按bar编号止损"],
        "target": ["结合日内剩余时间决定波段或小目标"],
        "traps": ["把第18根或第40根当机械反转信号", "忽略当天市场周期"]
    },
    {
        "id": "h4-l4",
        "title": "High 4 / Low 4",
        "family": "回调",
        "aliases": ["H4", "L4", "第四次入场", "复杂回调"],
        "source": "PAF 09 Pullbacks and Bar Counting",
        "summary": "H4/L4通常说明回调已经复杂化，可能不再是简单旗形，而是交易区间或反转过程。",
        "terms": ["High 4", "Low 4", "H4", "L4", "bar counting", "fourth entry"],
        "best": ["强趋势后的复杂回调", "回调仍未破坏大方向", "等待更强信号K"],
        "entry": ["只在背景仍然顺势时考虑第四次触发", "更常等待突破失败或二次确认"],
        "stop": ["复杂回调结构外"],
        "target": ["先看原趋势极点测试"],
        "traps": ["机械数到4就入场", "趋势已经变成交易区间仍按顺势旗形处理"]
    },
    {
        "id": "ii-pattern",
        "title": "II 连续内包K",
        "family": "K线信号",
        "aliases": ["Inside Inside", "II", "连续内包", "小三角形"],
        "source": "PAF 04 Bar Basics / PAF 12 Chart Patterns",
        "summary": "连续内包K代表波动压缩，小周期上常像小三角形，真正的含义取决于出现位置和突破后的跟随。",
        "terms": ["inside inside", "II", "inside bar", "内包", "连续内包", "small triangle"],
        "best": ["趋势中的短暂停顿", "关键价位附近的收缩", "突破后有强入场K"],
        "entry": ["突破母K高低点后再判断", "顺大背景方向优先"],
        "stop": ["母K另一侧或信号结构外"],
        "target": ["突破测量目标或最近磁力位"],
        "traps": ["交易区间中段的II", "突破后立刻回到母K内"]
    },
    {
        "id": "oo-pattern",
        "title": "OO 连续外包K",
        "family": "K线信号",
        "aliases": ["Outside Outside", "OO", "连续外包", "扩大三角形"],
        "source": "PAF 04 Bar Basics / PAF 12 Chart Patterns",
        "summary": "连续外包K代表双向扫单和波动扩张，小周期上常像扩大三角形，容易形成陷阱。",
        "terms": ["outside outside", "OO", "outside bar", "外包", "连续外包", "expanding triangle"],
        "best": ["极端位置的二次失败", "大波动后等待方向收敛", "结合通道线或区间边缘"],
        "entry": ["等一方失败后反向跟随", "新手更适合等待下一次清晰信号"],
        "stop": ["外包结构另一侧"],
        "target": ["区间中线或另一侧边缘"],
        "traps": ["在OO内部追突破", "把混乱当成强趋势"]
    },
    {
        "id": "ioi-pattern",
        "title": "IOI 内外内形态",
        "family": "K线信号",
        "aliases": ["Inside Outside Inside", "IOI", "突破模式", "末端旗形候选"],
        "source": "PAF 04 Bar Basics / PAF 12 Chart Patterns",
        "summary": "IOI是收缩、扩张、再收缩的组合，可作突破模式，也可能是趋势末端旗形。",
        "terms": ["IOI", "inside outside inside", "内外内", "breakout mode", "final flag"],
        "best": ["关键位附近", "趋势中途整理", "突破后有跟随"],
        "entry": ["突破IOI结构后顺势", "失败突破后反向"],
        "stop": ["IOI结构另一侧"],
        "target": ["测量移动或最近磁力位"],
        "traps": ["只看到IOI就交易", "忽略位置和市场周期"]
    },
    {
        "id": "tbt-l-correction",
        "title": "TBTL 十根K两段回调",
        "family": "回调",
        "aliases": ["Ten Bars Two Legs", "TBTL", "十根K两波", "两段修正"],
        "source": "PAF 09 Pullbacks / PAF 13 Always In",
        "summary": "Brooks常用TBTL描述趋势后的典型修正：至少约十根K、两段运动，之后才更适合评估原趋势是否恢复。",
        "terms": ["TBTL", "Ten Bars", "Two Legs", "十根", "两段", "correction"],
        "best": ["强趋势后的第一轮修正", "等待逆势方两次尝试失败"],
        "entry": ["第二段结束后看信号K和跟随", "顺原趋势优先"],
        "stop": ["修正结构外"],
        "target": ["原趋势极点测试或测量目标"],
        "traps": ["第一根反转K就逆势", "修正未完成就提前重仓"]
    },
    {
        "id": "moving-average-gap-bar",
        "title": "均线缺口K / Moving Average Gap Bar",
        "family": "目标/磁力",
        "aliases": ["MAG", "MA Gap Bar", "20 Gap Bar", "均线缺口棒"],
        "source": "PAF 19 Support and Resistance / PAF 25 Measured Moves",
        "summary": "K线与20EMA之间出现空隙，说明趋势推进较强；第一次均线缺口后的回测常成为趋势极点测试背景。",
        "terms": ["moving average gap", "MA gap bar", "gap bar", "20 gap bar", "均线缺口", "缺口棒"],
        "best": ["强趋势中第一次脱离均线", "回调后仍未破坏趋势结构"],
        "entry": ["回调结束后顺趋势", "看信号K和入场K"],
        "stop": ["回调结构外或信号K另一侧"],
        "target": ["测试趋势极点"],
        "traps": ["趋势已经高潮仍追", "把均线缺口当反转信号"]
    },
    {
        "id": "first-pullback-sequence",
        "title": "第一回撤序列",
        "family": "回调",
        "aliases": ["First Pullback", "First Pullback Sequence", "第一次回调"],
        "source": "Trading Price Action Trading Ranges / PAF 09 Pullbacks",
        "summary": "强趋势或突破后的第一次回撤通常最重要，顺势交易者会在不同层级寻找再次入场。",
        "terms": ["first pullback", "first pullback sequence", "第一次回撤", "first PB"],
        "best": ["强突破后第一次回调", "回调浅且反向K弱"],
        "entry": ["信号K高低点触发", "突破回踩成功后入场"],
        "stop": ["回调结构外"],
        "target": ["前高前低或测量目标"],
        "traps": ["无跟随突破后硬等回调", "第一次回调已经变成深回调"]
    },
    {
        "id": "opening-range",
        "title": "Opening Range 开盘区间",
        "family": "开盘",
        "aliases": ["开盘区间", "早盘区间", "OR"],
        "source": "PAF 46 Trading Opening Range Swings",
        "summary": "开盘后最初一段区间决定当天早期控制权，突破、失败突破和回踩会给出趋势日或区间日线索。",
        "terms": ["opening range", "open range", "开盘区间", "opening range swings"],
        "best": ["开盘前1小时", "结合昨日高低点和开盘价", "等待强突破或失败突破"],
        "entry": ["开盘区间突破后看跟随", "失败突破后反向"],
        "stop": ["开盘区间另一侧或信号K外"],
        "target": ["日内测量移动或昨日关键位"],
        "traps": ["开盘几根K里追在极端", "忽略昨日高低点"]
    },
    {
        "id": "open-of-day",
        "title": "Open of Day 开盘价磁力",
        "family": "开盘",
        "aliases": ["OOD", "开盘价", "日开盘价"],
        "source": "PAF 46-48 Intraday Trading",
        "summary": "开盘价是重要磁力位，日内价格经常围绕它判断多空控制权，尤其在区间日和尾盘更明显。",
        "terms": ["open of day", "OOD", "opening price", "开盘价"],
        "best": ["价格反复测试开盘价", "开盘价与昨日高低点重合", "尾盘回到开盘价附近"],
        "entry": ["等待测试失败或突破跟随"],
        "stop": ["测试结构另一侧"],
        "target": ["当日高低点或收盘磁力"],
        "traps": ["把开盘价当单独买卖点", "没有信号K就提前下注"]
    },
    {
        "id": "pain-trade",
        "title": "Pain Trade 痛苦交易",
        "family": "交易心理",
        "aliases": ["痛苦交易", "Trade what you see", "价格即真相"],
        "source": "PAF 37 How to Trade Price Action",
        "summary": "市场经常走出让多数人不愿相信的行情；Brooks强调交易看到的图，而不是自己希望看到的图。",
        "terms": ["pain trade", "trade what you see", "believe the chart", "价格即是真相", "痛苦交易"],
        "best": ["走势明显违背大众预期", "连续强K迫使反向交易者止损"],
        "entry": ["顺着已经证明控制权的一方", "等回调或小信号降低风险"],
        "stop": ["控制权被破坏的位置"],
        "target": ["被困交易者止损推动的测量移动"],
        "traps": ["因为觉得不可能而逆势", "用希望替代图表证据"]
    },
    {
        "id": "value-trader",
        "title": "Value Trader 价值交易者",
        "family": "交易区间",
        "aliases": ["价值交易者", "Buy Low Sell High", "BLSHS"],
        "source": "PAF 13 Trading Ranges / PAF 45 Trading in Trading Ranges",
        "summary": "交易区间里的交易者寻找价值：低买高卖、小目标、重视边缘位置，不轻信运动会走很远。",
        "terms": ["value trader", "BLSHS", "buy low sell high", "价值交易者", "低买高卖"],
        "best": ["明确交易区间", "接近区间高低点", "有失败突破或反转信号"],
        "entry": ["区间低买、区间高卖", "用限价单或信号K"],
        "stop": ["区间边缘外"],
        "target": ["区间中线或另一侧"],
        "traps": ["在区间中间追单", "把区间运动当趋势波段"]
    },
    {
        "id": "limit-order-market",
        "title": "限价单市场",
        "family": "入场逻辑",
        "aliases": ["Limit Order Market", "限价单", "区间挂单"],
        "source": "PAF 28 Orders / PAF 45 Trading Ranges",
        "summary": "当市场更像交易区间时，限价单交易者常能在高卖低买中获利；止损单追突破反而容易被套。",
        "terms": ["limit order", "limit order market", "限价单", "订单", "trading range"],
        "best": ["重叠K线多", "上下都有尾线", "突破缺少跟随"],
        "entry": ["在区间边缘用限价或等待信号K"],
        "stop": ["边缘外或失败结构外"],
        "target": ["小目标、区间中线、另一侧"],
        "traps": ["强趋势里逆势限价加仓", "没有足够资金和计划就摊位"]
    },
    {
        "id": "stop-order-market",
        "title": "止损单市场",
        "family": "入场逻辑",
        "aliases": ["Stop Order Market", "止损单入场", "突破市场"],
        "source": "PAF 28 Orders / PAF 38-39 Strong Breakouts",
        "summary": "强突破和强趋势中，止损单交易者顺动能入场，市场往往不给便宜回调。",
        "terms": ["stop order", "stop entry", "止损单", "buy stop", "sell stop", "breakout"],
        "best": ["强趋势日", "连续强趋势K", "突破后小回调或无回调"],
        "entry": ["突破高低点用止损单", "回调结束后顺势触发"],
        "stop": ["突破K另一侧或最近结构外"],
        "target": ["测量目标或波段持有"],
        "traps": ["交易区间中间追突破", "入场后无跟随仍死扛"]
    },
    {
        "id": "always-in-long",
        "title": "Always In Long 始终看多",
        "family": "趋势",
        "aliases": ["AIL", "总在场内多头", "Always In Long"],
        "source": "PAF 13 Always In / PAF 37 How to Trade",
        "summary": "如果必须一直在场内，当前应持多头；它是市场控制权判断，不是盲目持仓。",
        "terms": ["Always In Long", "AIL", "始终看涨", "总在场内多头"],
        "best": ["连续多头跟随", "回调浅", "空头反转尝试失败"],
        "entry": ["回调或突破后顺多头方向", "强趋势中优先做多"],
        "stop": ["多头结构被破坏处"],
        "target": ["前高、测量移动、通道线"],
        "traps": ["已经进入交易区间仍认为必须做多", "第一根强阴线后不重新评估"]
    },
    {
        "id": "always-in-short",
        "title": "Always In Short 始终看空",
        "family": "趋势",
        "aliases": ["AIS", "总在场内空头", "Always In Short"],
        "source": "PAF 13 Always In / PAF 37 How to Trade",
        "summary": "如果必须一直在场内，当前应持空头；强空头环境里，多头反转大多先按回调看。",
        "terms": ["Always In Short", "AIS", "始终看跌", "总在场内空头"],
        "best": ["连续空头跟随", "反弹弱", "多头反转尝试失败"],
        "entry": ["反弹结束后顺空头方向", "强趋势中优先做空"],
        "stop": ["空头结构被破坏处"],
        "target": ["前低、测量移动、通道线"],
        "traps": ["高潮末端继续追空", "忽略强多头突破"]
    },
    {
        "id": "spike-and-range",
        "title": "尖刺 + 交易区间",
        "family": "交易区间",
        "aliases": ["Spike and Range", "尖刺后区间", "趋势后区间"],
        "source": "PAF 06 Market Cycle / PAF 13 Trading Ranges",
        "summary": "强尖刺后市场不一定继续趋势，常转入交易区间；区间内要降低目标而不是继续追尖刺。",
        "terms": ["spike and range", "尖刺", "交易区间", "trend to trading range"],
        "best": ["强突破后跟随减弱", "价格围绕均线上下震荡"],
        "entry": ["区间边缘交易或等待二次突破"],
        "stop": ["区间边缘外"],
        "target": ["区间中线或另一侧"],
        "traps": ["尖刺后继续按强趋势追单", "忽略区间中间风险"]
    },
    {
        "id": "trendline-break",
        "title": "趋势线突破",
        "family": "反转/MTR",
        "aliases": ["Trendline Break", "突破趋势线", "趋势线被破"],
        "source": "PAF 16 Reversals / PAF 17 Major Trend Reversals",
        "summary": "趋势线突破通常只是反转过程的第一步，后面还要看测试原极端是否失败。",
        "terms": ["trendline break", "break below trend line", "break above trend line", "趋势线突破"],
        "best": ["趋势持续较久后出现强反向突破", "突破后有足够距离和跟随"],
        "entry": ["等待回测原高低点失败或二次信号"],
        "stop": ["测试极端外"],
        "target": ["两段反向运动或测量目标"],
        "traps": ["趋势线一破就当大反转", "没有二次证据就逆势重仓"]
    },
    {
        "id": "second-leg-trap",
        "title": "第二腿陷阱",
        "family": "失败形态",
        "aliases": ["Second Leg Trap", "第二波陷阱", "二腿失败"],
        "source": "PAF 09 Pullbacks / PAF 37 How to Trade",
        "summary": "交易者常期待第二腿延续，但如果第二腿没有跟随并快速反向，会形成被困交易者燃料。",
        "terms": ["second leg", "trap", "2nd leg", "第二腿", "第二波", "陷阱"],
        "best": ["二次尝试到关键位失败", "第二腿变弱", "反向信号强"],
        "entry": ["失败确认后反向", "等待反向跟随"],
        "stop": ["失败尝试极端外"],
        "target": ["区间另一侧或测量移动"],
        "traps": ["把任何第二腿都当确定延续", "没有反向跟随就做反向"]
    },
    {
        "id": "failed-high-2",
        "title": "失败 High 2",
        "family": "失败形态",
        "aliases": ["Failed H2", "H2 Failure", "高2失败"],
        "source": "PAF 09 Pullbacks / PAF 37 Failures",
        "summary": "H2在错误背景下失败时，做多者被困，常推动反向下跌。",
        "terms": ["failed high 2", "failed H2", "H2 failure", "High 2 failure", "高2失败"],
        "best": ["交易区间高位", "趋势已经破坏", "H2触发后没有跟随"],
        "entry": ["H2失败后反向做空", "等跌破信号K或回到区间内"],
        "stop": ["H2高点外"],
        "target": ["区间中线、低点或测量目标"],
        "traps": ["只因为数到H2就买", "忽略左侧卖压"]
    },
    {
        "id": "failed-low-2",
        "title": "失败 Low 2",
        "family": "失败形态",
        "aliases": ["Failed L2", "L2 Failure", "低2失败"],
        "source": "PAF 09 Pullbacks / PAF 37 Failures",
        "summary": "L2在错误背景下失败时，做空者被困，常推动反向上涨。",
        "terms": ["failed low 2", "failed L2", "L2 failure", "Low 2 failure", "低2失败"],
        "best": ["交易区间低位", "空头趋势被破坏", "L2触发后没有跟随"],
        "entry": ["L2失败后反向做多", "等突破信号K或回到区间内"],
        "stop": ["L2低点外"],
        "target": ["区间中线、高点或测量目标"],
        "traps": ["只因为数到L2就卖", "忽略左侧买压"]
    }
]


def _cx(
    item_id: str,
    title: str,
    family: str,
    source: str,
    summary: str,
    terms: list[str],
    best: list[str],
    entry: list[str],
    stop: list[str],
    target: list[str],
    traps: list[str],
    aliases: list[str] | None = None,
    prob_score: int = 50,
    importance: int = 82,
    difficulty: int = 3,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "title": title,
        "family": family,
        "aliases": aliases or [],
        "source": source,
        "summary": summary,
        "terms": terms,
        "best": best,
        "entry": entry,
        "stop": stop,
        "target": target,
        "traps": traps,
        "probScore": prob_score,
        "importance": importance,
        "difficulty": difficulty,
    }


EXTRA_CONCEPTS.extend(
    [
        _cx(
            "market-cycle",
            "市场周期：突破 → 通道 → 交易区间",
            "市场周期",
            "PAF 12 Market Cycle / PAF 14-18",
            "Brooks 的主线不是背形态，而是判断市场正处在突破、通道还是交易区间；形态只有放进周期里才有交易意义。",
            ["market cycle", "breakout channel trading range", "市场周期", "突破", "通道", "交易区间"],
            ["先判断当前结构属于哪一段", "看最近一次突破是否仍有跟随", "把区间中段和趋势中段区别开"],
            ["趋势段顺势，区间边缘反向，中间少交易", "周期转换处等待二次证据"],
            ["按当前结构外侧，而不是按主观看法"],
            ["突破测量、通道线、区间另一侧"],
            ["把所有图都当趋势", "把所有震荡都当反转"],
            ["Market Cycle"],
            54,
            99,
            4,
        ),
        _cx(
            "buying-selling-pressure",
            "买压 / 卖压",
            "K线信号",
            "PAF 10 Buying and Selling Pressure",
            "买压和卖压来自K线实体、收盘位置、尾线、连续性和是否能突破前一根K；它决定信号有没有后劲。",
            ["buying pressure", "selling pressure", "买压", "卖压", "pressure"],
            ["连续同向实体", "收盘靠近高低点", "回调K缺少反向实体"],
            ["等压力方向出现触发，而不是只看单根K颜色"],
            ["压力被明显反向K破坏处"],
            ["最近高低点、测量移动或磁力位"],
            ["把一根大K当成全部证据", "忽略下一根入场K是否失败"],
            ["Pressure"],
            55,
            97,
            4,
        ),
        _cx(
            "signal-bar-context",
            "信号K：位置比形状重要",
            "K线信号",
            "PAF 08 Candles Setups and Signal Bars",
            "Brooks 反复强调：漂亮信号K如果出现在错误位置，只是漂亮的陷阱；位置、背景、触发和跟随要一起看。",
            ["signal bar", "setup", "信号K", "信号棒", "candles"],
            ["位于趋势回调末端、区间边缘或关键价位", "信号K方向符合背景", "下一根入场K有跟随"],
            ["突破信号K高低点后入场", "更保守时等入场K收盘确认"],
            ["信号K另一侧或结构外"],
            ["最近磁力位或测量目标"],
            ["只背K线形状", "信号K很大导致风险过宽仍追"],
            ["Signal Bar", "Setup Bar"],
            52,
            96,
            3,
        ),
        _cx(
            "entry-bar-follow-through",
            "入场K与跟随",
            "K线信号",
            "PAF 08 Candles / PAF 15 Breakouts",
            "入场K告诉你市场是否接受这个交易方向；如果触发后没有跟随，原来的信号很快会变成失败信号。",
            ["entry bar", "follow-through", "入场K", "跟随", "entry"],
            ["触发后立即出现同向实体", "入场K收盘不差", "没有快速回到信号K内部"],
            ["入场K质量好可持有，质量差先降低目标"],
            ["入场K另一侧或信号K另一侧"],
            ["前高前低、测量移动、通道线"],
            ["触发就当成功", "忽略入场K收盘很差"],
            ["Entry Bar", "Follow Through"],
            55,
            96,
            3,
        ),
        _cx(
            "strong-trend-bar",
            "强趋势K",
            "K线信号",
            "PAF 08 / PAF 15 Breakouts",
            "强趋势K用实体、收盘位置和突破力度显示控制权。它不是单独信号，而是市场愿意接受新价格的证据。",
            ["trend bar", "strong trend bar", "big bar", "趋势K", "强K"],
            ["实体大、尾线小", "收盘靠近极端", "突破关键位并有跟随"],
            ["顺实体方向等待触发或回调", "大K后避免在最差价格追太大仓位"],
            ["大K另一侧通常太宽，优先等小结构"],
            ["测量移动或下一磁力位"],
            ["把高潮大K当低风险入场", "忽略大K后第2根是否失去跟随"],
            ["Trend Bar"],
            56,
            93,
            3,
        ),
        _cx(
            "weak-signal-bar",
            "弱信号K",
            "K线信号",
            "PAF 08 Candles Setups and Signal Bars",
            "弱信号K不是不能交易，而是必须有更好的背景或更好的入场K补强；在区间中段尤其容易失败。",
            ["weak signal bar", "bad signal bar", "弱信号", "信号K"],
            ["背景很强，信号K只是回调末端", "出现在区间边缘而非中间"],
            ["等下一根确认或用小仓位", "不在风险过宽时追"],
            ["弱信号结构外"],
            ["保守小目标或最近磁力位"],
            ["把弱信号按强信号处理", "看不懂就强行交易"],
            ["Weak Signal"],
            45,
            86,
            3,
        ),
        _cx(
            "inside-bar",
            "内包K",
            "K线信号",
            "PAF 08 Candles / PAF 12 Chart Patterns",
            "内包K代表短暂压缩，常是突破模式的一部分；方向必须由背景和突破后的跟随决定。",
            ["inside bar", "inside bars", "内包K", "inside"],
            ["趋势中短暂停顿", "关键位附近波动收缩", "突破后有跟随"],
            ["突破母K高低点后再判断", "顺背景方向优先"],
            ["母K另一侧"],
            ["测量目标或最近磁力位"],
            ["区间中间两边追", "把内包当必然爆发"],
            ["Inside Bar"],
            49,
            88,
            2,
        ),
        _cx(
            "outside-bar",
            "外包K",
            "K线信号",
            "PAF 08 Candles / PAF 12 Chart Patterns",
            "外包K说明双方都被扫过，既可能是强反转，也可能只是区间里的噪音；下一根K是否延续非常关键。",
            ["outside bar", "outside bars", "外包K", "outside"],
            ["极端位置", "突破失败后反向收盘强", "下一根继续跟随"],
            ["外包K方向明确后顺势", "不清楚时等第二根确认"],
            ["外包K另一侧"],
            ["区间另一边或测量移动"],
            ["在中段把外包当突破", "上下都被扫后情绪化追单"],
            ["Outside Bar"],
            48,
            87,
            3,
        ),
        _cx(
            "doji-neutral-bars",
            "十字K与中性K",
            "K线信号",
            "PAF 08 Candles Setups and Signal Bars",
            "十字K通常表示短期分歧或暂停，只有在特殊位置才有交易价值；它本身不等于反转。",
            ["doji", "neutral bar", "十字K", "中性K", "small bar"],
            ["强趋势后的短暂停顿", "区间边缘等待二次信号", "下一根给方向"],
            ["等突破十字K后有跟随", "不把十字K本身当方向"],
            ["小结构另一侧"],
            ["小目标或最近磁力位"],
            ["看见十字就猜反转", "在中段过度交易"],
            ["Doji"],
            42,
            80,
            2,
        ),
        _cx(
            "tails-and-overlap",
            "影线与重叠",
            "K线信号",
            "PAF 02 Chart Basics / PAF 10 Pressure",
            "影线和重叠告诉你市场是否缺少持续性；影线越多、重叠越多，越像交易区间思维。",
            ["tails", "overlap", "wicks", "影线", "重叠"],
            ["用来判断趋势是否变弱", "区间内寻找边缘交易", "突破后观察影线是否减少"],
            ["影线减少且实体连续时顺势", "影线密集时降低目标"],
            ["结构外"],
            ["小目标、区间中线或另一侧"],
            ["在影线密集处期待大趋势", "忽略收盘质量"],
            ["Tails", "Overlap"],
            45,
            90,
            2,
        ),
        _cx(
            "micro-gap",
            "微缺口",
            "缺口",
            "PAF 11 Gaps / PAF 14 Trends",
            "微缺口常显示趋势中的持续买压或卖压，尤其连续出现时，逆势交易需要非常谨慎。",
            ["micro gap", "micro gaps", "微缺口", "gap"],
            ["连续趋势K之间留出小空隙", "回调无法完全填补", "与EMA同向分离"],
            ["顺趋势方向等待小回调", "逆势只等失败突破或MTR"],
            ["最近微结构外"],
            ["通道线、前高前低、测量移动"],
            ["把微缺口当必填缺口", "逆势抢第一根反转"],
            ["Micro Gap"],
            57,
            91,
            3,
        ),
        _cx(
            "breakaway-gap",
            "突破缺口",
            "缺口",
            "PAF 11 Gaps / PAF 15 Breakouts",
            "突破缺口说明价格离开旧价值区，重点看缺口是否保持开放，以及回测时是否被买入或卖出。",
            ["breakaway gap", "gap breakout", "突破缺口", "breakout gap"],
            ["离开交易区间或关键位", "缺口不被快速填补", "有连续跟随K"],
            ["顺突破方向，或等缺口回测成功"],
            ["缺口另一侧或突破结构外"],
            ["测量移动、前方磁力位"],
            ["缺口开出后立刻逆势填补", "缺口被快速关闭仍顺势死扛"],
            ["Breakaway Gap"],
            61,
            90,
            3,
        ),
        _cx(
            "exhaustion-gap",
            "衰竭缺口",
            "缺口",
            "PAF 11 Gaps / PAF 29 Climaxes",
            "趋势末端的缺口如果缺少后续跟随，可能代表最后一批追单者入场，随后进入回调或反转。",
            ["exhaustion gap", "climax gap", "衰竭缺口", "高潮缺口"],
            ["趋势已经走远", "缺口后无法继续", "出现反向强K或失败突破"],
            ["等失败确认后反向或观望", "不要抢第一根反转"],
            ["末端极点外"],
            ["EMA、前波起点、交易区间中线"],
            ["只因为走远就逆势", "缺口仍强时提前做反向"],
            ["Exhaustion Gap"],
            50,
            88,
            4,
        ),
        _cx(
            "support-resistance-test",
            "支撑阻力测试",
            "支撑阻力/磁力",
            "PAF 19 Support and Resistance",
            "支撑阻力不是自动买卖点，而是订单密集区域；到达后要看突破、测试失败、二次尝试和跟随。",
            ["support", "resistance", "test", "支撑", "阻力", "测试"],
            ["前高前低、趋势线、通道线、EMA、整数位", "第一次测试后看反应", "第二次测试更有信息"],
            ["测试失败后反向，强突破后顺势", "不要在关键位前随意入场"],
            ["测试极点外"],
            ["下一个磁力位或区间另一侧"],
            ["把线当墙", "忽略到达后的K线质量"],
            ["S/R Test"],
            54,
            98,
            3,
        ),
        _cx(
            "prior-high-low",
            "前高 / 前低磁力",
            "支撑阻力/磁力",
            "PAF 19 Support and Resistance / HTT 48 Open",
            "前高前低是市场最常回看的位置，突破、未达、刺破失败都会暴露多空控制权。",
            ["prior high", "prior low", "前高", "前低", "yesterday high", "yesterday low"],
            ["接近昨日高低点或重要摆动点", "速度开始变化", "突破后是否立刻回到范围内"],
            ["突破成功顺势，失败突破反向", "靠近磁力位前降低不必要目标"],
            ["磁力位外侧或失败结构外"],
            ["前高前低、开盘价、测量移动"],
            ["价格差一点到位就急着反向", "假突破后还相信原突破"],
            ["Prior H/L"],
            53,
            95,
            3,
        ),
        _cx(
            "round-number-magnet",
            "整数位磁力",
            "支撑阻力/磁力",
            "PAF 19 Support and Resistance",
            "整数位常聚集止损单、获利单和算法订单；它的作用是吸引价格，交易方向仍由到达后的行为决定。",
            ["round number", "big round number", "整数位", "磁力"],
            ["接近整百、整千或品种常用整数", "价格反复回到该区域", "与前高前低重合"],
            ["等待测试、突破或失败突破", "不在整数位附近盲目挂单"],
            ["测试结构外"],
            ["下一磁力位"],
            ["认为整数位必然反转", "忽略趋势强度"],
            ["Round Number"],
            47,
            84,
            2,
        ),
        _cx(
            "measured-move-projection",
            "测量运动投射",
            "目标/磁力",
            "PAF 20 Measured Moves / PAF 25",
            "测量运动把已发生的腿、区间高度或突破幅度投射到未来目标；它是目标和磁力，不是入场理由。",
            ["measured move", "MM", "测量运动", "投射", "measuring"],
            ["有清晰第一腿或区间高度", "突破后保持跟随", "目标与其他磁力重合"],
            ["入场来自形态，测量运动只定目标", "接近目标时管理仓位"],
            ["形态结构外"],
            ["1倍测量、2倍测量、对称腿"],
            ["把目标当保证", "忽略达到目标前的失败信号"],
            ["Measured Move"],
            54,
            94,
            3,
        ),
        _cx(
            "ema-20-magnet",
            "20 EMA 磁力",
            "目标/磁力",
            "PAF 19 Support and Resistance / PAF 14 Trends",
            "20 EMA 是 Brooks 体系里最常用的动态磁力。强趋势中回调不深，交易区间里价格会反复穿越它。",
            ["20 EMA", "EMA", "moving average", "均线", "指数均线"],
            ["趋势中第一次回踩EMA", "价格与均线分离过远", "均线斜率配合趋势方向"],
            ["强趋势中顺EMA方向，区间里不把EMA当强支撑阻力"],
            ["回调结构外"],
            ["前高前低、通道线或测量移动"],
            ["每次碰EMA都入场", "忽略均线已经变平"],
            ["20 EMA"],
            56,
            96,
            3,
        ),
        _cx(
            "channel-line-overshoot",
            "通道线过冲",
            "通道",
            "PAF 16 Channels / PAF 24 Wedges",
            "价格冲出通道线后如果没有跟随，常说明趋势进入高潮或过度延伸，随后可能回到通道或进入两段回调。",
            ["channel line overshoot", "overshoot", "通道线过冲", "过冲"],
            ["趋势已经持续一段", "第三推或高潮附近", "过冲后收盘变差"],
            ["等失败确认或二次信号", "顺势者靠近过冲处减仓"],
            ["过冲极点外"],
            ["EMA、通道中线、前一摆动点"],
            ["一过冲就逆势", "通道仍强时过早猜顶底"],
            ["Overshoot"],
            48,
            88,
            4,
        ),
        _cx(
            "channel-breakout-failure",
            "通道突破失败",
            "失败形态",
            "PAF 16 Channels / PAF 18 Trading Ranges",
            "通道边缘的突破如果没有跟随，常会回到通道内；这类失败本质上是边缘交易，而不是中段追单。",
            ["channel breakout failure", "failed channel breakout", "通道突破失败", "失败突破"],
            ["宽通道或交易区间边缘", "突破后影线长、收盘差", "快速回到通道内"],
            ["回到通道后反向，或等待二次失败"],
            ["失败突破极点外"],
            ["通道中线或另一边"],
            ["突破时追在极端", "没有回到通道就提前反向"],
            ["Failed Channel BO"],
            52,
            89,
            3,
        ),
        _cx(
            "two-legged-correction",
            "两段修正",
            "回调",
            "PAF 09 Pullbacks / PAF 14 Trends",
            "很多回调和反转尝试会以两段形式展开。Brooks 用两段结构判断修正是否成熟，以及趋势方何时可能重新入场。",
            ["two legged correction", "two legs", "two-legged", "两段", "两腿"],
            ["趋势后第一轮修正", "第二腿弱于第一腿", "关键位附近第二次失败"],
            ["第二腿结束后看信号K和入场K", "顺原趋势优先"],
            ["第二腿极点外"],
            ["原趋势极点或测量目标"],
            ["第一腿刚出现就认为修正结束", "第二腿仍强时提前反向"],
            ["Two Legs"],
            56,
            95,
            3,
        ),
        _cx(
            "second-entry",
            "二次入场",
            "回调",
            "PAF 09 Pullbacks and Bar Counting",
            "二次入场的核心是第一批逆势交易者或追单者失败后，原趋势方得到更好的证据和更好的交易者方程。",
            ["second entry", "二次入场", "H2", "L2", "High 2", "Low 2"],
            ["趋势背景清楚", "第一次尝试失败", "第二次触发位置合理"],
            ["H2做多或L2做空，必须配合背景", "交易区间中只在边缘使用"],
            ["二次信号极点外"],
            ["前高前低、测量移动"],
            ["只会数K不会判断背景", "中段机械H2/L2"],
            ["Second Entry"],
            59,
            97,
            3,
        ),
        _cx(
            "trapped-traders",
            "被困交易者",
            "交易心理",
            "PAF 37 How to Trade / PAF 15 Breakouts",
            "Brooks 经常从被困交易者解释行情加速：失败方止损、补仓和平仓，会变成胜方的燃料。",
            ["trapped traders", "traders trapped", "被困交易者", "trap"],
            ["突破后快速反向", "信号触发后没有跟随", "关键位假突破"],
            ["等待失败方明显被迫退出后跟随胜方", "不要太早猜谁会被困"],
            ["失败结构另一侧"],
            ["被困方止损密集区或测量移动"],
            ["自己成了被困方还找理由", "没有确认就提前反向"],
            ["Trapped Traders"],
            55,
            96,
            4,
        ),
        _cx(
            "vacuum-test",
            "真空测试",
            "目标/磁力",
            "PAF 19 Support and Resistance / PAF 20 Measured Moves",
            "价格有时会快速冲向明显磁力位，这段运动像真空吸引；到达前不轻易反向，到达后再看反应。",
            ["vacuum test", "vacuum", "磁力测试", "真空"],
            ["上方或下方有明显前高前低", "价格突然加速但中间缺少阻力", "目标附近出现获利了结"],
            ["顺真空方向小心跟随，接近目标后管理", "反向要等到达后失败"],
            ["最近小结构外"],
            ["被测试的磁力位"],
            ["离磁力位很近还追大目标", "未到目标就猜反转"],
            ["Vacuum"],
            50,
            86,
            3,
        ),
        _cx(
            "buy-the-close",
            "收盘买入",
            "趋势",
            "PAF 14 Trends / PAF 15 Breakouts",
            "强多头趋势中，买方愿意在K线收盘买入，说明他们怕错过而不是怕回调；这是强趋势的典型行为。",
            ["buy the close", "BTC", "收盘买入", "buy close"],
            ["连续强多头K", "回调很浅或几乎没有", "空头信号反复失败"],
            ["强趋势里小仓顺势，或等第一次小回调", "不要在高潮末端加过大仓"],
            ["最近回调低点或微通道外"],
            ["测量移动、通道线、前高"],
            ["把所有阳线都当BTC", "高潮后还盲目追"],
            ["BTC"],
            60,
            91,
            4,
        ),
        _cx(
            "sell-the-close",
            "收盘卖出",
            "趋势",
            "PAF 14 Trends / PAF 15 Breakouts",
            "强空头趋势中，卖方愿意在K线收盘卖出，说明反弹很难等到；多头信号经常只是回调。",
            ["sell the close", "STC", "收盘卖出", "sell close"],
            ["连续强空头K", "反弹浅", "多头信号反复失败"],
            ["强趋势里小仓顺势，或等第一次小反弹", "不要在高潮末端卖太重"],
            ["最近回调高点或微通道外"],
            ["测量移动、通道线、前低"],
            ["把所有阴线都当STC", "跌势高潮后继续重仓追空"],
            ["STC"],
            60,
            91,
            4,
        ),
        _cx(
            "minor-reversal",
            "小反转",
            "反转/MTR",
            "PAF 21 Minor Reversals / PAF 22 MTR",
            "小反转通常只够做小目标或引发回调，不能自动升级成主要趋势反转；强趋势中第一反转大多失败。",
            ["minor reversal", "small reversal", "小反转", "反转"],
            ["趋势已有一定疲劳", "关键位附近", "只期待回调而非新趋势"],
            ["小目标交易或等二次证据", "强趋势中优先把它当回调"],
            ["反转信号外"],
            ["EMA、前一摆动点、两段回调"],
            ["把小反转当大反转", "逆强趋势重仓"],
            ["Minor Reversal"],
            42,
            89,
            3,
        ),
        _cx(
            "trend-resumption",
            "趋势恢复",
            "趋势",
            "PAF 14 Trends / PAF 09 Pullbacks",
            "趋势恢复通常发生在回调、交易区间或反转尝试失败后。真正要看的是原趋势方是否重新获得连续跟随。",
            ["trend resumption", "resume trend", "趋势恢复", "resumption"],
            ["回调没有破坏趋势", "逆势方两次尝试失败", "原趋势方出现强入场K"],
            ["顺原趋势方向入场", "突破回调结构后看跟随"],
            ["回调结构外"],
            ["前高前低或测量移动"],
            ["只因回调结束就入场", "没有跟随还坚持趋势恢复"],
            ["Resumption"],
            56,
            94,
            3,
        ),
        _cx(
            "trend-exhaustion",
            "趋势衰竭",
            "高潮",
            "PAF 29 Climaxes / PAF 14 Trends",
            "趋势衰竭不是看它走得远，而是看后续买卖力量是否还愿意继续推进；衰竭后常先进入回调或区间。",
            ["trend exhaustion", "exhausted trend", "衰竭", "趋势衰竭"],
            ["连续高潮K后跟随变差", "通道线过冲", "末端旗形或楔形"],
            ["等失败或二次信号", "顺势仓位靠近目标时管理"],
            ["末端极点外"],
            ["EMA、前一突破点、区间中线"],
            ["因为涨跌很多就逆势", "没有反向跟随仍赌衰竭"],
            ["Exhaustion"],
            47,
            90,
            4,
        ),
        _cx(
            "trading-range-middle",
            "交易区间中段",
            "交易区间",
            "PAF 18 Trading Ranges / HTT 47",
            "区间中段是 Brooks 最不喜欢新手交易的位置：上下空间都差，突破和反转都容易失败。",
            ["middle of trading range", "middle third", "区间中段", "trading range"],
            ["价格在区间中线附近", "K线重叠影线多", "方向信号频繁失败"],
            ["少交易或只做高质量小目标", "等待回到边缘"],
            ["小结构外，仓位更轻"],
            ["区间边缘或中线小目标"],
            ["中段追突破", "中段做大目标"],
            ["Middle of TR"],
            35,
            88,
            2,
        ),
        _cx(
            "trading-range-edge",
            "交易区间边缘",
            "交易区间",
            "PAF 18 Trading Ranges / HTT 47",
            "区间边缘是低买高卖和失败突破的主战场。边缘不是立即反向，而是看突破是否失败。",
            ["edge of trading range", "buy low sell high", "区间边缘", "低买高卖"],
            ["接近区间高低点", "突破缺少跟随", "出现反向信号K"],
            ["边缘失败突破后反向", "强突破后顺势但要确认"],
            ["区间外或失败结构外"],
            ["中线、另一侧边缘"],
            ["还没到边缘就提前反向", "强突破后死守区间思维"],
            ["TR Edge"],
            55,
            95,
            3,
        ),
        _cx(
            "scalp-vs-swing",
            "剥头皮 vs 波段",
            "交易管理",
            "PAF 31-36 Management / HTT 40",
            "同一个入场，背景不同，管理方式完全不同。强趋势争取波段，交易区间多用小目标。",
            ["scalp", "swing", "剥头皮", "波段", "management"],
            ["趋势日用波段预期", "区间日降低目标", "入场风险与目标匹配"],
            ["入场前先决定是小目标还是波段", "跟随变强时保留部分仓位"],
            ["按实际风险和结构设置"],
            ["固定小目标、测量移动或当天磁力位"],
            ["把区间单拿成趋势单", "把强趋势单过早平掉"],
            ["Scalp/Swing"],
            50,
            95,
            3,
        ),
        _cx(
            "actual-risk",
            "实际风险",
            "交易管理",
            "PAF 28 Orders / PAF 31 Management",
            "实际风险是入场后市场通常需要给你的空间，常常小于理论止损但大于你希望的最小风险；看对方向也可能因风险设错而亏。",
            ["actual risk", "risk", "实际风险", "初始风险"],
            ["信号K太大时重新评估仓位", "波动扩大时降低手数", "止损位置符合结构"],
            ["先算风险再入场", "不为了仓位好看而缩止损"],
            ["结构外而不是随意点数"],
            ["至少覆盖交易者方程"],
            ["止损太紧被正常波动扫出", "止损太宽导致无法执行"],
            ["Actual Risk"],
            50,
            98,
            3,
        ),
        _cx(
            "trader-equation",
            "交易者方程",
            "交易管理",
            "PAF 31 Management / PAF 37 How to Trade",
            "Brooks 用交易者方程把胜率、风险和收益放在一起。高胜率不等于好交易，低胜率也可能有正期望。",
            ["trader's equation", "trader equation", "risk reward probability", "交易者方程"],
            ["胜率、风险、收益同时可估", "目标符合市场背景", "风险可执行"],
            ["入场前确认方程为正", "背景变差就调低目标或退出"],
            ["按结构和仓位共同决定"],
            ["符合期望值的目标"],
            ["只看胜率", "只看盈亏比", "忽略实际成交和滑点"],
            ["Trader Equation"],
            50,
            99,
            4,
        ),
        _cx(
            "protective-stop",
            "保护性止损",
            "交易管理",
            "PAF 28 Orders / PAF 31 Management",
            "保护性止损要放在交易理由失效的位置；太近会被正常噪音扫掉，太远则让交易者方程失衡。",
            ["protective stop", "stop loss", "保护性止损", "止损"],
            ["结构清晰", "入场前已经知道失效点", "仓位按止损距离调整"],
            ["入场同时设置止损", "强趋势中可用结构移动止损"],
            ["信号K、回调、区间或趋势结构外"],
            ["先保本，再看波段目标"],
            ["随意移动止损", "亏损后取消止损"],
            ["Protective Stop"],
            50,
            97,
            3,
        ),
        _cx(
            "breakeven-stop",
            "保本止损",
            "交易管理",
            "PAF 31 Management",
            "保本止损是管理工具，不是自动规则。太早保本会被正常回踩扫出，太晚则暴露不必要风险。",
            ["breakeven stop", "break even", "保本止损", "BE"],
            ["已经有足够利润缓冲", "市场接近目标前回踩风险增加", "波段仓位需要保护"],
            ["根据结构移动，不按情绪移动", "强趋势中给价格更多空间"],
            ["入场价、最近结构或EMA附近"],
            ["保留波段尾仓或小目标兑现"],
            ["一赚钱就立刻保本", "该退出时只想保本"],
            ["BE Stop"],
            48,
            85,
            2,
        ),
        _cx(
            "scaling-in",
            "加仓 / 摊位",
            "交易管理",
            "PAF 31 Management / HTT 47 Trading Ranges",
            "加仓和摊位只适合明确计划、足够资金和合适背景。区间交易者会摊位，趋势交易者更重视顺势加仓。",
            ["scaling in", "scale in", "加仓", "摊位"],
            ["入场前有完整计划", "区间背景或强趋势背景明确", "总风险可承受"],
            ["区间摊位只在价值区，趋势加仓只顺控制权", "每次加仓都重新计算风险"],
            ["总仓结构外"],
            ["平均成本后的合理目标"],
            ["亏损后无计划摊平", "强趋势里逆势越跌越买"],
            ["Scale In"],
            45,
            86,
            4,
        ),
        _cx(
            "scaling-out",
            "减仓 / 部分止盈",
            "交易管理",
            "PAF 31 Management",
            "部分止盈能降低心理压力，但也会降低强趋势里的波段收益；是否减仓要看背景而不是习惯。",
            ["scaling out", "scale out", "减仓", "部分止盈"],
            ["接近磁力位", "跟随开始变差", "需要保留尾仓观察"],
            ["先出一部分，再用结构管理剩余仓位"],
            ["剩余仓位用保护止损"],
            ["小目标 + 波段目标组合"],
            ["强趋势过早全平", "区间里贪波段不减仓"],
            ["Scale Out"],
            50,
            84,
            2,
        ),
        _cx(
            "opening-gap",
            "开盘跳空",
            "开盘",
            "HTT 48 Trading the Open / PAF 11 Gaps",
            "开盘跳空会改变当天磁力结构：是否回补、是否守住缺口、是否形成趋势日，是早盘判断的关键。",
            ["opening gap", "gap open", "开盘跳空", "开盘缺口"],
            ["跳空到昨日区间外", "开盘后是否快速回补", "缺口边缘是否被守住"],
            ["缺口守住顺势，快速回补按失败突破处理"],
            ["开盘缺口另一侧或早盘结构外"],
            ["昨日高低点、开盘价、测量目标"],
            ["跳空后立刻反向赌回补", "缺口被关仍坚持趋势日"],
            ["Opening Gap"],
            53,
            90,
            3,
        ),
        _cx(
            "first-hour-control",
            "早盘第一小时控制权",
            "开盘",
            "HTT 48 Trading the Open",
            "早盘第一小时通常决定当天是趋势日、交易区间日还是双向波动日。不要只看第一根K，要看连续性。",
            ["first hour", "opening hour", "早盘", "第一小时", "open"],
            ["开盘区间方向清楚", "突破后跟随强", "回调不深"],
            ["强趋势日顺势，双向日等边缘", "开盘混乱时降低频率"],
            ["早盘结构外"],
            ["当日高低点、开盘价、测量目标"],
            ["第一根K决定全天", "早盘中段追最差价格"],
            ["First Hour"],
            52,
            92,
            3,
        ),
        _cx(
            "middle-of-day-range",
            "中盘交易区间",
            "开盘",
            "HTT 48G-H Trading the Middle of the Day",
            "中盘常从早盘趋势或双向波动转成更安静的交易区间，目标要缩小，等待边缘比追中间好。",
            ["middle of day", "midday", "中盘", "午盘", "trading range"],
            ["早盘波动后进入重叠", "EMA变平", "突破缺少跟随"],
            ["边缘低买高卖或等待新突破", "中段少交易"],
            ["区间外"],
            ["区间中线、另一侧或开盘价"],
            ["中盘还用早盘趋势目标", "在中段频繁追单"],
            ["Midday Range"],
            43,
            84,
            2,
        ),
        _cx(
            "end-of-day-magnet",
            "尾盘磁力与收盘",
            "开盘",
            "HTT 48I-K Trading the End of the Day",
            "尾盘价格会被开盘价、当日高低点、VWAP/EMA和期权/整数位吸引；时间不够时目标和风险都要重新估。",
            ["end of day", "EOD", "close", "尾盘", "收盘", "magnet"],
            ["接近收盘", "价格靠近当日关键位", "一方需要防守收盘位置"],
            ["只做时间允许的目标", "接近磁力位先管理仓位"],
            ["尾盘小结构外"],
            ["开盘价、当日高低点、收盘磁力"],
            ["尾盘还期待远距离目标", "忽略收盘前突然反向"],
            ["End of Day"],
            45,
            86,
            3,
        ),
        _cx(
            "higher-time-frame-context",
            "高周期背景",
            "市场周期",
            "PAF 02 Chart Basics / PAF 37 How to Trade",
            "同一张5分钟图，放到日线、60分钟或15分钟背景里，交易意义会变。Brooks 会先看大背景再看当前setup。",
            ["higher time frame", "HTF", "高周期", "larger time frame"],
            ["日线或60分钟接近关键位", "当前周期形态与高周期方向一致", "高周期目标未到或刚到"],
            ["顺高周期更容易持有", "逆高周期只做清晰小目标"],
            ["当前结构外，同时尊重高周期失效位"],
            ["高周期磁力位或当前周期目标"],
            ["只看一张小周期图", "高周期到目标后还死拿小周期趋势"],
            ["HTF Context"],
            50,
            93,
            3,
        ),
        _cx(
            "small-vs-deep-pullback",
            "小回调 vs 深回调",
            "回调",
            "PAF 09 Pullbacks / PAF 14 Trends",
            "小回调说明趋势方控制权强；深回调说明对手方力量增加，可能转成宽通道、交易区间或MTR。",
            ["small pullback", "deep pullback", "小回调", "深回调"],
            ["比较回调深度、K线重叠和是否到EMA", "看回调后原趋势是否有跟随"],
            ["小回调顺势，深回调等待更多确认"],
            ["回调结构外"],
            ["原趋势极点或区间边缘"],
            ["深回调还按强趋势追", "小回调中等待完美价格错过趋势"],
            ["Pullback Depth"],
            55,
            90,
            3,
        ),
        _cx(
            "failed-breakout-return-range",
            "失败突破回到区间",
            "失败形态",
            "PAF 18 Trading Ranges / PAF 15 Breakouts",
            "区间突破如果快速回到区间内，突破方向交易者被困，价格常测试区间另一侧或至少回到中线。",
            ["failed breakout", "return into range", "失败突破", "回到区间"],
            ["突破后缺少跟随", "收盘回到区间内", "被困方止损推动反向"],
            ["回到区间后反向，或等突破点回测失败"],
            ["失败突破极点外"],
            ["区间中线、另一侧边缘"],
            ["突破刚发生就反向", "回区间后还相信原突破"],
            ["Return to Range"],
            58,
            96,
            3,
        ),
        _cx(
            "breakout-test",
            "突破点回测",
            "突破",
            "PAF 15 Breakouts / PAF 19 Support and Resistance",
            "突破后的回测会告诉你旧阻力是否变支撑、旧支撑是否变阻力；成功回测常给更好的二次入场。",
            ["breakout test", "test of breakout point", "突破点回测", "回测突破点"],
            ["强突破后第一次回踩", "回测不深且反向K弱", "原突破点被守住"],
            ["回测成功后顺突破方向", "失败则按失败突破处理"],
            ["突破点另一侧或回测结构外"],
            ["测量移动或下一磁力位"],
            ["还没回测完就追", "回测失败后还顺原突破"],
            ["BO Test"],
            60,
            94,
            3,
        ),
    ]
)


@dataclass
class PdfPage:
    pdf_name: str
    pdf_path: str
    page: int
    text: str
    kind: str


def run_node_payload() -> dict[str, Any]:
    node = NODE_EXE if NODE_EXE.exists() else shutil.which("node")
    if not node:
        raise RuntimeError("Node.js not found; cannot load existing encyclopedia data.")

    js = r"""
const fs = require('fs');
const vm = require('vm');
const ctx = {
  window: {},
  console: { log() {}, warn() {}, error() {} },
  localStorage: { getItem() { return null; }, setItem() {}, removeItem() {} }
};
vm.createContext(ctx);
for (const file of ['site-data.js', 'encyclopedia-data.js', 'ab-chart-assets.js']) {
  vm.runInContext(fs.readFileSync(file, 'utf8'), ctx, { filename: file });
}
const app = fs.readFileSync('app.js', 'utf8').replace(/\ninit\(\);\s*$/, '\n');
const projection = `
globalThis.__payload = {
  stats: siteData.stats || {},
  lessons: siteData.videoLessons.map((lesson) => ({
    title: lesson.title,
    module: lesson.module,
    language: lesson.language,
    topics: lesson.topics || [],
    summary: lesson.summary || '',
    bullets: (lesson.bullets || []).slice(0, 6),
    minutesEstimate: lesson.minutesEstimate || 0,
    cueCount: lesson.cueCount || 0,
    brief: videoLessonBrief(lesson)
  })),
  patterns: encyclopediaPatterns.map((pattern) => {
    const insight = patternVideoInsight(pattern);
    return {
      ...pattern,
      video: {
        synthesis: insight.synthesis,
        thesis: insight.thesis,
        topics: insight.topics,
        bullets: insight.bullets,
        checklist: insight.checklist,
        sequence: insight.sequence,
        warning: insight.warning,
        relatedCount: insight.relatedCount,
        courseRefs: insight.courseRefs.slice(0, 10),
        lessons: insight.related.slice(0, 8).map((lesson) => ({
          title: lesson.title,
          module: lesson.module,
          language: lesson.language,
          topics: lesson.topics || [],
          summary: lesson.summary || '',
          bullets: (lesson.bullets || []).slice(0, 5),
          minutesEstimate: lesson.minutesEstimate || 0,
          cueCount: lesson.cueCount || 0,
          brief: videoLessonBrief(lesson)
        }))
      }
    };
  })
};
`;
vm.runInContext(app + projection, ctx, { filename: 'app.js' });
process.stdout.write(JSON.stringify(ctx.__payload));
"""
    result = subprocess.run([str(node), "-e", js], cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(result.stdout)


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "")
    value = value.replace("\x00", "")
    return value.strip()


def list_price_action_pdfs(pdf_dir: Path) -> list[Path]:
    if not pdf_dir.exists():
        raise FileNotFoundError(f"PDF folder not found: {pdf_dir}")
    pdfs = []
    for pdf in sorted(pdf_dir.glob("*.pdf")):
        name = pdf.name
        if "缠中说禅" in name:
            continue
        if "价格行为" in name or "Brooks" in name or "AL " in name:
            pdfs.append(pdf)
    return pdfs


def build_pdf_index(pdf_dir: Path, refresh: bool = False) -> list[PdfPage]:
    TMP_DIR.mkdir(exist_ok=True)
    pdfs = list_price_action_pdfs(pdf_dir)
    source_sig = {str(pdf): pdf.stat().st_mtime for pdf in pdfs}
    if PDF_INDEX_CACHE.exists() and not refresh:
        cached = json.loads(PDF_INDEX_CACHE.read_text(encoding="utf-8"))
        if cached.get("source_sig") == source_sig:
            return [PdfPage(**row) for row in cached["pages"]]

    pages: list[PdfPage] = []
    for pdf in pdfs:
        kind = "course" if "基础篇" in pdf.name or "进阶篇" in pdf.name else "book"
        print(f"Indexing {pdf.name}...")
        reader = PdfReader(str(pdf))
        for index, page in enumerate(reader.pages, start=1):
            try:
                text = clean_text(page.extract_text() or "")
            except Exception:
                text = ""
            pages.append(PdfPage(pdf.name, str(pdf), index, text, kind))

    PDF_INDEX_CACHE.write_text(
        json.dumps({"source_sig": source_sig, "pages": [asdict(page) for page in pages]}, ensure_ascii=False),
        encoding="utf-8",
    )
    return pages


def split_terms(text: str) -> list[str]:
    terms: list[str] = []
    for part in re.split(r"[/+·,，;；|()（）\s]+", text or ""):
        part = part.strip()
        if len(part) >= 2:
            terms.append(part)
    return terms


def pattern_terms(pattern: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    terms.append(pattern.get("title", ""))
    terms.extend(split_terms(pattern.get("title", "")))
    terms.extend(pattern.get("aliases") or [])
    terms.extend(pattern.get("terms") or [])
    terms.extend(SPECIAL_TERMS.get(pattern.get("id"), []))
    terms.extend(split_terms(pattern.get("source", "")))
    terms.extend(FAMILY_TERMS.get(pattern.get("family"), []))
    for key in ["summary", "best", "entry", "stop", "target", "traps"]:
        value = pattern.get(key)
        if isinstance(value, list):
            for item in value:
                terms.extend(split_terms(item))
        else:
            terms.extend(split_terms(str(value or "")))
    source = pattern.get("source", "")
    terms.extend(re.findall(r"\b(?:PAF|HTT)\s*\d+[A-Z]?\b", source, re.I))
    seen = set()
    out = []
    for term in terms:
        normalized = clean_text(term).lower()
        if len(normalized) < 2 or normalized in seen or normalized in GENERIC_TERMS:
            continue
        seen.add(normalized)
        out.append(term)
    return out


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value:
        return [str(value)]
    return []


def first_text(value: Any, fallback: str) -> str:
    items = as_list(value)
    return items[0] if items else fallback


def lesson_text(lesson: dict[str, Any]) -> str:
    pieces = [
        lesson.get("title", ""),
        lesson.get("module", ""),
        lesson.get("language", ""),
        lesson.get("summary", ""),
        lesson.get("brief", ""),
        " ".join(lesson.get("topics") or []),
        " ".join(lesson.get("bullets") or []),
    ]
    return clean_text(" ".join(str(piece) for piece in pieces)).lower()


def score_lesson(pattern: dict[str, Any], lesson: dict[str, Any], terms: list[str]) -> float:
    text = lesson_text(lesson)
    if not text:
        return 0
    score = 0.0
    source = pattern.get("source", "")
    for term in terms:
        key = term.lower()
        if not key or key in GENERIC_TERMS:
            continue
        count = text.count(key)
        if count:
            score += min(count, 4) * (4 + min(len(key), 18) / 3)
    for code in re.findall(r"\b(?:PAF|HTT)\s*\d+[A-Z]?\b", source, re.I):
        compact = re.sub(r"\s+", " ", code.lower())
        loose = compact.replace(" ", "")
        title = str(lesson.get("title", "")).lower().replace(" ", "")
        if loose in title:
            score += 35
    family = pattern.get("family", "")
    topics = " ".join(lesson.get("topics") or [])
    if family and family in topics:
        score += 18
    if pattern.get("title", "").lower() in text:
        score += 25
    return score


def related_lessons(pattern: dict[str, Any], lessons: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    terms = pattern_terms(pattern)
    scored = [(lesson, score_lesson(pattern, lesson, terms)) for lesson in lessons]
    scored = [(lesson, score) for lesson, score in scored if score > 0]
    scored.sort(key=lambda item: (item[1], item[0].get("language") == "中文", item[0].get("cueCount", 0)), reverse=True)
    selected: list[dict[str, Any]] = []
    seen_titles: set[str] = set()
    for lesson, _score in scored:
        title = str(lesson.get("title", ""))
        dedupe_key = re.sub(r"\s+", " ", title).lower()
        if dedupe_key in seen_titles:
            continue
        seen_titles.add(dedupe_key)
        selected.append(
            {
                "title": lesson.get("title", ""),
                "module": lesson.get("module", ""),
                "language": lesson.get("language", ""),
                "topics": lesson.get("topics") or [],
                "summary": lesson.get("summary", ""),
                "bullets": (lesson.get("bullets") or [])[:5],
                "minutesEstimate": lesson.get("minutesEstimate", 0),
                "cueCount": lesson.get("cueCount", 0),
                "brief": lesson.get("brief") or lesson.get("summary", ""),
            }
        )
        if len(selected) >= limit:
            break
    return selected


def video_summary_for_extra(pattern: dict[str, Any], lessons: list[dict[str, Any]]) -> dict[str, Any]:
    related = related_lessons(pattern, lessons, limit=10)
    lesson_titles = [lesson["title"] for lesson in related[:4]]
    course_refs = [
        {
            "title": lesson["title"],
            "languages": lesson["language"] or "未知",
            "topics": " / ".join((lesson.get("topics") or [])[:3]),
        }
        for lesson in related[:8]
    ]
    bullets: list[str] = []
    for lesson in related:
        for bullet in lesson.get("bullets") or []:
            bullet = str(bullet).strip().rstrip("。；;,.，")
            if bullet and bullet not in bullets:
                bullets.append(bullet)
            if len(bullets) >= 6:
                break
        if len(bullets) >= 6:
            break
    if not bullets:
        bullets = [
            f"先判断背景：{first_text(pattern.get('best'), '当前市场周期是否合适')}",
            f"再看触发：{first_text(pattern.get('entry'), '是否有信号K和跟随')}",
            f"失效条件：{first_text(pattern.get('traps'), '信号失败或位置不对')}",
        ]
    lesson_phrase = "、".join(lesson_titles) if lesson_titles else pattern.get("source", "相关课程")
    background = first_text(pattern.get("best"), "市场周期必须合适")
    trigger = first_text(pattern.get("entry"), "信号K和入场K需要有跟随")
    warning = first_text(pattern.get("traps"), "触发后无跟随")
    target = first_text(pattern.get("target"), "最近磁力位或测量目标")
    stop = first_text(pattern.get("stop"), "交易理由失效处")
    synthesis_templates = [
        (
            f"把 {lesson_phrase} 这些课合起来看，「{pattern['title']}」最先要解决的是背景问题：{background}。"
            f"只有背景站得住，再去看触发：{trigger}。Brooks 讲这类内容时通常会把控制权、被困交易者、"
            f"实际风险和目标距离连在一起，而不是让你看见一个名词就下单；一旦出现 {warning}，原逻辑就要降级或放弃。"
        ),
        (
            f"学习「{pattern['title']}」不要从定义开始背，而要从图上问三件事：现在谁在控盘，"
            f"触发是否真的是 {trigger}，止损放到 {stop} 后，目标 {target} 还值不值得做。"
            f"{lesson_phrase} 相关课程反复强调，同一个形状在趋势、通道和交易区间里的含义会完全不同。"
        ),
        (
            f"这组课程里，Brooks 会把「{pattern['title']}」当成交易者方程的一部分：背景是 {background}，"
            f"触发是 {trigger}，风险看 {stop}，目标先盯 {target}。如果图上开始出现 {warning}，"
            f"它就不再是原来的优势形态，而更像失败、观望或小目标管理。"
        ),
        (
            f"从 {lesson_phrase} 的讲法看，「{pattern['title']}」不是孤立按钮，而是一套读图顺序。"
            f"先筛掉不合格背景：{background}；再等市场给出可执行触发：{trigger}；"
            f"最后用 {stop} 和 {target} 检查风险收益。这样读，才接近 Brooks 说的按价格行为交易。"
        ),
    ]
    synthesis = synthesis_templates[sum(ord(ch) for ch in pattern["id"]) % len(synthesis_templates)]
    return {
        "synthesis": synthesis,
        "thesis": f"{pattern['title']} 的核心是把位置、触发、跟随和风险放在同一个交易者方程里判断。",
        "topics": sorted({topic for lesson in related for topic in (lesson.get("topics") or [])})[:8],
        "bullets": bullets,
        "checklist": [
            {"label": "背景", "value": first_text(pattern.get("best"), "先确认市场周期")},
            {"label": "触发", "value": first_text(pattern.get("entry"), "等待信号K和入场K")},
            {"label": "止损", "value": first_text(pattern.get("stop"), "放在交易理由失效处")},
            {"label": "目标", "value": first_text(pattern.get("target"), "最近磁力位或测量目标")},
            {"label": "放弃", "value": first_text(pattern.get("traps"), "触发后没有跟随")},
        ],
        "sequence": [
            f"先问：这是不是 {pattern.get('family', '当前主题')} 该出现的位置？",
            f"再问：触发是否符合 {first_text(pattern.get('entry'), '信号K和入场K')}？",
            f"最后问：止损 {first_text(pattern.get('stop'), '结构外')} 到目标 {first_text(pattern.get('target'), '磁力位')} 的方程是否划算？",
        ],
        "warning": first_text(pattern.get("traps"), "触发后无跟随"),
        "relatedCount": len(related),
        "courseRefs": course_refs,
        "lessons": related[:8],
    }


def make_extra_pattern(concept: dict[str, Any], lessons: list[dict[str, Any]]) -> dict[str, Any]:
    item = dict(concept)
    item.setdefault("aliases", [])
    item.setdefault("winRate", "视背景")
    item.setdefault("probScore", concept.get("probScore", 50))
    item.setdefault("importance", concept.get("importance", 82))
    item.setdefault("difficulty", concept.get("difficulty", 3))
    item["video"] = video_summary_for_extra(item, lessons)
    return item


def compact_title_key(title: str) -> str:
    key = re.split(r"[/：:|]", title or "", maxsplit=1)[0]
    return re.sub(r"\s+", "", key).lower()


def expand_patterns(patterns: list[dict[str, Any]], lessons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing_ids = {pattern["id"] for pattern in patterns}
    existing_title_keys = {compact_title_key(pattern.get("title", "")) for pattern in patterns}
    expanded = list(patterns)
    for concept in EXTRA_CONCEPTS:
        if concept["id"] in existing_ids:
            continue
        title_key = compact_title_key(concept.get("title", ""))
        if title_key and title_key in existing_title_keys:
            continue
        expanded.append(make_extra_pattern(concept, lessons))
        existing_ids.add(concept["id"])
        existing_title_keys.add(title_key)
    return expanded


def page_text_stats(text: str) -> dict[str, int | float]:
    ascii_count = len(re.findall(r"[A-Za-z]", text or ""))
    zh_count = len(re.findall(r"[\u4e00-\u9fff]", text or ""))
    words = len(re.findall(r"[A-Za-z]{2,}", text or ""))
    bullets = len(re.findall(r"•|▪|◦|\n\s*[-*]\s+", text or ""))
    sentences = len(re.findall(r"[.!?。！？]", text or ""))
    ratio = ascii_count / max(1, ascii_count + zh_count)
    return {
        "ascii": ascii_count,
        "zh": zh_count,
        "words": words,
        "bullets": bullets,
        "sentences": sentences,
        "english_ratio": ratio,
    }


def is_non_chart_text_page(page: PdfPage) -> bool:
    text = clean_text(page.text)
    if not text:
        return False
    lower = text.lower()
    stats = page_text_stats(text)
    words = int(stats["words"])
    bullets = int(stats["bullets"])
    sentences = int(stats["sentences"])
    zh_count = int(stats["zh"])

    if re.match(r"^(main points|主要内容|目录)\b", text, re.I):
        return True
    if re.match(r"^indicators:\s+", text, re.I):
        return True
    if "ail =" in lower and "blshs =" in lower and "mag =" in lower:
        return True

    long_english_bullets = bullets >= 8 and words >= 180 and zh_count < 80
    dense_english_handout = words >= 320 and sentences >= 15 and bullets >= 4 and zh_count < 80
    breakout_checklist = (
        "the breakout bar has" in lower
        and "the next bar has" in lower
        and "there is a sense of confusion" in lower
    )
    return bool(long_english_bullets or dense_english_handout or breakout_checklist)


def score_page(pattern: dict[str, Any], page: PdfPage, terms: list[str]) -> float:
    text = page.text.lower()
    if not text or is_non_chart_text_page(page):
        return 0
    score = 0.0
    family = pattern.get("family", "")
    if page.kind == "course":
        score += 8
    else:
        score += 2
    for term in terms:
        key = term.lower()
        if not key or key.isdigit():
            continue
        count = text.count(key)
        if not count:
            continue
        weight = 2.5
        if len(key) >= 8:
            weight += 4
        if key in {pattern.get("family", "").lower(), family.lower()}:
            weight += 2
        if re.match(r"^(paf|htt)\s*\d+", key):
            weight += 16
        score += min(count, 4) * weight
    title_words = [
        w.lower()
        for w in split_terms(pattern.get("title", ""))
        if len(w) > 2 and w.lower() not in GENERIC_TERMS
    ]
    if title_words and sum(1 for word in title_words if word in text) >= min(2, len(title_words)):
        score += 20
    return score


def select_pages(pattern: dict[str, Any], pages: list[PdfPage], per_pattern: int) -> list[tuple[PdfPage, float]]:
    terms = pattern_terms(pattern)
    scored = [(page, score_page(pattern, page, terms)) for page in pages]
    scored = [(page, score) for page, score in scored if score > 0]
    special = [term.lower() for term in SPECIAL_TERMS.get(pattern.get("id"), []) if len(term) > 2]
    if special:
        exact_scored = [
            (page, score + 35)
            for page, score in scored
            if any(term in page.text.lower() for term in special)
        ]
        if len(exact_scored) >= min(per_pattern, 2):
            scored = exact_scored
    scored.sort(key=lambda item: (item[1], item[0].kind == "course", -item[0].page), reverse=True)

    selected: list[tuple[PdfPage, float]] = []
    used_pdfs: set[str] = set()
    used_nearby: set[tuple[str, int]] = set()
    for page, score in scored:
        bucket = (page.pdf_name, math.floor(page.page / 4))
        if bucket in used_nearby:
            continue
        if len(selected) < max(2, per_pattern - 1) and page.kind != "course":
            continue
        selected.append((page, score))
        used_pdfs.add(page.pdf_name)
        used_nearby.add(bucket)
        if len(selected) >= per_pattern:
            break

    if len(selected) < per_pattern:
        for page, score in scored:
            if any(item[0].pdf_name == page.pdf_name and item[0].page == page.page for item in selected):
                continue
            selected.append((page, score))
            if len(selected) >= per_pattern:
                break
    return selected


def render_page_to_webp(page: PdfPage, out_file: Path, width: int = 1280) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    if out_file.exists():
        return
    pdftoppm = PDFTOPPM_EXE if PDFTOPPM_EXE.exists() else shutil.which("pdftoppm")
    if not pdftoppm:
        raise RuntimeError("pdftoppm not found.")
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "page"
        subprocess.run(
            [
                str(pdftoppm),
                "-f",
                str(page.page),
                "-l",
                str(page.page),
                "-jpeg",
                "-r",
                "130",
                page.pdf_path,
                str(prefix),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        jpgs = sorted(Path(tmp).glob("page-*.jpg"))
        if not jpgs:
            raise RuntimeError(f"Render failed for {page.pdf_name} p.{page.page}")
        with Image.open(jpgs[0]) as img:
            img = img.convert("RGB")
            if img.width > width:
                ratio = width / img.width
                img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
            img.save(out_file, "WEBP", quality=82, method=6)


def chart_note(pattern: dict[str, Any], page: PdfPage, rank: int) -> str:
    video = pattern.get("video", {})
    bullet = ""
    bullets = video.get("bullets") or []
    if bullets:
        bullet = str(bullets[rank % len(bullets)]).strip().rstrip("。；;,.，")
    first_best = first_text(pattern.get("best"), "先确认背景")
    first_entry = first_text(pattern.get("entry"), "等待触发")
    first_stop = first_text(pattern.get("stop"), "放在结构外")
    first_target = first_text(pattern.get("target"), "最近磁力位")
    first_trap = first_text(pattern.get("traps"), "信号失败")
    text = page.text
    focus_words = []
    for key, label in [
        ("突破", "突破后有没有跟随"),
        ("回调", "回调是否仍然弱"),
        ("交易区间", "价格是否在区间边缘还是中段"),
        ("通道", "通道斜率和边线反应"),
        ("反转", "反转是否已有二次证据"),
        ("楔形", "三推之后有没有失败"),
        ("缺口", "缺口是否被守住"),
        ("支撑", "支撑位测试后的反应"),
        ("阻力", "阻力位测试后的反应"),
        ("测量", "测量目标附近的管理"),
        ("开盘", "早盘控制权是否清楚"),
        ("止损", "失效点是否明确"),
    ]:
        if key in text and label not in focus_words:
            focus_words.append(label)
    focus = "、".join(focus_words[:2]) if focus_words else f"{pattern.get('family', '当前结构')}里的位置和跟随"
    tip = f" 课程提示：{bullet}。" if bullet else ""
    templates = [
        (
            f"先别急着找入场，先看这页把「{pattern['title']}」放在什么位置：{focus}。"
            f"如果背景接近“{first_best}”，再去检查触发是否满足“{first_entry}”；"
            f"触发后没有跟随，就按“{first_trap}”处理。{tip}"
        ),
        (
            f"这页适合按 Brooks 的顺序读：背景 -> 触发 -> 风险。背景看“{first_best}”，"
            f"触发看“{first_entry}”，止损不要凭感觉收窄，先参考“{first_stop}”。"
            f"本页重点盯住：{focus}。{tip}"
        ),
        (
            f"把图上的走势当成复盘样本：同样叫「{pattern['title']}」，只有出现在合适背景里才有优势。"
            f"这页最值得比较的是 {focus}；目标先看“{first_target}”，一旦出现“{first_trap}”，"
            f"就说明原交易理由已经变弱。{tip}"
        ),
        (
            f"本页不要只看形状，关键是控制权有没有转移。若“{first_best}”成立，"
            f"再等“{first_entry}”；若价格在触发后马上回到原结构内，"
            f"它更像失败形态而不是标准「{pattern['title']}」。重点：{focus}。{tip}"
        ),
        (
            f"用这页练一个判断句：背景是“{first_best}”，触发是“{first_entry}”，"
            f"风险放在“{first_stop}”，目标看“{first_target}”。"
            f"只要其中一环不成立，就别因为名字像「{pattern['title']}」而硬做。{tip}"
        ),
    ]
    return templates[rank % len(templates)]


def build_site(args: argparse.Namespace) -> None:
    payload = run_node_payload()
    pages = build_pdf_index(Path(args.pdf_dir), refresh=args.refresh_index)
    all_patterns = expand_patterns(payload["patterns"], payload.get("lessons", []))
    out_dir = Path(args.out)
    chart_dir = out_dir / "assets" / "charts"
    chart_dir.mkdir(parents=True, exist_ok=True)

    site_patterns = []
    total = len(all_patterns)
    for idx, pattern in enumerate(all_patterns, start=1):
        selected = select_pages(pattern, pages, args.images_per_pattern)
        charts = []
        print(f"{idx:03d}/{total} {pattern['title']}: {len(selected)} pages")
        for rank, (page, score) in enumerate(selected, start=1):
            out_file = chart_dir / f"{pattern['id']}-{rank:02d}.webp"
            render_page_to_webp(page, out_file)
            charts.append(
                {
                    "src": str(out_file.relative_to(out_dir)).replace("\\", "/"),
                    "source": page.pdf_name,
                    "page": page.page,
                    "score": round(score, 1),
                    "note": chart_note(pattern, page, rank - 1),
                    "textPreview": page.text[:360],
                }
            )
        item = dict(pattern)
        item["charts"] = charts
        site_patterns.append(item)

    data = {
        "author": "Karthus.Liu",
        "builtFrom": "E:/价格行为学/价格行为学文字资料",
        "patternCount": len(site_patterns),
        "chartCount": sum(len(pattern["charts"]) for pattern in site_patterns),
        "stats": payload.get("stats", {}),
        "patterns": site_patterns,
    }
    (out_dir / "data.js").write_text(
        "window.CN_PATTERN_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-dir", default=str(DEFAULT_PDF_DIR))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--images-per-pattern", type=int, default=4)
    parser.add_argument("--refresh-index", action="store_true")
    args = parser.parse_args()
    build_site(args)


if __name__ == "__main__":
    main()
