const lessons = [
  {
    title: "先建立交易语言",
    subtitle: "不要先找圣杯，先学会用同一套语言读图。",
    level: "基础",
    terms: ["价格行为", "市场周期", "Always In", "交易者方程"],
    diagram: "cycle",
    intro: "价格行为学不是背 K 线形态，而是理解市场正在用价格表达什么：谁被套住、谁在获利了结、谁被迫追单、哪一方掌控了下一段空间。",
    concepts: [
      ["背景优先", "同一根反转 K，在强趋势里可能只是噪音，在区间边缘可能是好信号。Brooks 的核心是先判断背景，再判断信号。"],
      ["形态不是图案", "MTR、楔形、突破、通道都不是静态图案，而是多空行为过程。你要读的是行为，不是轮廓。"],
      ["概率不是确定性", "大多数时间，多空交易的成功概率都在 40%-60% 之间。交易不是追求永远正确，而是让概率、风险和回报形成正期望。"],
      ["一切都要可执行", "任何知识点最后都必须落到：何时进、止损在哪、目标在哪、什么情况不做。"]
    ],
    read: [
      "价格行为 = 市场参与者通过每一根 K 线、每一次突破、每一次回调表达出来的集体行为。",
      "学习顺序应该是：市场周期 -> 趋势/区间 -> 信号 K -> 形态 -> 概率与管理 -> 练习统计。",
      "不要一开始就混看太多二创课程。先用核心课建立 Brooks 术语，再用补充课解决卡点。",
      "本课程把文件夹里的资料消化进网页内容；原资料只作为来源，不再要求你另行打开。"
    ],
    practice: ["打开任意图表，先只说一句话：现在是趋势、区间，还是突破模式。", "每次判断后写下证据：连续收盘？重叠多？尾巴多？是否接近磁力位？"],
    quiz: {
      q: "学习价格行为时，最先要建立的能力是什么？",
      options: ["背诵所有 K 线形态", "判断市场背景和周期", "找到胜率 90% 的指标"],
      answer: 1,
      explain: "同一形态在不同背景下意义完全不同。先读背景，再谈信号。"
    }
  },
  {
    title: "市场周期：突破、通道、区间",
    subtitle: "市场通常从强突破进入通道，再进入交易区间。",
    level: "基础",
    terms: ["Breakout", "Channel", "Trading Range", "Inertia"],
    diagram: "cycle",
    intro: "Brooks 的市场周期可以简化为三个阶段：突破阶段最强，通道阶段变弱，交易区间阶段双向交易。你每一笔交易都要先问：我在哪个阶段？",
    concepts: [
      ["突破阶段", "连续强趋势 K、收盘靠近极端、回调浅。此时顺势概率最高，但止损通常更远。"],
      ["通道阶段", "仍然是趋势，但推进变重叠、回调变明显。通道最终常转成区间。"],
      ["交易区间", "多空都能赚钱，突破多数失败。边缘交易优于中间交易。"],
      ["惯性规则", "趋势中大多数反转尝试失败；区间中大多数突破尝试失败。不要和当前背景硬拧。"]
    ],
    read: [
      "强突破时，市场在快速重新定价。追随突破方向通常比猜反转更合理。",
      "通道是弱趋势。它仍有方向，但不再像突破阶段那样单边。",
      "交易区间里，价格会在高低点之间来回测试，追突破很容易变成买高卖低。",
      "你的交易类型要匹配周期：突破做顺势，区间做失败突破，通道做边界和回调。"
    ],
    practice: ["在图表上标出最近一段强突破、随后通道、再之后区间。", "每段只写一个允许交易方向：顺势、双向、还是等待。"],
    quiz: {
      q: "在交易区间里，Brooks 常提醒什么？",
      options: ["多数突破尝试会失败", "所有反转都不能做", "只要大阳线就追多"],
      answer: 0,
      explain: "区间环境里，突破失败是常态，所以边缘和失败突破更重要。"
    }
  },
  {
    title: "K线、信号K与入场K",
    subtitle: "信号 K 不单独决定交易，位置和背景决定它的质量。",
    level: "基础",
    terms: ["Signal Bar", "Entry Bar", "Tail", "Close"],
    diagram: "signal",
    intro: "信号 K 是触发交易的 K 线，入场 K 是订单触发后的下一根或当前触发 K。新手常犯的错是只看信号 K 好不好看，却忽略它出现在哪里。",
    concepts: [
      ["收盘位置", "强多头信号 K 通常收在高位，强空头信号 K 通常收在低位。收盘弱代表犹豫。"],
      ["尾巴", "长上影表示上方卖压，长下影表示下方买压。尾巴越多，越像区间。"],
      ["大小", "过小的 K 线缺少说服力；过大的 K 线可能让止损过远，风险收益变差。"],
      ["位置", "区间中间的漂亮信号 K 也可能很差；关键价位附近的普通信号 K 可能更有意义。"]
    ],
    read: [
      "信号 K 的任务是证明某一方在关键位置开始行动。",
      "入场 K 触发后，如果立刻反向并收得很差，说明信号质量不足。",
      "一根 K 线不能脱离上下文。你要同时看左侧压力、趋势方向、是否接近磁力位。"
    ],
    practice: ["截取 20 个信号 K，只评分三项：背景、位置、收盘。", "把亏损交易里的信号 K 标出来，判断是信号弱还是位置差。"],
    quiz: {
      q: "一个漂亮的多头反转 K 出现在强空头趋势中间，应该怎么处理？",
      options: ["直接重仓做多", "先按低概率信号看待，等待更多证据", "证明趋势已经结束"],
      answer: 1,
      explain: "趋势有惯性。强趋势中第一个反转信号大多只是小反弹。"
    }
  },
  {
    title: "趋势与 Always In",
    subtitle: "先判断谁控制市场，再决定你能不能逆势。",
    level: "核心",
    terms: ["AIL", "AIS", "Trend", "Pullback"],
    diagram: "trend",
    intro: "Always In 是 Brooks 的核心判断：如果必须持仓，现在应该偏多还是偏空？它迫使你从市场控制权角度读图，而不是每根 K 都两边猜。",
    concepts: [
      ["趋势定义", "上涨趋势高点和低点逐步抬高，下跌趋势高点和低点逐步降低。"],
      ["趋势质量", "连续强收盘、回调浅、突破有跟随，说明趋势质量高。"],
      ["回调买卖", "趋势里最常见的入场是回调后顺势，而不是追在最远端。"],
      ["逆势条件", "逆势需要更多证据：通道突破、二次信号、失败恢复、磁力位。"]
    ],
    read: [
      "当市场 Always In Long，多头回调买入通常比空头猜顶更合理。",
      "当市场 Always In Short，空头反弹卖出通常比多头猜底更合理。",
      "强趋势里，你感觉价格太高或太低，往往只是因为趋势强。不要用主观便宜/贵交易。"
    ],
    practice: ["每天只标一个 Always In 转换点：市场从偏多变偏空，或从偏空变偏多。", "记录转换前是否出现了突破、失败、二次信号。"],
    quiz: {
      q: "Always In 的实际用途是什么？",
      options: ["告诉你永远持仓", "帮助判断当前市场控制权和优先方向", "替代止损"],
      answer: 1,
      explain: "Always In 是方向和背景判断工具，不是无脑持仓规则。"
    }
  },
  {
    title: "回调与数K线",
    subtitle: "趋势交易的最佳入场，常常藏在回调里。",
    level: "核心",
    terms: ["Pullback", "High 2", "Low 2", "Bar Counting"],
    diagram: "h2l2",
    intro: "回调是趋势中的逆向运动。Brooks 很重视 High 1/2、Low 1/2，因为它们表达的是逆势方尝试失败后，趋势方重新进场。",
    concepts: [
      ["High 1 / Low 1", "一段回调后的第一次顺势触发。强趋势里可用，普通趋势里可能太早。"],
      ["High 2 / Low 2", "两段回调后的第二次顺势触发，常比第一次更可靠。"],
      ["深回调", "回调越深，风险收益可能更好，但趋势延续概率可能下降。"],
      ["回调失败", "趋势中的反向突破若失败，常给趋势方提供更好的入场。"]
    ],
    read: [
      "回调不是趋势结束，而是趋势方等待更好价格。",
      "High 2 多头旗、Low 2 空头旗的核心是：逆势方两次尝试都没能改变市场。",
      "不要机械数 K。数 K 线是为了理解行为，不是为了凑数字。"
    ],
    practice: ["找 50 个 High 2 / Low 2，只记录趋势背景是否清晰。", "把失败样本分成两类：趋势已坏、信号太弱。"],
    quiz: {
      q: "High 2 / Low 2 更适合什么背景？",
      options: ["清晰趋势中的回调", "区间中间随机波动", "重大新闻前无方向震荡"],
      answer: 0,
      explain: "它们是趋势延续形态，离开趋势背景就失去优势。"
    }
  },
  {
    title: "支撑阻力与磁力位",
    subtitle: "价格会被可见位置吸引，也会在这些地方制造陷阱。",
    level: "核心",
    terms: ["Support", "Resistance", "Magnet", "Measured Move"],
    diagram: "magnets",
    intro: "磁力位是市场共同看见的位置：前高低、区间边缘、开盘价、均线、趋势线、通道线、测量目标。它们不是自动买卖点，而是注意力聚集点。",
    concepts: [
      ["前高前低", "市场常测试前高前低，因为那里有止损、止盈和突破订单。"],
      ["开盘价", "日内交易里，开盘价经常成为多空争夺中心。"],
      ["测量移动", "市场常尝试 Leg 1 = Leg 2，或从区间高度投射目标。"],
      ["突破测试", "突破后回踩成功，说明旧阻力可能变支撑；失败则回到区间。"]
    ],
    read: [
      "磁力位只告诉你哪里重要，不告诉你方向。",
      "真正的交易信号来自价格在磁力位附近的反应：突破、失败、反转、跟随。",
      "目标位附近不要盲目追单，因为对手方可能开始获利了结。"
    ],
    practice: ["每张图只画 3 个最重要磁力位，避免画满屏。", "记录价格到达磁力位后，是突破、失败，还是横盘。"],
    quiz: {
      q: "磁力位最正确的用途是什么？",
      options: ["一到就反向交易", "判断哪里会发生重要反应", "保证价格一定停住"],
      answer: 1,
      explain: "磁力位是注意力位置，交易还要看到达后的行为。"
    }
  },
  {
    title: "交易区间：买低卖高",
    subtitle: "区间里，追随强 K 线经常变成反向流动性。",
    level: "核心",
    terms: ["Trading Range", "Failed Breakout", "Buy Low Sell High"],
    diagram: "range",
    intro: "交易区间的特点是重叠多、尾巴多、跟随差。这里的高概率逻辑不是追突破，而是等待区间边缘的突破失败。",
    concepts: [
      ["区间中间最差", "中间没有足够空间，方向也最不清晰。"],
      ["边缘更重要", "区间高点附近找卖出或失败突破，低点附近找买入或失败突破。"],
      ["突破失败", "区间里很多强突破只是吸引追单，随后回到区间。"],
      ["目标务实", "区间交易目标通常先看中线，再看另一端，不要默认走出大趋势。"]
    ],
    read: [
      "区间里多空双方都能赚钱，所以你要降低趋势预期。",
      "强 K 线突破区间边缘后，如果没有跟随，常常是反向机会。",
      "交易区间里，优秀交易常常看起来不舒服，因为你是在别人追突破时反向。"
    ],
    practice: ["找 30 个失败突破，写出失败证据：回到区间、无跟随、反向强 K。", "禁止在区间中间开仓，连续练一周。"],
    quiz: {
      q: "交易区间中最应该避免的位置是？",
      options: ["区间边缘", "区间中间", "失败突破后回到区间"],
      answer: 1,
      explain: "区间中间方向不清、空间不足，交易者方程通常很差。"
    }
  },
  {
    title: "通道：弱趋势的交易法",
    subtitle: "通道仍是趋势，但趋势方已经没有突破阶段那么强。",
    level: "进阶",
    terms: ["Channel", "Tight Channel", "Broad Channel", "Trendline"],
    diagram: "channel",
    intro: "通道是趋势中的弱化阶段。紧密通道适合顺势，宽通道更像倾斜的交易区间，靠近边界时要关注反向压力。",
    concepts: [
      ["紧密通道", "回调浅、连续推进，逆势风险高。"],
      ["宽通道", "两边都能交易，更接近带方向的区间。"],
      ["通道线", "第三次触及通道线附近，若出现失败突破或强反向 K，要警惕回到均线或另一侧。"],
      ["75%倾向", "Brooks 常提到通道最终倾向反向突破并转成区间，但时间点不能提前猜。"]
    ],
    read: [
      "通道里不要因为价格高就卖，也不要因为价格低就买。先判断紧密还是宽。",
      "紧密通道中的逆势信号多数只是小回调。",
      "宽通道边界可以找反向，但仍要用信号和止损管理风险。"
    ],
    practice: ["把 20 个通道分成紧密通道和宽通道。", "每个通道只标三处：趋势线、通道线、第一次明显失败突破。"],
    quiz: {
      q: "紧密通道中最常见的新手错误是什么？",
      options: ["过早逆势", "顺势等待回调", "按趋势方向管理仓位"],
      answer: 0,
      explain: "紧密通道代表趋势方仍强，早逆势容易被连续小止损。"
    }
  },
  {
    title: "主要趋势反转 MTR",
    subtitle: "MTR 是过程，不是单根 K 线。",
    level: "进阶",
    terms: ["MTR", "Trendline Break", "Second Entry", "TBTL"],
    diagram: "mtr",
    intro: "主要趋势反转通常需要：原趋势清晰、突破趋势线或通道、测试原极端失败、第二次反转信号。早期 MTR 常只有约 40% 波段成功率，但风险小、回报大。",
    concepts: [
      ["第一突破常是小反转", "第一次突破紧密通道通常只是回调，不足以证明趋势反转。"],
      ["测试失败", "价格回测原高/低失败，说明趋势方力量下降。"],
      ["第二次信号", "第二次反转通常比第一次更有意义。"],
      ["低胜率高回报", "早期 MTR 胜率不高，但若成功，回报常大于风险。"]
    ],
    read: [
      "MTR 的交易者不是在猜顶底，而是在市场给出结构变化后尝试抓新趋势早期。",
      "如果你想要更高概率，可以等反向强突破，但止损会更远，收益风险会变化。",
      "MTR 失败并不说明你看错全部，只说明当前样本属于那 60% 小赢小亏或失败。"
    ],
    practice: ["收集 30 个 MTR，只统计是否有趋势线突破和第二次信号。", "把第一次反转和第二次反转分开标记。"],
    quiz: {
      q: "早期 MTR 的常见概率口径更接近？",
      options: ["约 40% 波段成功率", "稳定 90% 胜率", "只要二次信号就必然反转"],
      answer: 0,
      explain: "早期反转胜率通常不高，必须依靠更好的风险收益。"
    }
  },
  {
    title: "楔形、末端旗形与高潮",
    subtitle: "趋势末端的反转，要看动能衰减和失败继续。",
    level: "进阶",
    terms: ["Wedge", "Final Flag", "Climax", "Exhaustion"],
    diagram: "wedge",
    intro: "楔形是三推后的动能衰减，末端旗形是趋势末端看似继续的小整理，高潮是短时间过度推进。它们都需要背景支持，不能孤立交易。",
    concepts: [
      ["楔形", "三次推进后，如果第三推靠近通道线或磁力位，并出现强反向信号，可能至少产生两段回调。"],
      ["末端旗形", "趋势末端的小整理先像继续形态，随后继续失败并反向。"],
      ["高潮", "连续大 K、缺口、远离均线后，市场可能需要横盘或反向两段。"],
      ["不要过早", "趋势可以比你想象的更久。所有末端形态都需要确认。"]
    ],
    read: [
      "楔形回调顺趋势交易通常比楔形反转更稳。",
      "末端旗形的难点是：它在形成时看起来像普通旗形。",
      "高潮之后不一定立刻反转，也可能先横盘消化。"
    ],
    practice: ["找 20 个三推，标出第三推之后是否真的出现两段反向运动。", "找 10 个看错的末端旗形，写明为什么其实只是中途整理。"],
    quiz: {
      q: "楔形反转最容易犯的错误是什么？",
      options: ["只数三推，不看背景和信号", "等待第三推", "观察是否接近磁力位"],
      answer: 0,
      explain: "三推只是结构，交易还要看背景、位置、信号和风险收益。"
    }
  },
  {
    title: "突破交易与测量移动",
    subtitle: "强突破是高概率，但止损远；测量移动是目标，不是魔法。",
    level: "进阶",
    terms: ["Breakout", "Follow-through", "Measured Move", "Pullback Test"],
    diagram: "breakout",
    intro: "强突破常是 Brooks 最喜欢的高概率交易。成功突破后，市场经常尝试测量移动目标。但突破越强，止损可能越远，仓位必须相应调整。",
    concepts: [
      ["成功突破", "突破后有跟随 K、收盘强、回调浅，说明突破质量高。"],
      ["失败突破", "突破后立刻回到原区间，说明追单被套，可能反向。"],
      ["测量目标", "常见目标包括突破 K 高度、区间高度、Leg 1 = Leg 2。"],
      ["入场选择", "激进者突破收盘进，保守者等回调测试。概率和风险会互换。"]
    ],
    read: [
      "强突破中的高概率不是免费午餐，它通常用更远止损支付。",
      "如果突破发生在交易区间内，要特别警惕没有跟随的失败突破。",
      "测量移动到达前可以管理仓位；到达附近要警惕获利了结。"
    ],
    practice: ["收集 50 个突破，分成成功突破和失败突破。", "每个成功突破都画出一个测量移动目标。"],
    quiz: {
      q: "突破交易中，高概率通常要用什么支付？",
      options: ["更远止损或更小仓位", "不用止损", "更高杠杆"],
      answer: 0,
      explain: "概率、风险和回报互相交换。强突破常需要更宽止损。"
    }
  },
  {
    title: "交易者方程与风险管理",
    subtitle: "胜率不是单独指标，风险收益一起决定系统能否活。",
    level: "系统",
    terms: ["Trader's Equation", "Actual Risk", "Reward", "Probability"],
    diagram: "equation",
    intro: "交易者方程把交易拆成三件事：成功概率、盈利空间、亏损风险。一笔 40% 胜率的交易，如果平均盈利足够大，也可能是正期望。",
    concepts: [
      ["40%-60%常态", "大多数交易没有压倒性确定性。你需要接受不确定性。"],
      ["高胜率的代价", "高胜率往往意味着止损更远、利润更小，或入场更晚。"],
      ["低胜率的补偿", "低胜率交易必须有足够大的回报，比如 MTR 早期入场。"],
      ["实际风险", "真正需要承受的风险，常比理论止损小或大。你要基于实际风险评估目标。"]
    ],
    read: [
      "正期望不是靠感觉，而是靠统计：胜率、平均盈利、平均亏损、手续费。",
      "不要把胜率高误认为系统好。一个 70% 胜率但亏损远大于盈利的系统仍可能亏钱。",
      "每一种 setup 都要独立统计，不能把不同手法混在一起。"
    ],
    practice: ["用 20 笔模拟交易计算：胜率、平均盈利、平均亏损、手续费后净值。", "把每笔交易标注为：完全按规则 / 违反规则。"],
    quiz: {
      q: "为什么 40% 胜率的交易也可能值得做？",
      options: ["因为亏损可以不算", "因为盈利目标可能远大于风险", "因为连续亏损不会发生"],
      answer: 1,
      explain: "只要平均盈利足够覆盖亏损和成本，低胜率也可能正期望。"
    }
  },
  {
    title: "订单、止损、加仓与止盈",
    subtitle: "入场只是开始，管理决定你能不能留下利润。",
    level: "系统",
    terms: ["Stop Order", "Limit Order", "Protective Stop", "Scaling In", "Taking Profits"],
    diagram: "management",
    intro: "Brooks 课程后半部分强调交易管理：用什么订单进场，止损放在哪里，是否加仓，什么时候止盈。新手应先用简单、可重复的规则。",
    concepts: [
      ["止损单入场", "顺着市场动能入场，适合多数新手和突破/信号 K 交易。"],
      ["限价单入场", "常用于区间边缘反向或加仓，但需要经验。"],
      ["保护止损", "止损要放在结构失效处，而不是随便设一个金额。"],
      ["止盈", "目标可以是 1R、2R、TBTL、测量移动、区间另一端。不同 setup 目标不同。"]
    ],
    read: [
      "不要为了仓位大而把止损放得太近。止损太近会让正常波动变成亏损。",
      "加仓会提高概率或改善均价，但也会增加复杂度。先把单次入场练稳。",
      "止盈不是越远越好。目标要和背景匹配：区间交易目标务实，趋势交易可保留仓位。"
    ],
    practice: ["每个 setup 写两个止损：结构止损和实际风险止损。", "每次复盘问：我的退出是规则，还是情绪？"],
    quiz: {
      q: "保护止损应该优先放在哪里？",
      options: ["账户刚好能承受的位置", "结构失效的位置", "离入场最近的位置"],
      answer: 1,
      explain: "止损的逻辑是：如果到达这里，原交易理由失效。"
    }
  },
  {
    title: "开盘、早盘与日内节奏",
    subtitle: "很多日内机会集中在开盘后，但开盘也最容易骗追单。",
    level: "实战",
    terms: ["Opening Reversal", "Open", "Gap", "First Hour"],
    diagram: "opening",
    intro: "日内交易里，开盘价、昨日高低、缺口和前 60-90 分钟非常关键。开盘可能形成强趋势，也可能快速测试磁力位后反转。",
    concepts: [
      ["开盘趋势", "连续强 K、回调浅、突破有跟随，优先顺势。"],
      ["开盘反转", "快速测试磁力位后失败，出现强反向信号，可能形成当天主波段。"],
      ["缺口", "缺口可能成为磁力位，也可能形成测量移动背景。"],
      ["尾盘", "尾盘反复反转更多，难度通常高于早盘。"]
    ],
    read: [
      "开盘不要急着预测。先看市场是强趋势开盘，还是测试磁力位。",
      "开盘反转需要位置和信号，不是看到第一根反向 K 就入场。",
      "如果你只做日内，先练早盘一个小时，别全天乱做。"
    ],
    practice: ["连续复盘 20 个交易日，只记录前 90 分钟：趋势开盘、区间开盘、开盘反转。", "每次写出当天最重要的开盘磁力位。"],
    quiz: {
      q: "开盘反转最需要哪两个条件？",
      options: ["重要位置 + 反向证据", "价格涨太多 + 想做空", "第一根 K 线很大"],
      answer: 0,
      explain: "开盘反转不是猜，而是重要磁力位附近的失败和反向信号。"
    }
  },
  {
    title: "把知识变成交易系统",
    subtitle: "你不需要掌握所有 setup，你需要固定一把武器。",
    level: "系统",
    terms: ["Setup", "Trading Plan", "Journal", "Deliberate Practice"],
    diagram: "system",
    intro: "资料里最重要的学习方法是：选一个 setup，写开平细节表，前 100 笔验证，101-400 笔固定，500 笔后看交易者方程。不要贪多。",
    concepts: [
      ["开平细节表 1.0", "从课程、PPT、书中把同一 setup 的条件逐条写出来。"],
      ["前 100 笔", "严格按表执行，分析每笔成功/失败原因。不合规交易剔除。"],
      ["2.0 固定", "保留成功共性，删除含糊条件，把高频错误写入不得交易。"],
      ["500 笔之后", "看胜率、盈亏比、手续费后是否正期望。若不适合你，舍弃。"]
    ],
    read: [
      "不要同时练突破、MTR、楔形、区间反转。一次只练一种。",
      "系统变、执行也变时，你永远分不清问题出在哪里。",
      "交易系统不是找到完美规则，而是找到你能稳定执行、有统计优势的一组动作。"
    ],
    practice: ["今天选一个 setup，写出背景、触发、止损、目标、不得交易。", "接下来 100 笔，只允许做这一种 setup。"],
    quiz: {
      q: "为什么训练时不能随意修改细节表？",
      options: ["因为规则越旧越好", "否则分不清系统问题还是执行问题", "因为市场不会变化"],
      answer: 1,
      explain: "统计必须基于稳定规则。规则和执行同时变化，样本就失真。"
    }
  }
];

