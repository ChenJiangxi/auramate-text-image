#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-
"""
从 templates/ 生成 8 个内容类型的 demo slide。
每个 demo 的文案都按对应子 skill 的规则写，不是占位符。

    /usr/bin/python3 build.py && node render.js

03 图鉴那两张形态页交付的是 GIF 不是静帧（形态本来就是动的）：
    M=~/HermitAgents/auramate-shared/shishen-mov
    node ../../tools/slide-gif.js 03-tujian-2.html $M/dunwu-day.mov 03-tujian-2.gif 4
    node ../../tools/slide-gif.js 03-tujian-3.html $M/yali-day.mov  03-tujian-3.gif 4
仓库里那两张是 README 缩略版（GIF_WIDTH=620 GIF_MAX_MB=2），真交付走默认 1080 起。
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, '../../templates')

def load(p):
    return io.open(os.path.join(TPL, p), encoding='utf-8').read()

COVER = load('editorial-gradient/cover.html')
BODY  = load('editorial-gradient/body.html')
SHOT  = load('editorial-gradient/shot.html')
PAIR  = load('editorial-gradient/pair.html')
CARD_COVER = load('card-light/cover.html')
CARD_BODY  = load('card-light/body.html')


def cover(out, kicker, title_html, illo, title_px=132, illo_h=400, pos='center 76%'):
    s = COVER
    s = s.replace('灵伴 AI · {{系列名}}', kicker)
    s = s.replace('{{标题第一行}}，<br/>{{标题第二行}}，<br/>{{第三行含}}<span class="em">{{accent词}}</span>', title_html)
    s = s.replace('assets/illustration.png', illo)
    if title_px != 132:
        s = s.replace('font-size:132px', 'font-size:%dpx' % title_px)
    if illo_h != 400:
        s = s.replace('height:400px', 'height:%dpx' % illo_h)
    if pos != 'center 76%':
        s = s.replace('object-position:center 76%', 'object-position:%s' % pos)
    write(out, s)


def body(out, kicker, paras):
    s = BODY
    s = s.replace('{{系列名}} · 01', kicker)
    inner = '\n  '.join('<p>%s</p>' % p for p in paras)
    s = re.sub(r'<div class="body">.*?</div>\n<div class="foot">',
               '<div class="body">\n  %s\n</div>\n<div class="foot">' % inner, s, flags=re.S)
    write(out, s)


def shot(out, kicker, head_html, img, foot_l, foot_r, portrait=True):
    s = SHOT
    s = s.replace('{{系列名}} · 03', kicker)
    s = s.replace('{{一句说明}}，<span class="em">{{accent 部分}}</span>', head_html)
    s = s.replace('assets/pf-chart.png', img)
    s = s.replace('灵伴 AI · {{功能名}}', foot_l).replace('{{数据标注}}', foot_r)
    if not portrait:  # landscape / 近方图：铺满宽度
        s = s.replace('.shot{height:100%;', '.shot{width:100%;height:auto;max-height:100%;')
        s = s.replace('.shot img{height:100%;display:block;}', '.shot img{width:100%;display:block;}')
    write(out, s)


def pair(out, kicker, head_html, left, right, foot_l, foot_r):
    """left/right = (形态 id, 形态名, 标签, 一句话)"""
    s = PAIR
    s = s.replace('{{系列名}} · {{期号}}', kicker)
    s = s.replace('{{这一对讲的是什么}}，<span class="em">{{分成两种}}</span>', head_html)
    s = s.replace('assets/form-{{左}}.png', 'assets/form-%s.png' % left[0])
    s = s.replace('assets/form-{{右}}.png', 'assets/form-%s.png' % right[0])
    s = s.replace('{{左形态名}}', left[1]).replace('{{右形态名}}', right[1])
    s = s.replace('<span class="tag">稳</span>', '<span class="tag">%s</span>' % left[2], 1)
    s = s.replace('<span class="tag">野</span>', '<span class="tag">%s</span>' % right[2], 1)
    s = s.replace('{{一句话，具体，说人话}}', left[3])
    s = s.replace('{{一句话，跟左边形成对照}}', right[3])
    s = s.replace('灵伴 AI · {{功能名}}', foot_l).replace('{{标注}}', foot_r)
    write(out, s)


def card_cover(out, label, head_html, sub, orb):
    s = CARD_COVER
    s = s.replace('assets/cover-orb.jpg', orb)
    s = s.replace('· {{副标签}}', label)
    s = s.replace('{{第一行}}<br/><span class="em">{{accent}}</span> {{余下}}', head_html)
    s = s.replace('{{副标题一句话，46px}}', sub)
    write(out, s)


def card_body(out, kicker, name, state, orb):
    s = CARD_BODY
    s = s.replace('assets/form-{{id}}.png', orb)
    s = s.replace('{{系列名}} · {{序号}} / {{总数}}', kicker)
    s = s.replace('{{形态名}}', name)
    s = s.replace('{{一句具体状态，不是定义}}', state)
    write(out, s)


def write(name, s):
    io.open(os.path.join(HERE, name), 'w', encoding='utf-8').write(s)


# ════════════════════════════════════════════════════════════════
# 01 · 心理钩子 reframe（叙事随笔 · 主力线）
#     钩子：高敏+创伤+野心家，低谷期只会向内求 → 人生 K 线 life-kline
# ════════════════════════════════════════════════════════════════
cover('01-reframe-1.html', '灵伴 AI · 状态手记',
      '低谷期最大的坑，<br/>是你把自己，<br/>活成了<span class="em">替罪羊</span>',
      'assets/illustration.png')

body('01-reframe-2.html', '低谷期 · 01', [
 '有一种人，心思特别细，一点风吹草动都能往心里去；小时候多半还带着点没消化的委屈；'
 '可偏偏又不甘心，心里一直憋着股劲，想做成点什么。'
 '<span class="em">高敏、带旧伤、又是个野心家</span>——这三样，常常长在同一个人身上。',
 '顺的时候都还好。一到低谷就出事了：事情搞砸了，关系散了，钱也紧了。'
 '换别人，骂两句环境、怪两句运气，也就过去了。他不行。'
 '他只会往自己身上问——是不是我不够好，是不是又是我哪儿做错了。',
 '一件坏事，他能翻来覆去地嚼很久，嚼到最后，结论永远是那一个：怪我。慢慢地，什么锅都成了他的。',
])

shot('01-reframe-3.html', '低谷期 · 03',
     '你这一辈子，<span class="em">本来就有涨有跌</span>',
     'assets/pf-chart.png', '灵伴 AI · 人生 K 线', '红涨吉 · 绿跌凶')


# ════════════════════════════════════════════════════════════════
# 02 · 十神解析（知识解析）
#     ⚠️ 上一版是废稿：只说「有一套东西叫十神，我做成了产品」，没讲透任何概念，
#        配图还拿同一张通用光球充两个角色。重写标准 —— 读者读完要能复述一个新知识点。
#     真知识点 = 十种其实是五对，每对是同一件事的「稳」版和「野」版。
#     ⚠️ 十个原名里「伤官」「印」是违禁词，一个都不写。只用形态名 + 「正/偏」这层结构讲。
# ════════════════════════════════════════════════════════════════
cover('02-shishen-1.html', '灵伴 AI · 古人的十种状态 · 01',
      '古人形容状态，<br/>分成五对，<br/>每对都有个<span class="em">失控版</span>',
      'assets/forms-strip.png', illo_h=420, pos='center 50%')

body('02-shishen-2.html', '古人的十种状态 · 01', [
 '我们现在形容状态，词很少：忙、累、还行、emo。'
 '一千年前的人分得细得多——他们把人和外界的关系拆成<span class="em">五对</span>，一共十种。',
 '五对分别是：跟人<span class="em">并肩</span>、把东西<span class="em">往外给</span>、'
 '<span class="em">拿到</span>、被<span class="em">管着</span>、被<span class="em">托着</span>。'
 '每一对里还要再分一次——一个带「正」字，一个带「偏」字。',
 '「正」是稳的、走明路的；「偏」是野的、不按常理来的。'
 '同一件事，温和地发生和失控地发生，在他们眼里不是一回事，得给两个名字。'
 '<span class="last">这是这套东西里最值得学的一层：它承认同一种力有两张脸。</span>',
])

pair('02-shishen-3.html', '古人的十种状态', '同样是<span class="em">往外给</span>，古人分成两种',
     ('meishi', '美食日', '正 · 稳', '慢慢来，做点自己喜欢的事。<br/>力气是往外散的，但散得温和。'),
     ('fafeng', '发疯日', '偏 · 野', '憋不住了，非得说点什么。<br/>同样是往外，这天是炸开的。'),
     '灵伴 AI · 每日形态', '五对之二 · 往外给')


# ════════════════════════════════════════════════════════════════
# 03 · 图鉴自测（对号入座）—— 卡片风，一张一个形态
# ════════════════════════════════════════════════════════════════
card_cover('03-tujian-1.html', '· 十种状态',
           '你今天<br/>是<span class="em">哪一种</span>',
           '十种形态全在下面，对号入座一下。我自己最常出现的是顿悟日。',
           'assets/form-dunwu.png')

card_body('03-tujian-2.html', '十种状态 · 06 / 10', '顿悟日',
          '表面上没动静，脑子里一直在转。<br/>灵感是这天冒出来的。', 'assets/form-dunwu.png')

card_body('03-tujian-3.html', '十种状态 · 08 / 10', '压力日',
          '弦是绷着的，但该争的得争。<br/>这天适合把硬话说完。', 'assets/form-yali.png')


# ════════════════════════════════════════════════════════════════
# 04 · 功能更新（旺运地图 geo-fortune）
#     铁律：标题是痛点不是功能名；不许「重磅 / 上新 / 立即体验」
# ════════════════════════════════════════════════════════════════
cover('04-gongneng-1.html', '灵伴 AI · 新功能 · 旺运地图',
      '在哪个城市，<br/>我会过得<br/><span class="em">松一点</span>',
      'assets/geo-map.png', illo_h=430, pos='center 45%')

body('04-gongneng-2.html', '旺运地图 · 01', [
 '去年有人问我一个问题，我答不上来：我在深圳待了六年，一直觉得很紧，'
 '换个城市会不会好一点？',
 '这个问题很难答，因为它不是「哪个城市更好」，是「哪个城市<span class="em">和你更对得上</span>」。'
 '同一座城，有人如鱼得水，有人怎么都别扭。',
 '所以我们把它做成了一张图：把你的出生时间数据和全国各省的地理参数放在一起算，'
 '算出来一张热力图。红的是你舒展的地方，暗的是你使不上劲的地方。',
])

shot('04-gongneng-3.html', '旺运地图 · 02',
     '整张地图，<span class="em">每个人的都不一样</span>',
     'assets/geo-map.png', '灵伴 AI · 旺运地图', '越红越舒展', portrait=False)


# ════════════════════════════════════════════════════════════════
# 05 · BaziQA 数据集测评（数据背书）
#     ⚠️ 数据诚实红线：只用竞赛 5 模型口径，不混 live 榜，不臆造 Claude
# ════════════════════════════════════════════════════════════════
cover('05-baziqa-1.html', '灵伴 AI · 模型测评 · 四届专家赛真题',
      '我们拿四届<br/>专家赛真题，<br/>考了<span class="em">五个大模型</span>',
      'assets/chart.png', illo_h=440, pos='center 50%')

shot('05-baziqa-2.html', '模型测评 · 01',
     '结果有点意外：<span class="em">通用模型全在下面</span>',
     'assets/chart.png', '灵伴 AI · live benchmark', '2022–2025 四届宏平均', portrait=False)

body('05-baziqa-3.html', '模型测评 · 02', [
 '说清楚口径，不然这张图没意义：题目是 2022 到 2025 四届全球专家赛的真题，'
 '盲测，答完再对答案。人类那三根是历届冠亚季军的成绩。',
 '灵伴 <span class="em">37.1%</span>，比在场所有通用大模型都高，但离人类冠军的 44.4% 还差一截。'
 '我们没有赢过人，这个得说实话。',
 '另外一句也得说实话：这张图只包含我们本地测过的五个模型。'
 '最新的一些模型在我们另一份榜单上已经反超了灵伴，那份榜单里没有灵伴这一行，所以没法画进来。'
 '要加，得先补测。',
])


# ════════════════════════════════════════════════════════════════
# 06 · 使用教程（收藏率天花板）
# ════════════════════════════════════════════════════════════════
cover('06-jiaocheng-1.html', '灵伴 AI · 报告怎么读',
      '这份报告<br/>我看了三遍<br/>才<span class="em">看懂</span>',
      'assets/radar.png', illo_h=420, pos='center 40%')

shot('06-jiaocheng-2.html', '报告怎么读 · 01',
     '第一步：<span class="em">先看那个八边形</span>',
     'assets/radar.png', '灵伴 AI · 天赋脑图', '八个维度 · 分数越高越突出')

body('06-jiaocheng-3.html', '报告怎么读 · 02', [
 '很多人打开就往下拉找结论，其实<span class="em">最有用的是那个形状</span>。',
 '八个数字里，你不用记具体分，只要看哪两个凸出来、哪两个凹进去。'
 '凸出来的是你不费劲就能做好的事，凹进去的是你做起来特别耗的事。',
 '我自己那张，边缘系统 85 顶得最高，小脑 60 最低。'
 '翻译过来就是：我对情绪信号敏感得过头，但手上的精细活儿一做就烦。'
 '这解释了我为什么写东西可以写一天，装个家具能装到砸手。',
])


# ════════════════════════════════════════════════════════════════
# 07 · 抽奖活动
#     ⚠️ 必须走平台官方抽奖组件；不许「评论区扣」「私信我」
# ════════════════════════════════════════════════════════════════
cover('07-choujiang-1.html', '灵伴 AI · 抽奖 · 30 份深度报告',
      '上个月有人问<br/>这报告长什么样，<br/>不如<span class="em">直接送</span>',
      'assets/pentagon.png', illo_h=430, pos='center 50%')

body('07-choujiang-2.html', '抽奖 · 01', [
 '与其解释，不如直接给你们看。这次拿出 <span class="em">30 份</span>深度报告，'
 '用平台自带的抽奖功能开，<span class="em">我不经手</span>。',
 '报告里有五脏气机的平衡图、八个维度的天赋分布、还有一份按你出生时间算出来的年度节奏表。'
 '图 2 是其中一页，我自己那份。',
 '开奖之后我会单独发一条公示。没抽到也不要紧，这些功能本来就能自己去试。',
])


# ════════════════════════════════════════════════════════════════
# 08 · 节令热点（三伏 → 命理体检 health-wuyun）
# ════════════════════════════════════════════════════════════════
cover('08-jieling-1.html', '灵伴 AI · 节气手记',
      '入伏这几天，<br/>身体最先<br/><span class="em">扛不住的地方</span>',
      'assets/pentagon.png', illo_h=430, pos='center 50%')

shot('08-jieling-2.html', '节气手记 · 01',
     '五脏各有各的<span class="em">负载曲线</span>',
     'assets/pentagon.png', '灵伴 AI · 五脏读数', '木肝 · 火心 · 土脾 · 金肺 · 水肾', portrait=False)

body('08-jieling-3.html', '节气手记 · 02', [
 '古人把一年切成二十四段，不是为了好看，是因为<span class="em">身体在每一段里的负载不一样</span>。'
 '三伏这段最典型：外面热，里面反而是空的。',
 '一套一千年前的季节-体质对应表，把这件事记得很细：'
 '哪一段该多睡，哪一段不该吃凉的，哪一段情绪容易起火。'
 '我们把它做成了一份体检式的读数，每个人的图都不一样。',
 '你不用信它，就当是一份提醒：<span class="last">这几天你觉得累，可能真的不是你懒。</span>',
])

print('生成了 8 个 demo 共', len([f for f in os.listdir(HERE) if f.endswith('.html')]), '张 slide')