const patterns = [
  ["breakout", "强突破 / Breakout", "趋势延续", "60-70%+", 68, 3, "#087f8c", "强突破阶段顺势概率最高，但止损常更远。", ["有意义支撑阻力被突破", "连续强收盘", "回调浅或有跟随"], ["突破无跟随", "区间内假突破", "追在高潮末端"]],
  ["h2l2", "High 2 / Low 2", "趋势延续", "60%左右", 62, 2, "#315f93", "趋势中两段回调失败后，顺趋势方重新接管。", ["Always In 趋势清晰", "两段回调", "第二次信号收盘强"], ["趋势已坏", "区间中间硬数 K", "信号 K 弱"]],
  ["opening", "开盘反转", "日内结构", "55-60%", 60, 4, "#d95d39", "开盘测试关键磁力位失败后，可能形成当天主波段。", ["快速到达昨日高低/开盘价/缺口", "反向压力出现", "突破微型趋势线"], ["强趋势开盘硬反转", "未到磁力位提前猜", "忽略跟随"]],
  ["range", "交易区间反转", "区间交易", "55-60%", 58, 3, "#637f35", "区间边缘的失败突破常优于追突破。", ["重叠多、尾巴多", "接近区间边缘", "突破后无跟随"], ["区间中间开仓", "强突破日逆势", "目标设太远"]],
  ["measured", "测量移动", "目标管理", "50-60%", 56, 3, "#b88117", "测量移动是目标框架，不是单独入场理由。", ["已有清晰第一段", "突破后跟随", "目标空间足够"], ["把目标当入场", "目标太近追单", "忽略获利了结"]],
  ["channel", "通道", "趋势结构", "55% / 75%倾向", 55, 4, "#7b507d", "通道是弱趋势；紧密通道顺势，宽通道更双向。", ["趋势线/通道线清晰", "推进重叠增加", "靠近边界"], ["紧密通道过早逆势", "把通道当矩形区间", "忽略加速突破"]],
  ["wedge", "楔形 / 三推", "反转或延续", "40-60%", 52, 3, "#b94738", "三推后动能衰减；顺趋势楔形回调通常更稳。", ["三次推进", "第三推靠近磁力位", "出现反向信号"], ["只数三推", "逆强趋势", "未失败先入场"]],
  ["magnet", "磁力位", "背景过滤", "条件增强", 49, 2, "#4c7c59", "磁力位是注意力位置，不是自动买卖点。", ["前高低/开盘价/均线/目标", "到位后出现反应", "与形态共振"], ["一到就交易", "忽略突破成功", "画太多水平位"]],
  ["finalflag", "末端旗形", "反转", "约40%", 44, 4, "#a76f22", "趋势末端看似继续的小整理，继续失败后可能反向。", ["趋势已久", "靠近磁力位", "继续突破无跟随"], ["趋势中段误判末端", "没有反向压力", "不接受小赢小亏"]],
  ["mtr", "主要趋势反转 / MTR", "反转", "约40%", 40, 5, "#5f6f84", "MTR 是结构过程，不是单根反转 K。", ["原趋势清晰", "突破趋势线", "测试失败与二次信号"], ["第一次突破就重仓", "忽略趋势惯性", "没有足够回报"]]
];

const glossary = [
  ["AIL / AIS", "Always In Long / Short，当前市场若必须持仓，应偏多或偏空。"],
  ["BO", "Breakout，突破支撑阻力、前高低、趋势线、通道线或均线。"],
  ["PB", "Pullback，趋势中的回调或反弹。"],
  ["TR / TTR", "Trading Range / Tight Trading Range，交易区间 / 窄交易区间。"],
  ["MTR", "Major Trend Reversal，主要趋势反转，需要结构确认。"],
  ["TBTL", "Ten Bars Two Legs，至少 10 根 K、两段运动，常用于反转后目标。"],
  ["MM", "Measured Move，测量移动，常用作目标位。"],
  ["EMA20", "Brooks 课程默认的 20 周期指数均线。"],
  ["Signal Bar", "信号 K，提供交易触发条件的 K 线。"],
  ["Entry Bar", "入场 K，订单触发后的 K 线。"],
  ["High 2 / Low 2", "趋势中两段回调后的顺势旗形。"],
  ["Climax", "高潮，短时间过度推进，常引发横盘或反向。"],
  ["Final Flag", "末端旗形，趋势末端看似继续、实际可能失败的小整理。"],
  ["Wedge", "楔形或三推，表示多次推进后的动能衰减。"],
  ["Magnet", "磁力位，市场容易测试的可见价位。"],
  ["Actual Risk", "实际风险，入场后真实承受的风险。"]
];

const siteData = window.SITE_DATA || {
  stats: {},
  videoLessons: [],
  materialModules: [],
  importantSources: [],
  chartReferences: []
};

const encyclopediaPatterns = window.PATTERN_ENCYCLOPEDIA || [];
const abChartImages = window.AB_CHART_IMAGES || {};

const chartCoverImageSources = new Set([
  "assets/ab-charts/broad-bear-channel-03.jpg",
  "assets/ab-charts/broad-bull-channel-01.jpg",
  "assets/ab-charts/broad-bull-channel-02.jpg",
  "assets/ab-charts/buy-low-sell-high-range-02.jpg",
  "assets/ab-charts/climactic-reversal-04.jpg",
  "assets/ab-charts/climax-then-trading-range-01.jpg",
  "assets/ab-charts/double-bottom-02.jpg",
  "assets/ab-charts/double-bottom-bull-flag-04.jpg",
  "assets/ab-charts/double-bottom-bull-flag-05.jpg",
  "assets/ab-charts/double-top-01.jpg",
  "assets/ab-charts/double-top-bear-flag-04.jpg",
  "assets/ab-charts/double-top-bear-flag-05.jpg",
  "assets/ab-charts/ema-gap-bar-03.jpg",
  "assets/ab-charts/expanding-triangle-01.jpg",
  "assets/ab-charts/failed-final-flag-breakout-03.jpg",
  "assets/ab-charts/failed-final-flag-breakout-05.jpg",
  "assets/ab-charts/failed-second-entry-05.jpg",
  "assets/ab-charts/failed-signal-bar-01.jpg",
  "assets/ab-charts/high-1-low-1-01.jpg",
  "assets/ab-charts/high-2-bull-flag-01.jpg",
  "assets/ab-charts/high-3-low-3-03.jpg",
  "assets/ab-charts/inside-bar-breakout-02.jpg",
  "assets/ab-charts/lower-low-mtr-02.jpg",
  "assets/ab-charts/major-trend-reversal-bottom-03.jpg",
  "assets/ab-charts/measuring-gap-04.jpg",
  "assets/ab-charts/micro-channel-01.jpg",
  "assets/ab-charts/micro-double-top-bear-flag-02.jpg",
  "assets/ab-charts/nested-wedge-01.jpg",
  "assets/ab-charts/nested-wedge-02.jpg",
  "assets/ab-charts/outside-bar-signal-04.jpg",
  "assets/ab-charts/scale-in-trading-range-05.jpg",
  "assets/ab-charts/scalp-in-trading-range-02.jpg",
  "assets/ab-charts/strong-breakout-follow-through-05.jpg",
  "assets/ab-charts/swing-after-strong-breakout-03.jpg",
  "assets/ab-charts/trend-from-the-open-03.jpg",
  "assets/ab-charts/trend-from-the-open-04.jpg",
  "assets/ab-charts/two-legged-pullback-to-ema-04.jpg",
  "assets/ab-charts/wedge-bull-flag-01.jpg",
  "assets/ab-charts/wedge-bull-flag-02.jpg"
]);

const coreTheoryDefinitions = [
  {
    id: "market-cycle",
    title: "市场周期与惯性",
    scope: "先判断环境，再谈形态",
    priority: 100,
    topics: ["市场周期", "趋势与Always In"],
    keywords: ["cycle", "inertia", "trend", "channel", "trading range", "always in", "市场周期", "惯性"],
    thesis: "Brooks 反复强调，价格通常在突破、通道和交易区间之间循环。强趋势里多数反转失败，交易区间里多数突破失败；你先要知道自己站在哪个环境里。",
    rules: [
      "强突破代表市场在重新定价，顺突破方向的交易优先级更高。",
      "通道是弱趋势：仍有方向，但回调开始变深、重叠开始增加。",
      "交易区间是双向市场，边缘交易优于中间交易，追突破要更谨慎。",
      "惯性不是预测，而是默认假设：当前状态会继续，直到反证出现。"
    ],
    mistakes: [
      "看见一根反转 K 就认为趋势结束。",
      "在交易区间中间硬做方向判断。",
      "把通道当作没有方向的矩形区间。"
    ],
    transfer: "任何形态条目都先套这句：它发生在强趋势、弱通道、还是交易区间？背景错了，形态名字再标准也不能提高胜率。"
  },
  {
    id: "always-in",
    title: "Always In 与方向控制权",
    scope: "判断市场必须持仓时偏多还是偏空",
    priority: 98,
    topics: ["趋势与Always In", "市场周期"],
    keywords: ["always in", "ail", "ais", "control", "trend reversal", "方向", "控制权"],
    thesis: "Always In 不是叫你任何时候都持仓，而是训练你判断：如果必须在市场里，只能选多还是空？它把混乱图表压缩成控制权问题。",
    rules: [
      "连续强收盘、浅回调和失败反转，通常说明 Always In 仍在原方向。",
      "真正的方向切换需要反向突破、跟随和原方向测试失败。",
      "强趋势第一波反转多数只是获利了结，不是趋势反转。",
      "当 Always In 不清楚，仓位和目标都要降级。"
    ],
    mistakes: [
      "把 Always In 当成追单信号。",
      "方向刚模糊就急着预测反转。",
      "忽略反向跟随质量，只看是否突破某条线。"
    ],
    transfer: "High 2、Low 2、MTR、楔形都要先问 Always In 有没有改变；没有改变时，逆势形态只能按小概率或短线处理。"
  },
  {
    id: "trader-equation",
    title: "交易者方程：概率、风险、回报",
    scope: "胜率不能脱离止损和目标",
    priority: 96,
    topics: ["交易管理", "订单与止损", "市场周期"],
    keywords: ["probability", "risk", "reward", "actual risk", "trader's equation", "probability risk reward", "交易者方程"],
    thesis: "Brooks 的胜率口径不是独立数字。任何交易都要同时看概率、实际风险、目标空间和管理方式；方向看对但止损太远，也可能不是好交易。",
    rules: [
      "高概率通常伴随更差价格或更远止损，不能只看命中率。",
      "实际风险是入场后市场真正给你的风险，常常小于理论止损，也可能突然扩大。",
      "目标太近时，低胜率反转没有交易价值；目标足够远时，40% 也可能能做。",
      "交易前先知道退出条件，而不是进场后再找理由。"
    ],
    mistakes: [
      "把 60% 胜率理解成每次都该做。",
      "只背形态胜率，不计算止损距离。",
      "盈利后没有按背景决定是波段持有还是快速兑现。"
    ],
    transfer: "形态百科里的胜率排名只是入口；真正筛选时，把该形态的止损、目标和失效条件一起读。"
  },
  {
    id: "orders-stops",
    title: "订单、入场、止损与实际风险",
    scope: "把观点变成可执行交易",
    priority: 94,
    topics: ["订单与止损", "K线与信号", "交易管理"],
    keywords: ["entry", "stop", "protective stop", "signal bar", "entry bar", "actual risk", "limit order", "stop order"],
    thesis: "Brooks 会把入场讲得非常具体：信号 K、入场 K、止损位置、实际风险、是否允许回撤。因为价格行为不是观点比赛，而是订单执行问题。",
    rules: [
      "信号 K 只提供触发条件，入场后是否有跟随才决定质量。",
      "止损通常放在结构外，而不是放在心理舒服的位置。",
      "大信号 K 可能方向清楚但风险太大，需要等回调或缩小仓位。",
      "限价单适合区间思路，止损单更常用于突破和顺势触发。"
    ],
    mistakes: [
      "信号 K 漂亮就入场，却没有计划止损。",
      "入场 K 立刻反向还继续找理由。",
      "把止损放得太近，结果被正常噪音扫出。"
    ],
    transfer: "每个形态模块都可以按同一流程落地：触发在哪里，结构止损在哪里，触发后第一根入场 K 是否支持你的方向。"
  },
  {
    id: "signal-context",
    title: "信号 K 必须服从背景",
    scope: "单根 K 线不能独立下结论",
    priority: 92,
    topics: ["K线与信号", "市场周期", "突破"],
    keywords: ["signal bar", "entry bar", "tail", "close", "bar", "context", "信号K"],
    thesis: "课程里大量信号 K 的讨论其实都在讲同一件事：K 线质量要和位置、背景、左侧压力、目标空间一起判断。漂亮信号出现在错误位置，仍然是差交易。",
    rules: [
      "强信号通常收在极端，并且出现在关键位置。",
      "尾巴多、实体小、重叠多，通常说明双方都不愿意承诺。",
      "在区间边缘，一般信号也可能足够；在区间中间，漂亮信号也要降级。",
      "信号后没有跟随，就是市场没有确认你的判断。"
    ],
    mistakes: [
      "只看蜡烛形状，不看它左边发生了什么。",
      "把每根外包 K、内包 K 都当成交易信号。",
      "忽略信号 K 太大导致风险收益变差。"
    ],
    transfer: "百科图里的中文标注会提示背景、触发、止损和目标；读图时不要只盯买卖框，要回看信号出现的位置。"
  },
  {
    id: "trading-range",
    title: "交易区间的买低卖高原则",
    scope: "区间里多数突破会失败",
    priority: 90,
    topics: ["交易区间", "突破", "交易管理"],
    keywords: ["trading range", "range", "failed breakout", "buy low sell high", "ttr", "区间"],
    thesis: "Brooks 对交易区间的核心提醒很朴素：多空都能赚钱，追突破的人经常被困。区间中间信息最差，边缘和失败突破才是重点。",
    rules: [
      "区间高位优先寻找做空或获利了结，低位优先寻找做多或空头回补。",
      "突破没有连续跟随，往往会回到区间。",
      "窄区间里不要反复追高杀低，等待更清楚的边缘或突破跟随。",
      "区间里的目标要务实，先看中线，再看另一侧。"
    ],
    mistakes: [
      "把区间里的大阳线当成趋势开始。",
      "在中间位置做满仓方向单。",
      "突破失败后还坚持原突破方向。"
    ],
    transfer: "失败突破、双顶双底、第二次入场等形态，在交易区间语境下比在强趋势中更有意义。"
  },
  {
    id: "breakout-follow-through",
    title: "突破必须看跟随",
    scope: "突破不是穿过去，而是站得住",
    priority: 88,
    topics: ["突破", "趋势与Always In", "K线与信号"],
    keywords: ["breakout", "follow-through", "gap", "breakout pullback", "failed breakout", "突破", "跟随"],
    thesis: "Brooks 讲突破时，重点不是某一根 K 突破了线，而是突破后有没有更多交易者愿意在突破方向继续成交。跟随决定突破是真的还是陷阱。",
    rules: [
      "强突破常见大实体、收盘靠近极端、后续回调浅。",
      "突破后 1-3 根 K 如果马上回到原区间，要按失败突破处理。",
      "突破回踩成功，通常比第一根突破更容易管理风险。",
      "高潮式突破可能短期成功，但追在末端要降低目标。"
    ],
    mistakes: [
      "只要穿过线就追，忽略收盘和后续 K。",
      "突破已经过远，还用原始止损硬追。",
      "失败突破回到区间后不愿意反向思考。"
    ],
    transfer: "强突破、突破回踩、测量缺口、开盘趋势日都围绕同一个问题：突破后是否持续被接受。"
  },
  {
    id: "support-magnets",
    title: "支撑阻力、磁力位和测量移动",
    scope: "位置决定交易是否值得做",
    priority: 86,
    topics: ["支撑阻力/磁力", "测量移动", "开盘与日内"],
    keywords: ["support", "resistance", "magnet", "measured move", "target", "open", "yesterday", "磁力", "测量移动"],
    thesis: "支撑阻力和磁力位告诉你市场会在哪里关注价格，不直接告诉你买卖方向。测量移动是目标框架，不是入场理由。",
    rules: [
      "前高低、开盘价、昨日高低、均线、趋势线和测量目标都会吸引价格。",
      "到达磁力位后，先观察突破、失败还是横盘。",
      "测量移动适合规划目标和止盈，不应单独触发交易。",
      "关键位置越明显，越容易引发获利了结和反向尝试。"
    ],
    mistakes: [
      "画太多线，导致任何位置都像关键位。",
      "价格一到支撑阻力就立刻反向。",
      "目标位太近还追单，风险收益不够。"
    ],
    transfer: "读任何 AB 原图时先找位置：它是在磁力位附近触发，还是在没有空间的中间地带触发。"
  },
  {
    id: "reversal-process",
    title: "反转是过程，不是猜顶底",
    scope: "MTR、楔形、高潮都要等证据",
    priority: 84,
    topics: ["反转/MTR", "楔形/三推", "末端旗形/高潮"],
    keywords: ["major trend reversal", "mtr", "wedge", "climax", "final flag", "second entry", "反转"],
    thesis: "Brooks 讲反转时最防新手冲动：真正反转通常需要原趋势过度、趋势线被破、测试失败、二次信号或强反向跟随。第一根反向 K 很少足够。",
    rules: [
      "强趋势中第一次反转常是小回调，不能直接当 MTR。",
      "MTR 更像三步过程：破趋势线，测试极端失败，再出现二次信号。",
      "楔形和高潮强调动能衰竭，但仍需要触发和跟随。",
      "反转交易概率低于顺势，但目标足够时可以成立。"
    ],
    mistakes: [
      "因为涨多了就做空，跌多了就做多。",
      "看到三推就忽略趋势强度。",
      "没有二次信号也强行预测趋势结束。"
    ],
    transfer: "MTR、楔形、末端旗形、高潮反转都不要孤立记，统一按“原趋势证据减弱 + 反向证据增强”来读。"
  },
  {
    id: "open-day-structure",
    title: "开盘与日内结构",
    scope: "一天的早期信息决定交易节奏",
    priority: 78,
    topics: ["开盘与日内", "市场周期", "突破"],
    keywords: ["open", "opening reversal", "gap", "trend from the open", "day", "开盘"],
    thesis: "开盘课里有大量不绑定单张图的规则：开盘会测试昨日高低、缺口、开盘价和均线；早期强突破可能定义全天，早期失败则容易进入区间。",
    rules: [
      "开盘前几根 K 的强弱、尾巴和重叠，决定当天先按趋势日还是区间日处理。",
      "强开盘突破有跟随时，不要太早逆势猜回补缺口。",
      "开盘测试关键位失败，可能形成当天第一段主波段。",
      "午后交易要考虑当天已经形成的高低点和磁力位。"
    ],
    mistakes: [
      "开盘波动大就立刻反向。",
      "忽略昨日高低点、缺口和开盘价。",
      "趋势日里用区间目标太早出场，区间日里用趋势目标硬扛。"
    ],
    transfer: "开盘反转、趋势开盘、缺口测试和当天测量移动，都先按日内结构看，而不是只按单个形态名看。"
  },
  {
    id: "process-psychology",
    title: "交易流程与心理纪律",
    scope: "减少冲动和二次错误",
    priority: 74,
    topics: ["交易系统/心理", "交易管理", "术语基础"],
    keywords: ["discipline", "psychology", "plan", "management", "system", "心理", "流程"],
    thesis: "Brooks 的课程不是只教形态，也一直在训练流程：等待、放弃、缩小仓位、接受小亏、避免在低质量位置重复交易。心理纪律来自清楚的规则。",
    rules: [
      "交易前写清楚背景、入场、止损、目标和失效，不在入场后补理由。",
      "连续亏损通常说明环境判断错了，先暂停而不是加速追回。",
      "不清楚时降低频率；错过交易比在坏位置进场更容易修复。",
      "复盘要统计同一类错误，而不是只看单笔盈亏。"
    ],
    mistakes: [
      "错过一笔后追在最差位置。",
      "亏损后把短线交易改成波段幻想。",
      "每天换一种形态重点，无法积累样本。"
    ],
    transfer: "这个模块是所有形态的底层执行层：当百科条目给出条件时，你只做满足条件的样本，不用每张图都交易。"
  }
];

const exampleAtlas = [
  {
    id: "breakout-follow-through",
    title: "强突破 + 跟随",
    pattern: "突破",
    probability: "60-70%+",
    diagram: "breakout",
    color: "#087f8c",
    source: "核心课 Trading Breakouts / 10种最佳形态",
    read: ["突破前有清晰阻力或区间边界。", "突破K实体大、收盘靠近高位。", "后续K线继续收在突破方向，说明追单方没有立刻被套。"],
    entry: "顺突破方向入场，或等待第一次小回调；止损通常放在突破K或回调结构外。",
    invalid: "突破后立刻回到区间、连续小实体无跟随，或突破已经是高潮末端。"
  },
  {
    id: "failed-breakout-range",
    title: "交易区间失败突破",
    pattern: "交易区间",
    probability: "55-60%",
    diagram: "range",
    color: "#637f35",
    source: "核心课 Trading Ranges / Steven 区间突破失败",
    read: ["区间内重叠多、尾巴多。", "价格冲出边界后没有跟随。", "反向K线把价格拉回区间，追突破者被困住。"],
    entry: "回到区间后顺反向交易，目标先看区间中线，再看另一侧。",
    invalid: "突破有连续跟随，或区间已经转为强趋势日。"
  },
  {
    id: "high-two-bull-flag",
    title: "High 2 多头旗",
    pattern: "回调",
    probability: "60%左右",
    diagram: "h2l2",
    color: "#315f93",
    source: "核心课 Pullbacks and Bar Counting",
    read: ["背景是清晰上涨趋势。", "两段下跌回调都没有改变 Always In Long。", "第二次向上触发代表空头再次失败。"],
    entry: "第二次向上突破信号K高点入场，止损放在回调低点下方。",
    invalid: "回调太深、跌破关键支撑，或进入交易区间中间硬数K。"
  },
  {
    id: "low-two-bear-flag",
    title: "Low 2 空头旗",
    pattern: "回调",
    probability: "60%左右",
    diagram: "h2l2",
    color: "#5f6f84",
    source: "核心课 Pullbacks and Bar Counting",
    read: ["背景是清晰下跌趋势。", "两段反弹都无法形成强多头跟随。", "第二次向下触发后，空头重新控制。"],
    entry: "第二次向下突破信号K低点入场，止损放在回调高点上方。",
    invalid: "反弹突破趋势线并形成强多头收盘，说明空头趋势可能已经坏掉。"
  },
  {
    id: "major-trend-reversal-top",
    title: "MTR 顶部反转",
    pattern: "反转/MTR",
    probability: "约40%",
    diagram: "mtr",
    color: "#5f6f84",
    source: "核心课 Major Trend Reversals / Trading MTR Tops",
    read: ["先有清晰上涨趋势。", "趋势线被突破，说明趋势控制权松动。", "回测前高失败，并出现第二次做空信号。"],
    entry: "第二次反转信号触发后试空，目标通常先看两段下跌或均线附近。",
    invalid: "没有趋势线突破、没有测试失败，或强多头继续创新高。"
  },
  {
    id: "major-trend-reversal-bottom",
    title: "MTR 底部反转",
    pattern: "反转/MTR",
    probability: "约40%",
    diagram: "mtr",
    color: "#087f8c",
    source: "核心课 Trading MTR Bottoms",
    read: ["先有清晰下跌趋势。", "突破下降趋势线后，价格回测低点失败。", "二次做多信号出现，空头无法继续。"],
    entry: "第二次反转信号触发后试多，止损放在测试低点下方。",
    invalid: "空头仍有强跟随，或反弹只是紧密空头通道中的小回调。"
  },
  {
    id: "wedge-third-push",
    title: "楔形第三推失败",
    pattern: "楔形/三推",
    probability: "40-60%",
    diagram: "wedge",
    color: "#b94738",
    source: "核心课 Wedges / Steven 三推反转",
    read: ["三次推进逐渐靠近通道线或磁力位。", "第三推看似突破，但收盘和跟随变差。", "反向信号出现后，市场常至少回调两段。"],
    entry: "第三推失败后用反向信号试单，保守者等突破微型趋势线。",
    invalid: "第三推后仍连续强收盘，说明趋势并未耗尽。"
  },
  {
    id: "final-flag-failure",
    title: "末端旗形失败",
    pattern: "末端旗形",
    probability: "约40%",
    diagram: "finalflag",
    color: "#a76f22",
    source: "核心课 Final Flags / Steven 高潮反转",
    read: ["趋势已经走了很久，接近磁力位。", "小整理看起来像普通旗形。", "继续突破失败后快速反向，暴露趋势方乏力。"],
    entry: "继续失败并反向触发后入场，目标先看均线或两段回调。",
    invalid: "趋势仍处早中段，或旗形突破后有强跟随。"
  },
  {
    id: "climax-reversal",
    title: "高潮后两段回调",
    pattern: "高潮",
    probability: "条件型",
    diagram: "climax",
    color: "#d95d39",
    source: "核心课 Climaxes / Trading Climactic Reversals",
    read: ["连续大实体、缺口或远离均线。", "趋势方获利了结压力增加。", "第一波反向后常出现第二段测试。"],
    entry: "不抢第一根反向K；等失败继续或二次信号更稳。",
    invalid: "高潮后继续出现同方向强跟随，或反向空间不足。"
  },
  {
    id: "tight-bull-channel",
    title: "紧密多头通道",
    pattern: "通道",
    probability: "顺势优先",
    diagram: "channel",
    color: "#087f8c",
    source: "核心课 Trading Tight Bull Channels",
    read: ["回调浅、K线重叠少。", "价格反复贴近通道线，逆势信号没有空间。", "第一次反转多数只是小回调。"],
    entry: "等待回调顺势买，或在强跟随后持有到磁力位。",
    invalid: "通道被强力跌破并形成反向跟随。"
  },
  {
    id: "broad-bear-channel",
    title: "宽幅空头通道",
    pattern: "通道",
    probability: "双向交易",
    diagram: "channel",
    color: "#7b507d",
    source: "核心课 Trading Broad Bear Channels",
    read: ["仍有下行方向，但反弹幅度明显。", "靠近上轨卖出、靠近下轨减仓或看反弹。", "本质更像带方向的交易区间。"],
    entry: "上轨附近出现空头信号后试空，目标更务实。",
    invalid: "下轨追空且空间不足，或强突破上轨转为新趋势。"
  },
  {
    id: "opening-reversal",
    title: "开盘测试后反转",
    pattern: "开盘",
    probability: "55-60%",
    diagram: "opening",
    color: "#d95d39",
    source: "核心课 Trading the Open",
    read: ["开盘快速测试昨日高低点、缺口或开盘价。", "测试后无法继续，出现强反向K。", "反向跟随可能成为当天主波段。"],
    entry: "等测试失败和反向触发，止损放在测试极端外。",
    invalid: "强趋势开盘并持续跟随，不能因为涨跌过快就反向。"
  },
  {
    id: "measured-move-target",
    title: "测量移动目标",
    pattern: "目标管理",
    probability: "目标框架",
    diagram: "measured",
    color: "#b88117",
    source: "核心课 Measured Moves",
    read: ["第一段运动清晰。", "回调后第二段常尝试复制第一段长度。", "目标位附近会有止盈和反向压力。"],
    entry: "测量移动不是单独入场理由，应和突破、回调或反转信号配合。",
    invalid: "目标太近仍追单，或忽略途中强反向信号。"
  },
  {
    id: "magnet-test",
    title: "磁力位测试",
    pattern: "支撑阻力/磁力",
    probability: "条件增强",
    diagram: "magnets",
    color: "#4c7c59",
    source: "核心课 Support and Resistance",
    read: ["前高低、开盘价、均线、趋势线、测量目标都可能吸引价格。", "到位后观察突破、失败还是横盘。", "磁力位只告诉你哪里重要，不直接告诉方向。"],
    entry: "用磁力位过滤交易位置，再等待形态触发。",
    invalid: "画太多线导致任何位置都像关键位。"
  }
];

const state = {
  lesson: Number(localStorage.getItem("activeLesson") || 0),
  pattern: "breakout",
  patternSort: "probability",
  libraryModule: "all",
  libraryTopic: "all",
  libraryLanguage: "all",
  libraryQuery: "",
  activeVideoId: null,
  activeExample: "breakout-follow-through",
  encyclopediaSort: "combined",
  encyclopediaFamily: "all",
  encyclopediaQuery: "",
  activeEncyclopediaId: null
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function init() {
  renderHome();
  renderLessonList();
  renderLesson();
  renderEncyclopediaFilters();
  renderEncyclopedia();
  renderCoreTheory();
  renderVideoFilters();
  renderVideoLibrary();
  renderMaterials();
  renderGlossary();
  bindEvents();
}

function bindEvents() {
  $("#prevLesson").addEventListener("click", () => goLesson(state.lesson - 1));
  $("#nextLesson").addEventListener("click", () => goLesson(state.lesson + 1));
  $("#openPatternLab").addEventListener("click", () => $("#encyclopedia").scrollIntoView({ behavior: "smooth" }));
  $$("[data-encyclopedia-sort]").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      state.encyclopediaSort = link.dataset.encyclopediaSort;
      $("#encyclopediaSort").value = state.encyclopediaSort;
      renderEncyclopedia();
      $("#encyclopedia").scrollIntoView({ behavior: "smooth" });
    });
  });
  $("#encyclopediaSort").addEventListener("change", (event) => {
    state.encyclopediaSort = event.target.value;
    renderEncyclopedia();
  });
  $("#encyclopediaFamily").addEventListener("change", (event) => {
    state.encyclopediaFamily = event.target.value;
    renderEncyclopedia();
  });
  $("#encyclopediaSearch").addEventListener("input", (event) => {
    state.encyclopediaQuery = event.target.value.trim().toLowerCase();
    renderEncyclopedia();
  });
  $("#clearEncyclopediaFilters").addEventListener("click", () => {
    state.encyclopediaSort = "combined";
    state.encyclopediaFamily = "all";
    state.encyclopediaQuery = "";
    $("#encyclopediaSort").value = "combined";
    $("#encyclopediaFamily").value = "all";
    $("#encyclopediaSearch").value = "";
    renderEncyclopedia();
  });
  $("#moduleFilter").addEventListener("change", (event) => {
    state.libraryModule = event.target.value;
    renderVideoLibrary();
  });
  $("#topicFilter").addEventListener("change", (event) => {
    state.libraryTopic = event.target.value;
    renderVideoLibrary();
  });
  $("#languageFilter").addEventListener("change", (event) => {
    state.libraryLanguage = event.target.value;
    renderVideoLibrary();
  });
  $("#videoSearch").addEventListener("input", (event) => {
    state.libraryQuery = event.target.value.trim().toLowerCase();
    renderVideoLibrary();
  });
  $("#clearVideoFilters").addEventListener("click", () => {
    state.libraryModule = "all";
    state.libraryTopic = "all";
    state.libraryLanguage = "all";
    state.libraryQuery = "";
    $("#moduleFilter").value = "all";
    $("#topicFilter").value = "all";
    $("#languageFilter").value = "all";
    $("#videoSearch").value = "";
    renderVideoLibrary();
  });
}

function goLesson(index) {
  if (index < 0 || index >= lessons.length) return;
  state.lesson = index;
  localStorage.setItem("activeLesson", String(index));
  renderHome();
  renderLessonList();
  renderLesson();
}

function renderHome() {
  const chartCount = Object.values(abChartImages).flatMap((items) => normalizeChartItems(items)).length;
  const stats = siteData.stats || {};
  const topPatterns = [...encyclopediaPatterns]
    .sort((a, b) => (b.probScore + b.importance) - (a.probScore + a.importance))
    .slice(0, 3);
  const leadPattern = topPatterns[0] || encyclopediaPatterns[0];

  $("#homeStats").innerHTML = [
    ["图表百科", `${encyclopediaPatterns.length} 个`, "主学习内容"],
    ["AB 原图", `${formatNumber(chartCount)} 张`, "每个形态优先看图"],
    ["视频讲解", `${formatNumber(stats.subtitleFiles || 0)} 份`, "作为形态解释来源"],
    ["系统课程", `${lessons.length} 课`, "只作为辅助路径"]
  ].map(([label, value, note]) => `
    <article class="stat-card searchable" data-search="${html(`${label} ${value} ${note}`)}">
      <span>${html(label)}</span>
      <strong>${html(value)}</strong>
      <p>${html(note)}</p>
    </article>
  `).join("");

  $("#homeContinue").innerHTML = `
    <div class="continue-topline">
      <span>主工作区</span>
      <strong>百科</strong>
    </div>
    <p>${leadPattern ? html(leadPattern.title) : "按形态进入图表百科"}</p>
    <small>先按胜率和重要性选择形态，再看 AB 原图、中文标注、视频课讲解和失效条件。</small>
    <div class="continue-links">
      <a href="#encyclopedia">进入图表百科</a>
      <a href="#encyclopedia">看最高优先级</a>
      <a href="#video-library">查视频来源</a>
    </div>
    <span class="next-lesson">推荐顺序：形态排序 → 原图标注 → 视频总结 → 复盘。</span>
  `;

  $("#homeRoutes").innerHTML = [
    ["01", "查图表百科", "按胜率、重要性、类别和关键词快速定位形态。", "#encyclopedia"],
    ["02", "看 AB 原图", "每个形态先看原始图表和中文标注，别先背概念。", "#encyclopedia"],
    ["03", "读视频讲解", "用 Brooks 课程总结解释这张图为什么成立或失败。", "#video-library"],
    ["04", "补系统课程", "不懂市场背景时，再回课程路径补框架。", "#course"]
  ].map(([step, title, text, href]) => `
    <a class="route-card searchable" href="${href}" data-search="${html(`${step} ${title} ${text}`)}">
      <span>${step}</span>
      <strong>${html(title)}</strong>
      <p>${html(text)}</p>
    </a>
  `).join("");

}

function renderLessonList() {
  $("#lessonCount").textContent = `${lessons.length} 课`;
  $("#lessonList").innerHTML = lessons.map((lesson, index) => `
    <button class="lesson-button searchable ${index === state.lesson ? "active" : ""}" type="button" data-lesson="${index}" data-search="${searchText(lesson)}">
      <span class="lesson-number">${index + 1}</span>
      <span><strong>${lesson.title}</strong><span>${lesson.level} · ${lesson.subtitle}</span></span>
    </button>
  `).join("");
  $$(".lesson-button").forEach((button) => button.addEventListener("click", () => goLesson(Number(button.dataset.lesson))));
}

function renderLesson() {
  const lesson = lessons[state.lesson];
  $("#lessonTitle").textContent = lesson.title;
  $("#lessonContent").innerHTML = `
    <section class="lesson-section callout searchable" data-search="${searchText(lesson)}">
      <h2>${lesson.subtitle}</h2>
      <p>${lesson.intro}</p>
    </section>
    <section class="chart-panel searchable" data-search="${lesson.title} ${lesson.terms.join(" ")}">
      <div class="diagram">${diagramSvg(lesson.diagram, "#087f8c")}</div>
      <div class="lesson-section">
        <h2>本课怎么学</h2>
        <ol>${lesson.read.map((item) => `<li>${item}</li>`).join("")}</ol>
      </div>
    </section>
    <section class="lesson-grid">
      ${lesson.concepts.map(([title, text]) => `
        <article class="concept-card searchable" data-search="${title} ${text}">
          <h3>${title}</h3>
          <p>${text}</p>
        </article>
      `).join("")}
    </section>
    <section class="lesson-section searchable" data-search="${lesson.practice.join(" ")}">
      <h2>本课练习</h2>
      <ul>${lesson.practice.map((item) => `<li>${item}</li>`).join("")}</ul>
    </section>
  `;
  renderQuiz(lesson);
  renderTerms(lesson);
  $("#prevLesson").disabled = state.lesson === 0;
  $("#nextLesson").disabled = state.lesson === lessons.length - 1;
}

function renderQuiz(lesson) {
  $("#quizStatus").textContent = `第 ${state.lesson + 1} 课`;
  $("#quizBox").innerHTML = `
    <p>${lesson.quiz.q}</p>
    ${lesson.quiz.options.map((option, index) => `<button class="quiz-option" type="button" data-answer="${index}">${option}</button>`).join("")}
    <p id="quizExplain" class="quiz-explain"></p>
  `;
  $$(".quiz-option").forEach((button) => {
    button.addEventListener("click", () => {
      const selected = Number(button.dataset.answer);
      $$(".quiz-option").forEach((item) => {
        item.classList.remove("correct", "wrong");
        const idx = Number(item.dataset.answer);
        if (idx === lesson.quiz.answer) item.classList.add("correct");
        if (idx === selected && selected !== lesson.quiz.answer) item.classList.add("wrong");
      });
      $("#quizExplain").textContent = lesson.quiz.explain;
    });
  });
}

function renderTerms(lesson) {
  $("#lessonTerms").innerHTML = lesson.terms.map((term) => `<span>${term}</span>`).join("");
}

function renderEncyclopediaFilters() {
  const families = uniqueSorted(encyclopediaPatterns.map((pattern) => pattern.family));
  $("#encyclopediaFamily").innerHTML = optionList("全部类别", families);
}

function renderEncyclopedia() {
  const rows = sortedEncyclopediaPatterns();
  if (!rows.some((pattern) => pattern.id === state.activeEncyclopediaId)) {
    state.activeEncyclopediaId = rows[0]?.id || encyclopediaPatterns[0]?.id || null;
  }
  const avgProb = rows.length ? Math.round(rows.reduce((sum, item) => sum + item.probScore, 0) / rows.length) : 0;
  const avgImportance = rows.length ? Math.round(rows.reduce((sum, item) => sum + item.importance, 0) / rows.length) : 0;
  $("#encyclopediaStats").innerHTML = [
    ["当前形态", `${formatNumber(rows.length)} 个`, "可点击查阅"],
    ["总收录", `${formatNumber(encyclopediaPatterns.length)} 个`, "覆盖主要课程形态"],
    ["平均胜率分", `${avgProb}`, "用于排序，不是保证"],
    ["平均重要性", `${avgImportance}`, "按学习优先级"]
  ].map(([label, value, note]) => `
    <div class="mini-stat searchable" data-search="${html(`${label} ${value} ${note}`)}">
      <span>${html(label)}</span><strong>${html(value)}</strong><small>${html(note)}</small>
    </div>
  `).join("");

  $("#encyclopediaList").innerHTML = rows.map((pattern, index) => `
    <button class="encyclopedia-row searchable ${pattern.id === state.activeEncyclopediaId ? "active" : ""}" type="button" data-encyclopedia="${pattern.id}" data-search="${html(searchText(pattern))}">
      <strong class="rank-number">${String(index + 1).padStart(2, "0")}</strong>
      <span class="ency-title"><strong>${html(pattern.title)}</strong><em>${html(pattern.family)} · ${html(pattern.winRate)}</em></span>
      <span class="score-pair"><b>${pattern.probScore}</b><small>胜率</small></span>
      <span class="score-pair"><b>${pattern.importance}</b><small>重要性</small></span>
    </button>
  `).join("") || `<div class="empty-state">没有匹配的形态。换一个关键词或清空筛选。</div>`;

  $$(".encyclopedia-row").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeEncyclopediaId = button.dataset.encyclopedia;
      renderEncyclopedia();
    });
  });
  renderEncyclopediaDetail();
}

function renderEncyclopediaDetail() {
  const pattern = encyclopediaPatterns.find((item) => item.id === state.activeEncyclopediaId);
  if (!pattern) {
    $("#encyclopediaDetail").innerHTML = `<div class="empty-state">请选择一个形态。</div>`;
    return;
  }
  const chartItems = normalizeChartItems(abChartImages[pattern.id]);
  const videoInsight = patternVideoInsight(pattern);
  $("#encyclopediaDetail").innerHTML = `
    <div class="pattern-hero encyclopedia-hero searchable" data-search="${html(searchText(pattern))}">
      <div class="diagram">${diagramSvg(pattern.diagram, colorForFamily(pattern.family))}</div>
      <div>
        <div class="pattern-meta">
          <span class="pill">${html(pattern.family)}</span>
          <span class="pill">${html(pattern.winRate)}</span>
          <span class="pill">胜率分 ${pattern.probScore}</span>
          <span class="pill">重要性 ${pattern.importance}</span>
          <span class="pill">难度 ${"●".repeat(pattern.difficulty)}</span>
          <span class="pill">视频课总结</span>
        </div>
        <h3>${html(pattern.title)}</h3>
        <p>${html(pattern.summary)}</p>
        <p class="muted-text">${html(pattern.source)}</p>
        <div class="term-chips">${(pattern.aliases || []).map((alias) => `<span>${html(alias)}</span>`).join("")}</div>
      </div>
    </div>
    ${renderPatternVideoInsight(pattern, videoInsight)}
    ${chartItems.length ? `
      <section class="ab-chart-card searchable" data-search="${html(`${pattern.title} ${chartItems.map((chart) => `${chart.caption} ${chart.source}`).join(" ")}`)}">
        <div class="ab-chart-heading">
          <div>
            <p class="eyebrow">AB Original Chart With Chinese Notes</p>
            <h4>AB 原图中文标注图库</h4>
          </div>
          <span>${chartItems.length} 张中文标注样本</span>
        </div>
        <div class="ab-chart-gallery">
          ${chartItems.map((chart, index) => renderAnnotatedChartFigure(pattern, chart, index, videoInsight)).join("")}
        </div>
      </section>
    ` : `
      <section class="empty-state">这个形态暂时没有匹配到 AB 原图截图。</section>
    `}
  `;
}

function renderCoreTheory() {
  const lessons = siteData.videoLessons || [];
  const stats = siteData.stats || {};
  const modules = coreTheoryDefinitions.map((module) => ({
    ...module,
    sourceScore: module.topics.reduce((sum, topic) => sum + topicLibraryScore(topic), 0),
    lessons: coreTheoryLessons(module)
  }));

  const coveredTopics = uniqueOrdered(coreTheoryDefinitions.flatMap((module) => module.topics));
  $("#coreTheoryStats").innerHTML = [
    ["理论模块", `${coreTheoryDefinitions.length} 个`, "独立于单张图的 Brooks 方法论"],
    ["字幕来源", `${formatNumber(stats.subtitleFiles || lessons.length)} 份`, `覆盖 ${formatNumber(stats.uniqueCourseUnits || lessons.length)} 个课程单元`],
    ["核心主题", `${coveredTopics.length} 类`, coveredTopics.slice(0, 4).join(" / ")],
    ["课程权重", formatNumber(modules.reduce((sum, module) => sum + module.sourceScore, 0)), "按字幕主题得分汇总"]
  ].map(([label, value, note]) => `
    <div class="mini-stat searchable" data-search="${html(`${label} ${value} ${note}`)}">
      <span>${html(label)}</span><strong>${html(value)}</strong><small>${html(note)}</small>
    </div>
  `).join("");

  $("#coreTheoryGrid").innerHTML = modules
    .sort((a, b) => b.priority - a.priority)
    .map((module, index) => renderCoreTheoryCard(module, index))
    .join("");
}

function renderCoreTheoryCard(module, index) {
  const lessonSearch = module.lessons.map((lesson) => searchText(lesson)).join(" ");
  const keywords = uniqueOrdered([...(module.topics || []), ...(module.keywords || [])]).slice(0, 8);
  return `
    <article class="core-theory-card searchable" data-search="${html(`${searchText(module)} ${lessonSearch}`)}">
      <div class="core-theory-top">
        <span>${String(index + 1).padStart(2, "0")}</span>
        <strong>重要性 ${module.priority}</strong>
      </div>
      <div class="core-theory-head">
        <div>
          <p class="eyebrow">${html(module.scope)}</p>
          <h3>${html(module.title)}</h3>
        </div>
        <div class="term-chips">${keywords.map((item) => `<span>${html(item)}</span>`).join("")}</div>
      </div>
      <p class="core-thesis">${html(module.thesis)}</p>
      <div class="theory-columns">
        <section>
          <h4>课程提炼</h4>
          <ul>${module.rules.map((item) => `<li>${html(item)}</li>`).join("")}</ul>
        </section>
        <section>
          <h4>常见误读</h4>
          <ul>${module.mistakes.map((item) => `<li>${html(item)}</li>`).join("")}</ul>
        </section>
      </div>
      <div class="theory-transfer">
        <span>套到形态百科时怎么用</span>
        <p>${html(module.transfer)}</p>
      </div>
      ${module.lessons.length ? `
        <div class="theory-source-list">
          <div class="related-heading">
            <h5>对应视频课摘要</h5>
            <span>${html(module.topics.join(" / "))}</span>
          </div>
          ${module.lessons.slice(0, 5).map((lesson) => `
            <article class="theory-source-row">
              <span>${html(lesson.module)} · ${html(lesson.language)} · ${formatDuration(lesson.minutesEstimate || 0)}</span>
              <strong>${html(lesson.title)}</strong>
              <p>${html(lesson.summary)}</p>
            </article>
          `).join("")}
        </div>
      ` : ""}
    </article>
  `;
}

function coreTheoryLessons(module) {
  return (siteData.videoLessons || [])
    .map((lesson) => ({ lesson, score: coreTheoryLessonScore(lesson, module) }))
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || (b.lesson.wordUnits || 0) - (a.lesson.wordUnits || 0))
    .slice(0, 6)
    .map((item) => item.lesson);
}

function coreTheoryLessonScore(lesson, module) {
  const lessonTopics = lesson.topics || [];
  const text = searchText(lesson).toLowerCase();
  let score = 0;
  (module.topics || []).forEach((topic) => {
    if (lessonTopics.includes(topic)) score += 45;
    if (text.includes(topic.toLowerCase())) score += 10;
  });
  (module.keywords || []).forEach((keyword) => {
    if (text.includes(String(keyword).toLowerCase())) score += 8;
  });
  if (lesson.language === "中文") score += 3;
  if (String(lesson.module || "").includes("核心")) score += 2;
  return score;
}

function topicLibraryScore(topic) {
  const item = (siteData.stats?.topTopics || []).find((row) => row.topic === topic);
  return item?.score || 0;
}

function patternVideoInsight(pattern) {
  const lessons = siteData.videoLessons || [];
  const stats = siteData.stats || {};
  const terms = patternSearchTerms(pattern);
  const scored = lessons
    .map((lesson) => ({ lesson, score: lessonRelevanceScore(lesson, pattern, terms) }))
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || b.lesson.wordUnits - a.lesson.wordUnits)
    .slice(0, 10);
  const related = scored.length ? scored.map((item) => item.lesson) : lessons.slice(0, 8);
  const bullets = uniqueOrdered(related.flatMap((lesson) => lesson.bullets || [])).slice(0, 6);
  const topics = topTopicLabels(related).slice(0, 5);
  const primaryLesson = related[0];
  const checklist = [
    { label: "背景", value: firstText(pattern.best) },
    { label: "触发", value: firstText(pattern.entry) },
    { label: "止损", value: firstText(pattern.stop) },
    { label: "目标", value: firstText(pattern.target) },
    { label: "放弃", value: firstText(pattern.traps) }
  ];
  return {
    subtitleFiles: stats.subtitleFiles || lessons.length,
    courseUnits: stats.uniqueCourseUnits || lessons.length,
    relatedCount: scored.length || related.length,
    topics,
    bullets,
    related,
    primaryLesson,
    thesis: familyVideoThesis(pattern),
    patternFocus: patternCourseFocus(pattern),
    checklist,
    sequence: [
      `先判断市场周期：趋势、通道、交易区间，不能只因为看见 ${pattern.title} 就下结论。`,
      `再确认位置：${firstText(pattern.best)}`,
      `然后等触发：${firstText(pattern.entry)}`,
      `最后检查交易者方程：止损看 ${firstText(pattern.stop)}，目标先看 ${firstText(pattern.target)}。`
    ],
    mistakes: uniqueOrdered([
      firstText(pattern.traps),
      ...bullets
    ]).slice(0, 5),
    warning: firstText(pattern.traps)
  };
}

function renderPatternVideoInsight(pattern, insight) {
  return `
    <section class="video-insight-card course-insight searchable" data-search="${html(`${pattern.title} ${insight.thesis} ${insight.patternFocus} ${insight.sequence.join(" ")} ${insight.bullets.join(" ")}`)}">
      <div class="template-heading">
        <div>
          <p class="eyebrow">Al Brooks Video Course Notes</p>
          <h4>视频课讲解总结：怎么理解 ${html(pattern.title)}</h4>
        </div>
        <span>匹配 ${formatNumber(insight.relatedCount)} 节相关课 · 全库 ${formatNumber(insight.subtitleFiles)} 份字幕</span>
      </div>
      <div class="course-insight-main">
        <article class="course-thesis">
          <span>01</span>
          <h5>Brooks 讲这类形态真正想让你抓住什么</h5>
          <p>${html(insight.thesis)}</p>
          <p>${html(insight.patternFocus)}</p>
        </article>
        <article class="course-checklist">
          <span>02</span>
          <h5>套到这个形态，入场前按这 5 句检查</h5>
          <div class="course-check-grid">
            ${insight.checklist.map((item) => `
              <div>
                <strong>${html(item.label)}</strong>
                <p>${html(item.value)}</p>
              </div>
            `).join("")}
          </div>
        </article>
      </div>
      <div class="course-insight-layout">
        <article>
          <h5>按课程思路读图的顺序</h5>
          <ol>${insight.sequence.map((item) => `<li>${html(item)}</li>`).join("")}</ol>
        </article>
        <article>
          <h5>这一形态最容易学错的地方</h5>
          <ul>${insight.mistakes.map((item) => `<li>${html(item)}</li>`).join("")}</ul>
        </article>
      </div>
      <div class="related-video-lessons">
        <div class="related-heading">
          <h5>相关视频课摘要</h5>
          <span>${insight.topics.map((topic) => html(topic)).join(" / ")}</span>
        </div>
        <div class="related-video-grid">
          ${insight.related.slice(0, 6).map((lesson) => `
            <article class="related-video-card">
              <span>${html(lesson.module)} · ${html(lesson.language)}</span>
              <strong>${html(lesson.title)}</strong>
              <p>${html(lesson.summary)}</p>
              ${(lesson.bullets || []).length ? `<ul>${lesson.bullets.slice(0, 3).map((item) => `<li>${html(item)}</li>`).join("")}</ul>` : ""}
              <small>${html((lesson.topics || []).slice(0, 4).join(" / "))}</small>
            </article>
          `).join("")}
        </div>
      </div>
    </section>
  `;
}

function patternCourseFocus(pattern) {
  return `放到 ${pattern.title} 上，学习重点不是把名字背下来，而是看它是否同时满足 Brooks 反复讲的四件事：背景合适、位置有优势、触发后有跟随、风险收益划算。这个形态的第一判断句是：${firstText(pattern.best)}；真正的触发句是：${firstText(pattern.entry)}。`;
}

function patternSearchTerms(pattern) {
  const familyTerms = {
    "突破": ["breakout", "breakouts", "follow-through", "breakout pullback", "failed breakout", "突破", "跟随"],
    "回调": ["pullback", "pullbacks", "bar counting", "high 2", "low 2", "h2", "l2", "回调", "数K"],
    "交易区间": ["trading range", "range", "tight trading range", "tr", "ttr", "交易区间", "区间"],
    "通道": ["channel", "channels", "broad channel", "tight channel", "通道"],
    "趋势": ["trend", "trends", "always in", "always-in", "趋势"],
    "反转/MTR": ["major trend reversal", "mtr", "reversal", "trend reversal", "反转"],
    "楔形": ["wedge", "wedges", "three pushes", "三推", "楔形"],
    "末端旗形": ["final flag", "final flags", "末端旗形"],
    "双顶双底": ["double top", "double bottom", "dt", "db", "双顶", "双底"],
    "三角形": ["triangle", "triangles", "三角形"],
    "头肩": ["head and shoulders", "头肩"],
    "圆弧": ["rounding", "rounded", "圆弧"],
    "高潮": ["climax", "climaxes", "buy climax", "sell climax", "高潮"],
    "缺口": ["gap", "gaps", "measuring gap", "breakaway gap", "缺口"],
    "开盘": ["open", "opening", "first hour", "开盘"],
    "目标/磁力": ["magnet", "measured move", "support and resistance", "目标", "磁力", "测量移动"],
    "K线信号": ["signal bar", "entry bar", "outside bar", "inside bar", "信号K"],
    "失败形态": ["failed", "failure", "trap", "失败", "陷阱"],
    "入场逻辑": ["entry", "entries", "stop order", "limit order", "入场"],
    "交易管理": ["management", "scalp", "swing", "actual risk", "risk", "管理"]
  };
  return uniqueOrdered([
    pattern.title,
    pattern.family,
    pattern.diagram,
    pattern.source,
    ...(pattern.aliases || []),
    ...(familyTerms[pattern.family] || []),
    ...String(pattern.title).split(/[ /+]+/),
    ...String(pattern.source || "").match(/PAF\s*\d+[A-Z]?|HTT\s*\d+/gi) || []
  ].map((term) => String(term || "").trim()).filter((term) => term.length > 1));
}

function lessonRelevanceScore(lesson, pattern, terms) {
  const text = searchText(lesson).toLowerCase();
  let score = 0;
  terms.forEach((term) => {
    const normalized = term.toLowerCase();
    if (!normalized) return;
    if (text.includes(normalized)) score += normalized.length > 8 ? 12 : 7;
  });
  if ((lesson.topics || []).some((topic) => topicMatchesFamily(topic, pattern.family))) score += 18;
  if (String(pattern.source || "").toLowerCase().includes(String(lesson.title || "").toLowerCase().slice(0, 8))) score += 12;
  return score;
}

function topicMatchesFamily(topic, family) {
  const map = {
    "突破": ["突破", "市场周期"],
    "回调": ["回调与数K", "趋势与Always In"],
    "交易区间": ["交易区间", "市场周期"],
    "通道": ["通道", "趋势与Always In"],
    "趋势": ["趋势与Always In", "市场周期"],
    "反转/MTR": ["反转/MTR", "趋势与Always In"],
    "楔形": ["楔形/三推"],
    "末端旗形": ["末端旗形/高潮"],
    "高潮": ["末端旗形/高潮"],
    "缺口": ["突破", "开盘与日内"],
    "开盘": ["开盘与日内"],
    "目标/磁力": ["支撑阻力/磁力", "测量移动"],
    "K线信号": ["K线与信号"],
    "失败形态": ["突破", "反转/MTR"],
    "入场逻辑": ["订单与止损", "交易管理"],
    "交易管理": ["交易管理", "订单与止损"]
  };
  return (map[family] || []).includes(topic);
}

function familyVideoThesis(pattern) {
  const thesis = {
    "突破": "视频课里 Brooks 反复强调，突破本身不是证据，突破后的跟随才是证据；在交易区间里，多数突破尝试会失败，只有强收盘和后续K线继续推进，概率才会上升。",
    "回调": "Brooks 讲回调时，核心是原趋势是否仍然控制市场。High 2、Low 2 和两段回调不是机械数K，而是看逆势方两次尝试失败后，顺势方是否重新接管。",
    "交易区间": "交易区间课程的主线是买低卖高、边缘优于中间、目标要务实。区间里双方都能赚钱，但追突破的一方更容易在失败突破里被困住。",
    "通道": "通道相关视频强调趋势仍存在，但推进方式更重叠、更容易双向交易。通道末端要降低顺势追单预期，更多等待通道线、均线或前高低附近的二次信号。",
    "趋势": "趋势视频的核心是 Always In 控制权。强趋势里第一反转大多只是回调，顺势交易优先，逆势交易必须等结构破坏、测试失败和二次证据。",
    "反转/MTR": "主要趋势反转不是猜顶底。Brooks 通常要求先有趋势线突破，再有回测原极端失败，最后有二次信号或更高低点/更低高点，才把反转当成交易计划。",
    "楔形": "楔形和三推视频强调动能衰竭，但衰竭不等于立刻反转。顺大趋势的楔形旗形通常比逆大趋势的楔形反转更可靠，第三推后的跟随决定质量。",
    "末端旗形": "末端旗形在视频里常被当作趋势末期陷阱：它看起来像顺势整理，但如果突破没有跟随、很快回到旗形内，就说明最后一批追单者可能被套住。",
    "高潮": "高潮课程强调远离均线、连续大K和情绪化推进后，市场常进入横盘或两段回调。高潮后不要默认立刻反转，也不要在末端追最差价格。",
    "缺口": "缺口视频强调重新定价和测试。缺口不被回补且有跟随时可能成为测量缺口；快速回补则说明缺口方向没有控制权。",
    "开盘": "开盘视频强调速度、昨日高低点、开盘价和早盘失败。开盘形态不能脱离日内磁力位，强开盘会形成趋势日，失败开盘会快速回到区间。",
    "目标/磁力": "支撑阻力和测量移动课程强调，磁力位告诉你价格可能被吸引的位置，不直接告诉方向；真正的交易要等到位后的突破、失败或反转证据。",
    "K线信号": "信号K课程强调单根漂亮K线不能脱离背景。信号K只提供触发，位置、左侧结构和入场K跟随才决定它是否值得交易。",
    "失败形态": "失败形态在 Brooks 体系里很重要，因为被困交易者会成为反向燃料。失败是否成立，要看突破或反转尝试后是否快速回到原结构内，并出现反向跟随。",
    "入场逻辑": "入场课程强调订单方式必须匹配市场速度。止损单适合突破和强趋势，限价单多用于区间边缘；入场后没有跟随，要快速降低预期。",
    "交易管理": "交易管理视频反复讲实际风险、目标距离、手续费和滑点。看对方向不等于能赚钱，只有概率、风险和回报同时合格，交易者方程才成立。"
  };
  return thesis[pattern.family] || `视频课里 Brooks 对 ${pattern.title} 的共同要求是先判断市场周期，再看位置和信号，最后用实际风险与目标距离决定是否值得交易。`;
}

function topTopicLabels(lessons) {
  const counts = lessons.reduce((acc, lesson) => {
    (lesson.topics || []).forEach((topic) => {
      acc[topic] = (acc[topic] || 0) + 1;
    });
    return acc;
  }, {});
  return Object.entries(counts).sort((a, b) => b[1] - a[1]).map(([topic]) => topic);
}

function uniqueOrdered(values) {
  const seen = new Set();
  return values.filter((value) => {
    const key = String(value || "").trim().toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function renderAnnotatedChartFigure(pattern, chart, index, videoInsight) {
  const rawSrc = chart.src || "";
  const annotatedSrc = annotatedChartSrc(chart);
  const lesson = chartTeachingNote(pattern, chart, index, videoInsight);
  return `
    <figure class="annotated-figure searchable" data-search="${html(`${pattern.title} ${lesson.title} ${lesson.summary} ${lesson.points.join(" ")} ${chart.caption || ""}`)}">
      <div class="annotated-chart">
        <a href="${html(annotatedSrc)}" target="_blank" rel="noreferrer">
          <img src="${html(annotatedSrc)}" alt="${html(pattern.title)} AB 原图中文标注 ${index + 1}" ${index > 1 ? 'loading="lazy"' : ""} onerror="this.onerror=null;this.src='${html(rawSrc)}';" />
        </a>
        <span class="chart-stamp">中文标注版 · 样本 ${index + 1}</span>
      </div>
      <figcaption>
        <span>${html(chart.source)} · p.${html(chart.page)} · ${html(pattern.title)}</span>
        <a href="${html(rawSrc)}" target="_blank" rel="noreferrer">打开无标注原图</a>
      </figcaption>
      <div class="chart-lesson-card">
        <div class="chart-lesson-head">
          <span>${html(lesson.badge)}</span>
          <strong>${html(lesson.title)}</strong>
        </div>
        <p>${html(lesson.summary)}</p>
        <div class="chart-lesson-points">
          ${lesson.points.map((point) => `<p>${html(point)}</p>`).join("")}
        </div>
        <small>${html(lesson.source)}</small>
      </div>
    </figure>
  `;
}

function chartTeachingNote(pattern, chart, index, videoInsight) {
  const lens = chartLessonLens(index);
  const family = chartFamilyPrinciple(pattern.family);
  const related = videoInsight?.related || [];
  const relatedLesson = related.length ? related[index % related.length] : null;
  const relatedBullet = relatedLesson?.bullets?.length ? relatedLesson.bullets[index % relatedLesson.bullets.length] : "";
  const source = relatedLesson
    ? `相关视频课摘要：${relatedLesson.title}；本图来自图表百科 p.${chart.page}。`
    : `课程来源：${pattern.source}；本图来自图表百科 p.${chart.page}。`;

  return {
    badge: `样本 ${index + 1} · ${lens.badge}`,
    title: lens.title(pattern, family),
    summary: lens.summary(pattern, family, index),
    points: uniqueOrdered([
      lens.point(pattern, family),
      family.point(pattern, index),
      relatedBullet ? `视频课联想：${relatedBullet}` : family.fallback(pattern)
    ]).slice(0, 3),
    source
  };
}

function chartLessonLens(index) {
  const lenses = [
    {
      badge: "背景",
      title: () => "先判断形态是否出现在高质量位置",
      summary: (pattern, family) => `Brooks 讲形态时通常先问市场环境，而不是先问名字。这张图适合练习：左侧是否已经给出 ${firstPaText(pattern.best)}，以及这个位置是否真的让 ${pattern.title} 的概率变高。`,
      point: (pattern) => `读图动作：遮住右半边，只看入场前的背景；如果只剩形态名称而没有位置优势，这笔交易就不该升级。`
    },
    {
      badge: "触发",
      title: (pattern) => `看信号K之后有没有真正触发`,
      summary: (pattern) => `Brooks 不会因为“看起来像”就交易，他要看到信号K和入场K。此图重点是把 ${firstPaText(pattern.entry)} 和后续跟随连起来看，而不是孤立地看一根漂亮K线。`,
      point: (pattern) => `读图动作：找到信号K、入场K和入场后第一两根K；如果入场后没有跟随，就把预期从波段降到小目标或直接放弃。`
    },
    {
      badge: "管理",
      title: () => "把止损和目标放回同一张图里看",
      summary: (pattern) => `这张图下面不再只背“止损、目标”，而是看交易者方程：止损若在 ${firstPaText(pattern.stop)}，目标至少要能看到 ${firstPaText(pattern.target)}，否则方向看对也可能不是好交易。`,
      point: () => "读图动作：先量入场点到止损，再量入场点到最近磁力位；如果目标太近，Brooks 通常会降低仓位、等更好价格，或不交易。"
    },
    {
      badge: "陷阱",
      title: (pattern) => `这张图用来识别 ${pattern.title} 的失效点`,
      summary: (pattern) => `Brooks 很重视失败形态，因为被套交易者会制造反向燃料。这里要练的是：什么情况下 ${pattern.title} 不再成立，尤其是 ${firstPaText(pattern.traps)}。`,
      point: () => "读图动作：不要只标出理想入场，也要标出哪一根K之后你的交易理由消失；理由消失时，不要用希望代替规则。"
    },
    {
      badge: "复盘",
      title: () => "用这张图复盘 Brooks 的读图顺序",
      summary: (pattern, family) => `这张图适合做完整复盘：先定市场周期，再看位置，等触发，最后看风险收益。${family.core} 这个顺序比单独记住 ${pattern.title} 更重要。`,
      point: () => "读图动作：用一句话写下“为什么现在多头或空头更有优势”；写不出来，就说明图还没有读清楚。"
    }
  ];
  return lenses[index % lenses.length];
}

function firstPaText(value) {
  return priceActionPhrase(firstText(value));
}

function priceActionPhrase(value) {
  return String(value || "")
    .replace(/清晰支撑阻力、区间高低点或趋势线被突破/g, "关键支撑/阻力被有效突破")
    .replace(/突破K实体大，收盘靠近极端/g, "突破K实体大，收盘强")
    .replace(/后续1-3根K没有立刻回到原区间/g, "后续K线不回到原区间")
    .replace(/突破K另一端/g, "突破K另一侧")
    .replace(/信号K另一端/g, "信号K另一侧")
    .replace(/测量移动/g, "测量目标")
    .replace(/交易区间中间硬数H2/g, "交易区间中段不要硬数H2")
    .replace(/把区间中间波动当L2/g, "交易区间中段不要硬数L2")
    .replace(/趋势已经坏掉仍买/g, "趋势结构已坏仍买入")
    .replace(/反弹已转多仍卖/g, "反弹转强仍卖出")
    .replace(/信号K太大导致风险收益差/g, "信号K过大，盈亏比变差")
    .replace(/跌\/突破旗形另一侧后入场/g, "破旗形另一侧后反向入场")
    .replace(/跌\/突破信号K另一端/g, "破信号K另一侧后反向")
    .replace(/\s+/g, " ")
    .trim();
}

function chartFamilyPrinciple(family) {
  const map = {
    "突破": {
      core: "突破的核心不是穿过价位，而是突破后有无跟随。",
      point: () => "原理：强突破会迫使反向交易者止损，也会吸引顺势交易者追随；没有跟随时，突破常退化成区间里的假突破。",
      fallback: () => "课程提醒：交易区间里的多数突破会失败，只有强收盘和后续K继续推进，才值得提高预期。"
    },
    "回调": {
      core: "回调形态的核心是原趋势是否仍在控制。",
      point: () => "原理：High 2 / Low 2 表达的是逆势方两次尝试失败后，顺势方重新接管；机械数K不是入场理由。",
      fallback: () => "课程提醒：在强趋势里，第一次和第二次回调更有价值；在区间中段，数到2也可能只是噪音。"
    },
    "交易区间": {
      core: "区间里边缘比中间重要，失败突破比追突破更常见。",
      point: () => "原理：区间内多空都能赚钱，但中间位置优势最差；Brooks 通常更重视边缘、磁力位和失败突破。",
      fallback: () => "课程提醒：交易区间中不要默认突破成功，先按买低卖高和小目标管理。"
    },
    "通道": {
      core: "通道是趋势变弱后的推进方式，容易出现双向交易。",
      point: () => "原理：紧密通道仍偏顺势，宽通道则要尊重回撤和通道线；通道末端追单质量会下降。",
      fallback: () => "课程提醒：通道里不要把每次触线都当反转，等测试失败或二次信号更稳。"
    },
    "趋势": {
      core: "趋势图首先看 Always In 控制权。",
      point: () => "原理：强趋势中多数反向信号只是回调；只有结构被破坏并有反向跟随，才开始考虑反转。",
      fallback: () => "课程提醒：不要因为价格看起来太高或太低就逆势，先问现在谁控制市场。"
    },
    "反转/MTR": {
      core: "主要趋势反转是一个过程，不是猜顶底。",
      point: () => "原理：Brooks 通常要看到趋势线突破、回测原极端失败、二次信号或强反向跟随，才把反转当计划。",
      fallback: () => "课程提醒：第一根反向K通常不够，等待结构证据能过滤很多早进场。"
    },
    "楔形": {
      core: "三推说明动能衰竭，但衰竭不等于立刻反转。",
      point: () => "原理：第三推后要看触发和跟随；顺大趋势的楔形旗形通常比逆大趋势反转更可靠。",
      fallback: () => "课程提醒：不要只数三次推进，第三推之后没有反向跟随就仍可能继续原趋势。"
    },
    "末端旗形": {
      core: "末端旗形常是趋势末端的顺势陷阱。",
      point: () => "原理：它看起来像普通整理，但突破失败并回到旗形内时，最后一批追单者会被困住。",
      fallback: () => "课程提醒：末端旗形要重点看突破后是否立刻失败，而不是看到旗形就顺势追。"
    },
    "高潮": {
      core: "高潮后的常见结果是横盘或两段回调，不一定马上反转。",
      point: () => "原理：连续大K和远离均线代表情绪化推进；之后市场常需要时间消化，目标要降到现实。",
      fallback: () => "课程提醒：不要在高潮末端追最差价格，也不要默认第一根反向K就是大反转。"
    },
    "缺口": {
      core: "缺口要看是否回补，未回补才有测量意义。",
      point: () => "原理：缺口代表重新定价；如果很快回补，说明缺口方向没有控制权，若不回补并跟随，才可能成为测量缺口。",
      fallback: () => "课程提醒：缺口本身不是入场理由，要等测试、跟随或回补失败。"
    },
    "开盘": {
      core: "开盘形态要结合昨日高低点、开盘价和早盘速度。",
      point: () => "原理：强开盘可能形成趋势日，失败开盘会迅速回到区间；早盘不要脱离磁力位读图。",
      fallback: () => "课程提醒：开盘前几根K信息密度高，但也最容易追在情绪极端。"
    },
    "目标/磁力": {
      core: "磁力位告诉你价格可能被吸引的位置，不直接告诉方向。",
      point: () => "原理：测量目标、前高低和均线都是市场会测试的位置；到位后的突破或失败才给交易方向。",
      fallback: () => "课程提醒：目标太近时不要硬做，因为方向正确也可能没有足够回报。"
    },
    "K线信号": {
      core: "信号K只提供触发，不能脱离背景。",
      point: () => "原理：同一根K在强趋势里可能只是噪音，在区间边缘可能是好信号；位置决定信号质量。",
      fallback: () => "课程提醒：漂亮信号K后还要看入场K和跟随，不能只看形状。"
    },
    "失败形态": {
      core: "失败形态的力量来自被困交易者。",
      point: () => "原理：当突破或二次入场失败并快速反向时，原方向交易者的止损会推动反向运动。",
      fallback: () => "课程提醒：失败必须有反向跟随，没有跟随只是普通震荡。"
    },
    "入场逻辑": {
      core: "入场方式要匹配市场速度。",
      point: () => "原理：止损单适合突破和强趋势，限价单更常用于区间边缘；入场后没有跟随，要快速降低预期。",
      fallback: () => "课程提醒：先定义入场K和实际风险，再决定能不能做。"
    },
    "交易管理": {
      core: "交易管理看概率、实际风险、目标距离和执行成本。",
      point: () => "原理：看对方向不等于能赚钱，止损太远或目标太近时，交易者方程不成立。",
      fallback: () => "课程提醒：先管理风险，再谈形态胜率。"
    }
  };
  return map[family] || {
    core: "Brooks 的读图重点是背景、位置、触发、跟随和风险收益。",
    point: () => "原理：形态名称只是索引，真正决定交易质量的是市场周期和订单行为。",
    fallback: () => "课程提醒：先判断市场环境，再看信号和交易者方程。"
  };
}

function annotatedChartSrc(chart) {
  const src = String(chart.src || "");
  if (!src) return "";
  return src.replace("assets/ab-charts/", "assets/ab-charts-annotated/").replace(/\.jpe?g$/i, "-annotated.jpg");
}

function toList(value) {
  return Array.isArray(value) ? value : [value].filter(Boolean);
}

function firstText(value) {
  return toList(value)[0] || "先确认背景、位置、信号、风险收益是否同时成立。";
}

function shortText(value, maxLength = 34) {
  const text = String(value || "");
  return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;
}

function sortedEncyclopediaPatterns() {
  const query = state.encyclopediaQuery;
  const rows = encyclopediaPatterns.filter((pattern) => {
    if (state.encyclopediaFamily !== "all" && pattern.family !== state.encyclopediaFamily) return false;
    if (!query) return true;
    return searchText(pattern).toLowerCase().includes(query);
  });
  return rows.sort((a, b) => {
    if (state.encyclopediaSort === "probability") return b.probScore - a.probScore || b.importance - a.importance;
    if (state.encyclopediaSort === "importance") return b.importance - a.importance || b.probScore - a.probScore;
    if (state.encyclopediaSort === "difficulty") return a.difficulty - b.difficulty || b.importance - a.importance;
    if (state.encyclopediaSort === "family") return a.family.localeCompare(b.family, "zh-CN") || b.importance - a.importance;
    return (b.probScore + b.importance) - (a.probScore + a.importance);
  });
}

function renderVideoFilters() {
  const lessons = siteData.videoLessons || [];
  const modules = uniqueSorted(lessons.map((lesson) => lesson.module));
  const topics = uniqueSorted(lessons.flatMap((lesson) => lesson.topics || []));
  const languages = uniqueSorted(lessons.map((lesson) => lesson.language));
  $("#moduleFilter").innerHTML = optionList("全部模块", modules);
  $("#topicFilter").innerHTML = optionList("全部主题", topics);
  $("#languageFilter").innerHTML = optionList("全部语言", languages);
}

function renderVideoLibrary() {
  const lessons = filteredVideoLessons();
  if (!lessons.some((lesson) => lesson.id === state.activeVideoId)) {
    state.activeVideoId = lessons[0]?.id || null;
  }
  const totalMinutes = lessons.reduce((sum, lesson) => sum + (lesson.minutesEstimate || 0), 0);
  const moduleCount = uniqueSorted(lessons.map((lesson) => lesson.module)).length;
  $("#videoSummaryStats").innerHTML = [
    ["当前结果", `${formatNumber(lessons.length)} 节`, "可逐条点击学习"],
    ["估算时长", formatDuration(totalMinutes), "按字幕密度估算"],
    ["覆盖模块", `${moduleCount} 个`, "核心课和补充课"],
    ["中文/英文", languageBreakdown(lessons), "保留对照材料"]
  ].map(([label, value, note]) => `
    <div class="mini-stat searchable" data-search="${html(`${label} ${value} ${note}`)}">
      <span>${html(label)}</span><strong>${html(value)}</strong><small>${html(note)}</small>
    </div>
  `).join("");

  $("#videoLessonGrid").innerHTML = lessons.map((lesson) => `
    <button class="video-card searchable ${lesson.id === state.activeVideoId ? "active" : ""}" type="button" data-video="${lesson.id}" data-search="${html(searchText(lesson))}">
      <span class="video-card-top"><strong>${html(lesson.title)}</strong><em>${html(lesson.language)}</em></span>
      <span>${html(lesson.module)} · ${html(lesson.section)}</span>
      <p>${html(lesson.summary)}</p>
      <span class="tag-line">${(lesson.topics || []).slice(0, 3).map((topic) => `<i>${html(topic)}</i>`).join("")}</span>
    </button>
  `).join("") || `<div class="empty-state">没有匹配的字幕摘要。换一个主题或清空筛选。</div>`;

  $$(".video-card").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeVideoId = Number(button.dataset.video);
      renderVideoLibrary();
    });
  });
  renderVideoDetail();
}

function renderVideoDetail() {
  const lesson = (siteData.videoLessons || []).find((item) => item.id === state.activeVideoId);
  if (!lesson) {
    $("#videoLessonDetail").innerHTML = `<div class="empty-state">请选择一节字幕课。</div>`;
    return;
  }
  $("#videoLessonDetail").innerHTML = `
    <div class="detail-header searchable" data-search="${html(searchText(lesson))}">
      <p class="eyebrow">${html(lesson.module)} · ${html(lesson.language)}</p>
      <h3>${html(lesson.title)}</h3>
      <p>${html(lesson.summary)}</p>
      <div class="pattern-meta">
        <span class="pill">${html(lesson.section)}</span>
        <span class="pill">${formatDuration(lesson.minutesEstimate || 0)}</span>
        <span class="pill">${formatNumber(lesson.cueCount || 0)} 条字幕</span>
      </div>
    </div>
    <div class="pattern-info-grid detail-grid">
      ${infoBlock("本课要点", lesson.bullets || [])}
      ${infoBlock("主题归类", (lesson.topicScores || []).map((item) => `${item.topic} · ${item.score}`))}
      ${infoBlock("练习动作", [lesson.practice])}
      ${infoBlock("来源文件", [`<a href="${localHref(lesson.path)}" target="_blank" rel="noreferrer">${html(lesson.path)}</a>`])}
    </div>
  `;
}

function renderMaterials() {
  const modules = siteData.materialModules || [];
  $("#moduleGrid").innerHTML = modules.map((module) => `
    <article class="module-card searchable" data-search="${html(searchText(module))}">
      <div class="module-head">
        <div>
          <span>${formatNumber(module.files)} 个文件 · ${module.sizeGB} GB</span>
          <h3>${html(module.name)}</h3>
        </div>
        <strong>${module.kinds?.[0] ? html(module.kinds[0].kind) : "资料"}</strong>
      </div>
      <p>${html(module.note)}</p>
      <div class="kind-chips">${(module.kinds || []).slice(0, 5).map((kind) => `<span>${html(kind.kind)} ${formatNumber(kind.count)}</span>`).join("")}</div>
      <div class="sample-links">
        ${(module.samples || []).slice(0, 4).map((sample) => `<a href="${localHref(sample.path)}" target="_blank" rel="noreferrer">${html(sample.name)}</a>`).join("")}
      </div>
    </article>
  `).join("");

  $("#sourceList").innerHTML = (siteData.importantSources || []).slice(0, 34).map((source) => sourceRow(source)).join("");
  renderBars("#kindBars", siteData.stats?.fileKinds || [], "kind", "count", "files");
}

function renderExamples() {
  $("#exampleGrid").innerHTML = exampleAtlas.map((item) => `
    <button class="example-card searchable ${item.id === state.activeExample ? "active" : ""}" type="button" data-example="${item.id}" data-search="${html(searchText(item))}">
      <div class="diagram mini-diagram">${diagramSvg(item.diagram, item.color)}</div>
      <span><strong>${html(item.title)}</strong><em>${html(item.pattern)} · ${html(item.probability)}</em></span>
    </button>
  `).join("");
  $$(".example-card").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeExample = button.dataset.example;
      renderExamples();
    });
  });
  renderExampleDetail();
  $("#chartReferenceList").innerHTML = (siteData.chartReferences || []).slice(0, 24).map((source) => sourceRow(source)).join("");
}

function renderExampleDetail() {
  const item = exampleAtlas.find((example) => example.id === state.activeExample) || exampleAtlas[0];
  $("#exampleDetail").innerHTML = `
    <div class="pattern-hero searchable" data-search="${html(searchText(item))}">
      <div class="diagram">${diagramSvg(item.diagram, item.color)}</div>
      <div>
        <div class="pattern-meta">
          <span class="pill">${html(item.pattern)}</span>
          <span class="pill">${html(item.probability)}</span>
        </div>
        <h3>${html(item.title)}</h3>
        <p>${html(item.source)}</p>
      </div>
    </div>
    <div class="pattern-info-grid detail-grid">
      ${infoBlock("看图要点", item.read)}
      ${infoBlock("入场逻辑", [item.entry])}
      ${infoBlock("失效条件", [item.invalid])}
      ${infoBlock("训练方式", ["先遮住右侧走势，只根据背景写计划。", "每个形态收集至少 30 张图，再统计是否符合你的交易者方程。"])}
    </div>
  `;
}

function renderPatterns() {
  const sorted = [...patterns].sort((a, b) => {
    if (state.patternSort === "sequence") return patterns.indexOf(a) - patterns.indexOf(b);
    if (state.patternSort === "difficulty") return a[5] - b[5];
    return b[4] - a[4];
  });
  $("#patternList").innerHTML = sorted.map((pattern, index) => `
    <button class="pattern-row searchable ${pattern[0] === state.pattern ? "active" : ""}" type="button" data-pattern="${pattern[0]}" data-search="${pattern.join(" ")}">
      <strong>${String(index + 1).padStart(2, "0")}</strong>
      <span><strong>${pattern[1]}</strong><span>${pattern[2]} · 难度 ${"●".repeat(pattern[5])}</span></span>
      <span class="pattern-score">${pattern[3]}</span>
    </button>
  `).join("");
  $$(".pattern-row").forEach((button) => {
    button.addEventListener("click", () => {
      state.pattern = button.dataset.pattern;
      renderPatterns();
    });
  });
  renderPatternDetail();
}

function renderPatternDetail() {
  const pattern = patterns.find((item) => item[0] === state.pattern) || patterns[0];
  $("#patternDetail").innerHTML = `
    <div class="pattern-hero searchable" data-search="${pattern.join(" ")}">
      <div class="diagram">${diagramSvg(pattern[0], pattern[6])}</div>
      <div>
        <div class="pattern-meta">
          <span class="pill">${pattern[3]}</span>
          <span class="pill">${pattern[2]}</span>
          <span class="pill">难度 ${"●".repeat(pattern[5])}</span>
        </div>
        <h3>${pattern[1]}</h3>
        <p>${pattern[7]}</p>
      </div>
    </div>
    <div class="pattern-info-grid">
      ${infoBlock("最佳背景", pattern[8])}
      ${infoBlock("主要陷阱", pattern[9])}
      ${infoBlock("练习方法", [`只收集 ${pattern[1]} 样本`, "每笔记录背景、触发、止损、目标", "至少 100 笔后再判断是否适合你"])}
      ${infoBlock("交易者方程", ["胜率不能单独看", "目标必须覆盖实际风险", "手续费和滑点必须计入"])}
    </div>
  `;
}

function infoBlock(title, items) {
  return `
    <article class="info-block searchable" data-search="${title} ${items.join(" ")}">
      <h4>${title}</h4>
      <ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>
    </article>
  `;
}

function renderGlossary() {
  $("#glossaryGrid").innerHTML = glossary.map(([term, description]) => `
    <article class="glossary-card searchable" data-search="${term} ${description}">
      <strong>${term}</strong>
      <p>${description}</p>
    </article>
  `).join("");
}

function filteredVideoLessons() {
  const query = state.libraryQuery;
  return (siteData.videoLessons || []).filter((lesson) => {
    if (state.libraryModule !== "all" && lesson.module !== state.libraryModule) return false;
    if (state.libraryTopic !== "all" && !(lesson.topics || []).includes(state.libraryTopic)) return false;
    if (state.libraryLanguage !== "all" && lesson.language !== state.libraryLanguage) return false;
    if (!query) return true;
    return searchText(lesson).toLowerCase().includes(query);
  });
}

function renderBars(selector, rows, labelKey, valueKey, suffix) {
  const max = Math.max(...rows.map((row) => row[valueKey] || 0), 1);
  $(selector).innerHTML = rows.slice(0, 12).map((row) => {
    const label = row[labelKey];
    const value = row[valueKey] || 0;
    const width = Math.max(4, Math.round((value / max) * 100));
    return `
      <div class="bar-row searchable" data-search="${html(`${label} ${value}`)}">
        <span>${html(label)}</span>
        <div><i style="width:${width}%"></i></div>
        <strong>${formatNumber(value)} ${suffix === "files" ? "" : ""}</strong>
      </div>
    `;
  }).join("");
}

function sourceRow(source) {
  return `
    <a class="source-row searchable" href="${localHref(source.path)}" target="_blank" rel="noreferrer" data-search="${html(searchText(source))}">
      <span>${html(source.kind || "文件")}</span>
      <strong>${html(source.name)}</strong>
      <em>${html(source.module || "")}</em>
    </a>
  `;
}

function optionList(allLabel, values) {
  return [`<option value="all">${html(allLabel)}</option>`]
    .concat(values.map((value) => `<option value="${html(value)}">${html(value)}</option>`))
    .join("");
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => String(a).localeCompare(String(b), "zh-CN"));
}

function kindCount(kind) {
  return siteData.stats?.fileKinds?.find((item) => item.kind === kind)?.count || 0;
}

function languageBreakdown(lessons) {
  const counts = lessons.reduce((acc, lesson) => {
    acc[lesson.language] = (acc[lesson.language] || 0) + 1;
    return acc;
  }, {});
  return Object.entries(counts).map(([label, count]) => `${label} ${count}`).join(" / ") || "0";
}

function formatDuration(minutes) {
  const safeMinutes = Math.max(0, Number(minutes) || 0);
  const hours = Math.floor(safeMinutes / 60);
  const rest = safeMinutes % 60;
  if (!hours) return `${rest} 分钟`;
  return `${hours} 小时 ${rest} 分钟`;
}

function formatNumber(value) {
  return new Intl.NumberFormat("zh-CN").format(Number(value) || 0);
}

function localHref(path) {
  return `../${String(path || "").split("/").map((part) => encodeURIComponent(part)).join("/")}`;
}

function normalizeChartItems(value) {
  const items = Array.isArray(value) ? value : value ? [value] : [];
  return items.filter((chart) => !isChapterCoverChart(chart));
}

function isChapterCoverChart(chart) {
  return chartCoverImageSources.has(String(chart?.src || ""));
}

function colorForFamily(family) {
  const colors = {
    "突破": "#087f8c",
    "回调": "#315f93",
    "交易区间": "#637f35",
    "通道": "#7b507d",
    "趋势": "#087f8c",
    "反转/MTR": "#5f6f84",
    "楔形": "#b94738",
    "末端旗形": "#a76f22",
    "双顶双底": "#315f93",
    "三角形": "#637f35",
    "头肩": "#7b507d",
    "圆弧": "#5f6f84",
    "高潮": "#d95d39",
    "缺口": "#b88117",
    "开盘": "#d95d39",
    "目标/磁力": "#4c7c59",
    "K线信号": "#315f93",
    "失败形态": "#b94738",
    "入场逻辑": "#087f8c",
    "交易管理": "#b88117"
  };
  return colors[family] || "#087f8c";
}

function html(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  })[char]);
}

function searchText(value) {
  if (Array.isArray(value)) return value.join(" ");
  if (typeof value === "object" && value) return Object.values(value).flat(2).join(" ");
  return String(value || "");
}

function diagramSvg(type, color) {
  const diagrams = {
    cycle: { levels: [[62, "突破"], [118, "通道"], [154, "区间"]], path: "M24 154 L70 100 L110 62 L150 92 L190 112 L230 146 L286 138", candles: [[50,154,112,108,158],[86,112,78,72,116],[124,78,62,56,82],[162,62,94,58,98],[202,94,114,90,118],[242,114,146,110,150]], label: "突破 → 通道 → 区间" },
    signal: { levels: [[150, "支撑"]], path: "M24 82 L70 116 L112 148 L154 138 L194 100 L238 72 L286 58", candles: [[50,82,116,78,120],[92,116,148,112,152],[134,148,138,132,154],[176,138,100,96,142],[218,100,72,68,104],[260,72,58,54,78]], label: "关键位置的信号蜡烛" },
    trend: { levels: [], path: "M24 158 L64 126 L102 140 L142 104 L180 118 L220 82 L286 52", candles: [[46,158,126,122,162],[86,126,140,122,144],[126,140,104,100,144],[166,104,118,100,122],[206,118,82,78,122],[254,82,52,48,86]], label: "多头控制趋势" },
    h2l2: { levels: [], path: "M24 158 L64 128 L102 142 L140 108 L178 128 L218 86 L284 54", candles: [[46,150,125,120,158],[88,126,142,122,146],[130,140,108,102,144],[170,109,128,104,134],[216,126,86,80,130],[258,86,54,48,90]], label: "两段回调失败" },
    magnets: { levels: [[76, "阻力"], [150, "支撑"], [112, "开盘/均线"]], path: "M24 150 L72 112 L116 78 L154 98 L200 150 L244 112 L286 76", candles: [[52,150,112,108,154],[96,112,78,72,116],[136,78,98,74,102],[180,98,150,94,154],[224,150,112,108,154],[268,112,76,72,116]], label: "磁力位测试" },
    range: { levels: [[62, "区间高"], [152, "区间低"]], path: "M24 150 L62 84 L100 64 L140 142 L178 154 L220 86 L262 66 L292 132", candles: [[45,146,84,80,152],[84,84,64,58,90],[124,66,140,62,146],[164,140,154,136,160],[208,154,86,82,158],[250,86,66,60,92]], label: "买低卖高" },
    channel: { channel: true, path: "M24 156 L68 132 L112 142 L156 104 L200 112 L244 72 L288 84", candles: [[48,154,132,128,160],[92,132,142,126,146],[136,142,104,100,146],[180,104,112,100,116],[224,112,72,66,116],[268,72,84,68,90]], label: "通道线测试" },
    mtr: { levels: [[68, "趋势线突破"]], path: "M24 52 L68 76 L112 96 L152 128 L192 96 L232 132 L286 86", candles: [[46,52,76,48,80],[90,76,96,72,100],[134,96,128,92,132],[178,128,96,92,132],[222,96,132,92,136],[264,132,86,82,136]], label: "突破通道 + 二次反转" },
    wedge: { levels: [[68, "第三推"]], path: "M24 154 L62 116 L98 132 L136 92 L174 110 L214 70 L256 102 L288 136", candles: [[50,154,116,112,158],[86,116,132,112,136],[126,132,92,88,136],[166,92,110,88,114],[208,110,70,64,114],[250,70,102,66,108]], label: "三推后失败" },
    breakout: { levels: [[120, "阻力"]], path: "M24 150 L58 146 L90 151 L124 148 L154 146 L184 110 L216 78 L252 52 L286 44", candles: [[38,142,151,138,154],[72,151,145,142,156],[106,146,151,140,154],[140,151,145,141,156],[178,143,108,101,147],[214,108,78,72,112],[250,77,52,46,82]], label: "强突破 + 跟随" },
    measured: { levels: [[154, "突破点"], [58, "测量目标"]], path: "M24 154 L72 104 L118 72 L160 116 L206 82 L286 58", candles: [[52,150,104,100,156],[96,104,72,68,108],[142,72,116,68,122],[190,116,82,76,120],[244,82,58,52,86]], label: "第一段 = 第二段" },
    equation: { levels: [[76, "目标"], [150, "止损"]], path: "M24 128 L64 104 L102 126 L142 82 L182 112 L226 72 L286 84", candles: [[50,128,104,100,132],[90,104,126,100,130],[130,126,82,78,130],[170,82,112,78,116],[214,112,72,68,116],[258,72,84,68,88]], label: "概率 × 回报 > 风险" },
    management: { levels: [[72, "止盈"], [154, "保护止损"]], path: "M24 150 L70 112 L116 130 L160 92 L206 78 L252 86 L286 70", candles: [[52,150,112,108,154],[96,112,130,108,134],[140,130,92,88,134],[186,92,78,72,96],[230,78,86,74,90],[268,86,70,66,90]], label: "入场后管理" },
    opening: { levels: [[148, "昨日低点"], [92, "开盘价"]], path: "M24 82 L62 120 L100 150 L136 138 L174 102 L214 78 L286 58", candles: [[46,84,118,80,122],[84,118,150,112,155],[124,150,136,132,154],[166,136,102,98,140],[208,102,78,72,106],[252,78,58,52,82]], label: "开盘测试后反转" },
    system: { levels: [[96, "规则"], [150, "复盘"]], path: "M24 150 L70 126 L116 136 L160 110 L206 96 L252 116 L286 86", candles: [[52,150,126,122,154],[96,126,136,122,140],[140,136,110,106,140],[186,110,96,92,114],[230,96,116,92,120],[268,116,86,82,120]], label: "固定一种形态" },
    finalflag: { levels: [[60, "磁力位"]], path: "M24 154 L70 116 L112 86 L154 64 L190 70 L224 66 L260 92 L288 132", candles: [[50,154,116,112,158],[94,116,86,80,120],[138,86,64,58,90],[180,64,70,60,74],[218,70,66,62,74],[254,66,92,62,98]], label: "末端旗形失败" },
    climax: { levels: [[48, "远离均线"], [128, "两段回调"]], path: "M24 168 L66 132 L106 92 L146 54 L184 42 L220 88 L256 72 L288 118", candles: [[46,168,132,128,172],[86,132,92,88,136],[126,92,54,50,98],[166,54,42,36,60],[206,42,88,38,94],[246,88,72,68,94],[278,72,118,68,124]], label: "高潮后两段回调" },
    magnet: { levels: [[76, "阻力"], [150, "支撑"], [112, "开盘/均线"]], path: "M24 150 L72 112 L116 78 L154 98 L200 150 L244 112 L286 76", candles: [[52,150,112,108,154],[96,112,78,72,116],[136,78,98,74,102],[180,98,150,94,154],[224,150,112,108,154],[268,112,76,72,116]], label: "磁力位测试" }
  };
  const d = diagrams[type] || diagrams.breakout;
  const levelMarkup = (d.levels || []).map(([y, text]) => `<line x1="18" y1="${y}" x2="302" y2="${y}" class="level"/><text x="22" y="${y - 6}" class="level-text">${text}</text>`).join("");
  const channelMarkup = d.channel ? `<line x1="24" y1="156" x2="288" y2="68" class="channel-line"/><line x1="24" y1="118" x2="288" y2="30" class="channel-line"/>` : "";
  const candles = d.candles.map(([x, open, close, low, high]) => candle(x, open, close, low, high, close < open ? color : "#d95d39")).join("");
  return `
    <svg viewBox="0 0 320 220" role="img" aria-label="${d.label}">
      <rect x="0" y="0" width="320" height="220" fill="#fbfcfa"/>
      <line x1="18" y1="184" x2="302" y2="184" class="axis"/>
      ${levelMarkup}
      ${channelMarkup}
      <path d="${d.path}" fill="none" stroke="${color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      ${candles}
      <text x="18" y="205" class="diagram-label">${d.label}</text>
    </svg>
  `;
}

function candle(x, open, close, low, high, color) {
  const top = Math.min(open, close);
  const height = Math.max(7, Math.abs(close - open));
  return `<line x1="${x}" y1="${low}" x2="${x}" y2="${high}" stroke="#43505a" stroke-width="2"/><rect x="${x - 6}" y="${top}" width="12" height="${height}" rx="1.5" fill="${color}" stroke="#24313a" stroke-width="1"/>`;
}

init();
