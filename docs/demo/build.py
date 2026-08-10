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


def cover(out, kicker, title_html, illo, title_px=132, illo_h=400, pos='center 76%',
          fit='cover', bg=None, card=False):
    """fit='contain' + bg：横构图信息图不可裁。
       card=True：近方形信息图（雷达 / 五边形）—— 居中圆角卡，不出血，
       图自己就是卡，两边露浅渐变。塞进出血横带会左右留一大片底色。"""
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
    if fit != 'cover':
        s = s.replace('object-fit:cover', 'object-fit:%s' % fit)
    if bg and not card:
        s = s.replace('.illo{height:%dpx' % illo_h, '.illo{background:%s;height:%dpx' % (bg, illo_h))
    if card:
        s = s.replace('.illo{height:%dpx;flex-shrink:0;margin:0 -88px;}' % illo_h,
                      '.illo{height:%dpx;flex-shrink:0;display:flex;align-items:center;'
                      'justify-content:center;}' % illo_h)
        s = s.replace('.illo img{width:100%;height:100%;object-fit:contain;',
                      '.illo img{height:100%;width:auto;max-width:100%;border-radius:24px;')
        s = s.replace('box-shadow:0 -8px 28px rgba(72,48,92,0.12);',
                      'box-shadow:0 18px 44px rgba(72,48,92,0.24);')
    write(out, s)


def body(out, kicker, paras):
    s = BODY
    s = s.replace('{{系列名}} · 01', kicker)
    inner = '\n  '.join('<p>%s</p>' % p for p in paras)
    s = re.sub(r'<div class="body">.*?</div>\n<div class="foot">',
               '<div class="body">\n  %s\n</div>\n<div class="foot">' % inner, s, flags=re.S)
    write(out, s)


def shot(out, kicker, head_html, img, foot_l, foot_r, portrait=True, note=None):
    """note: 横构图截图下方的解读段，用来填掉图和 foot 之间的空。竖图不用传。"""
    s = SHOT
    s = s.replace('{{系列名}} · 03', kicker)
    s = s.replace('{{一句说明}}，<span class="em">{{accent 部分}}</span>', head_html)
    s = s.replace('assets/pf-chart.png', img)
    s = s.replace('灵伴 AI · {{功能名}}', foot_l).replace('{{数据标注}}', foot_r)
    if not portrait:  # landscape / 近方图：铺满宽度
        s = s.replace('.shot{height:100%;', '.shot{width:100%;height:auto;max-height:100%;')
        s = s.replace('.shot img{height:100%;display:block;}', '.shot img{width:100%;display:block;}')
    if note:
        s = s.replace('{{横图才留这段解读，竖图删掉}}', note)
    else:
        s = s.replace('<div class="note">{{横图才留这段解读，竖图删掉}}</div>\n', '')
    write(out, s)


def pair(out, kicker, head_html, left, right, foot_l, foot_r):
    """left/right = (形态 id, 形态名, 标签, 一句话)"""
    s = PAIR
    s = s.replace('{{系列名}} · {{期号}}', kicker)
    s = s.replace('{{这一对讲的是什么}}，<span class="em">{{分成两种}}</span>', head_html)
    s = s.replace('assets/form-{{左}}.jpg', 'assets/form-%s.jpg' % left[0])
    s = s.replace('assets/form-{{右}}.jpg', 'assets/form-%s.jpg' % right[0])
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
    s = s.replace('assets/form-{{id}}.jpg', orb)
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

body('01-reframe-3.html', '低谷期 · 02', [
 '后来我慢慢想明白：他不是不会反省，是反省的时候，手里没有一把<span class="em">尺子</span>。'
 '没有尺子，他就量不出来——眼前这件坏事，几分是我的问题，几分是这段日子本来就难。',
 '少了这把尺子，剩下的就只能全算到自己头上。'
 '所以我做了个东西，叫人生 K 线：拿你的出生时间数据，把这一辈子的起落，画成一条有涨有跌的线。',
 '哪几年往上走，哪几年本来就低，清清楚楚摆在你面前。'
 '它不替你开脱什么，只是让你看见——你现在正踩着的这个坑，在整条线里，是有它的位置的。',
])

shot('01-reframe-4.html', '低谷期 · 03',
     '你这一辈子，<span class="em">本来就有涨有跌</span>',
     'assets/pf-chart.png', '灵伴 AI · 人生 K 线', '红涨吉 · 绿跌凶')

shot('01-reframe-5.html', '低谷期 · 04',
     '点开那一年，<span class="em">它把起落讲给你听</span>',
     'assets/pf-detail.png', '灵伴 AI · 人生 K 线', '开盘 · 收盘 · 最高 · 最低')

body('01-reframe-6.html', '低谷期 · 05', [
 '向内求，本来是件好事。可一旦过了头，就成了没完没了的自我审判——'
 '把系统的、时运的、别人的问题，一股脑收进自己身上，判自己有罪。',
 '这套东西给你的，从来不是一张免罪符，让你把责任推给命。它给的是一个<span class="em">坐标</span>：'
 '让你在最难、最想骂自己的那一刻，抬头看一眼——哦，我这会儿正站在低处，这段本来就难，它会过去。',
 '<span class="last">低谷这东西，说到底不是你坏了，是你正走在一段低的运里。'
 '这条线迟早会拐头往上。你要做的，只是别在最难的时候，还亲手判自己有罪。</span>',
])


# ════════════════════════════════════════════════════════════════
# 02 · 十神解析（知识解析）
#     ⚠️ 前两版都是废稿。第一版只说「有这么个东西，我做成了产品」；第二版编了个
#        「正=稳/偏=野」的分法当定义——用户：「八字里的十神概念是怎么样的？你这内容完全不符合」。
#     真实结构（安全说法）：
#       ① 十种是**关系**不是标签，相对「你自己」这个基准点算，换个基准点名字全变
#       ② 关系只有五类，因为五种元素两两之间只可能有五种关系：
#          帮我的 / 我帮的 / 管我的 / 我管的 / 跟我一样的
#       ③ 每类按**阴阳同不同**再分二 → 五乘二正好十。「十」不是凑的，是算出来的
#     ⚠️ 红线：「伤官」「印」「命主」「八字」一个都不写。「日主」也避（跟命主同险），
#        改说「你自己那个基准点」。「阴阳」「五种元素」不违禁。
# ════════════════════════════════════════════════════════════════
cover('02-shishen-1.html', '灵伴 AI · 古人的十种状态 · 01',
      '不是十种性格，<br/>是你和世界的<br/><span class="em">十种关系</span>',
      'assets/forms-strip.jpg', illo_h=420, pos='center 50%')

body('02-shishen-2.html', '古人的十种状态 · 01', [
 '很多人把这十个当性格标签用，像 MBTI 那样对号入座。但它<span class="em">根本不是标签，是关系</span>。',
 '算出来的每一个名字，说的都是「某样东西对你」是什么关系——'
 '基准点是<span class="em">你自己</span>。同一样东西，换个人来算，名字完全不同。'
 '所以它没办法脱离你单独存在，也就没有「这个人是 XX 型」这种说法。',
 '这是它和现代那些人格测试最不一样的地方：那些测的是你是谁，这个测的是你和外面的东西怎么接上。',
])

body('02-shishen-3.html', '古人的十种状态 · 02', [
 '关系一共只有五类。因为古人拿来描述世界的那五种元素，两两之间只可能有五种关系：'
 '<span class="em">帮我的、我帮的、管我的、我管的、跟我一样的</span>。想不出第六种。',
 '每一类再分成两个，分法是看<span class="em">阴阳同不同</span>。'
 '阴阳不同的那个，两边有牵引，作用直接、来得快；'
 '阴阳相同的那个，没这层牵引，劲儿要么更钝、要么走偏。',
 '<span class="last">五类乘二，正好十个。所以「十」不是古人凑了十个词，'
 '是这个结构算下来只能是十个。</span>',
])

pair('02-shishen-4.html', '古人的十种状态', '同样是<span class="em">我帮的</span>，阴阳同不同，出来两个样',
     ('meishi', '美食日', '阴阳相同', '没牵引，劲儿泄得慢。<br/>慢慢做点自己喜欢的事。'),
     ('fafeng', '发疯日', '阴阳相异', '有牵引，泄得又快又猛。<br/>憋不住，非得说点什么。'),
     '灵伴 AI · 每日形态', '五类之二 · 我帮的')


# ════════════════════════════════════════════════════════════════
# 03 · 图鉴自测（对号入座）—— 完整 12 张
#     ⚠️ 这类不是 3 张能讲完的。类型数 8-12，一种一张，少了不够挑。
#     顺序按五对排（并肩/往外给/拿到/管着/托着），扫起来有结构。
#     真交付是 GIF（形态本来就是动的），静帧只是这里为了仓库体积。
# ════════════════════════════════════════════════════════════════
card_cover('03-tujian-01.html', '· 十种状态',
           '你今天<br/>是<span class="em">哪一种</span>',
           '十种形态全在下面，一种一张。我自己最常出现的是顿悟日。',
           'assets/form-dunwu.jpg')

FORMS = [
 ('hezuo',    '合作日', '02', '想找的人都在线，约得上。<br/>这天谈事比一个人闷头干强。'),
 ('fenxiang', '分享日', '03', '嘴松，钱也松。<br/>想请客、想买单、想把知道的都说出去。'),
 ('meishi',   '美食日', '04', '慢慢来，做点自己喜欢的事。<br/>力气是往外散的，但散得温和。'),
 ('fafeng',   '发疯日', '05', '憋不住了，非得说点什么。<br/>同样是往外，这天是炸开的。'),
 ('gaoqian',  '搞钱日', '06', '坐得住，一笔一笔推进度。<br/>拿到的是你自己挣的那份。'),
 ('jianlou',  '捡漏日', '07', '没打算要，它自己掉下来。<br/>眼疾手快接住的那种。'),
 ('juanwang', '卷王日', '08', '按节拍走，列表一条条勾掉。<br/>不亢奋，但手感很稳。'),
 ('yali',     '压力日', '09', '弦是绷着的，但该争的得争。<br/>这天适合把硬话说完。'),
 ('xuexi',    '学习日', '10', '有人托着你，事情自己顺。<br/>适合学新东西、接别人递过来的。'),
 ('dunwu',    '顿悟日', '11', '表面上没动静，脑子里一直在转。<br/>灵感是这天冒出来的。'),
]
for fid, name, no, state in FORMS:
    card_body('03-tujian-%s.html' % no, '十种状态 · %s / 10' % no, name, state,
              'assets/form-%s.jpg' % fid)

card_body('03-tujian-12.html', '十种状态 · 收尾', '每天换一种',
          '它读你的出生时间数据，自己判断今天是哪一种。<br/>不用填问卷，也不用选心情。',
          'assets/forms-strip.jpg')


# ════════════════════════════════════════════════════════════════
# 04 · 功能更新（旺运地图 geo-fortune）
#     铁律：标题是痛点不是功能名；不许「重磅 / 上新 / 立即体验」
# ════════════════════════════════════════════════════════════════
cover('04-gongneng-1.html', '灵伴 AI · 新功能 · 旺运地图',
      '在深圳待了六年，<br/>我一直以为<br/><span class="em">是我不够拼</span>',
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
     'assets/geo-map.png', '灵伴 AI · 旺运地图', '越红越舒展', portrait=False,
     note='红的地方不是「那儿更好」，是<span class="em">那儿跟你更对得上</span>。'
          '同一张地图，换个人算出来能差一大片——我自己这张，最红的一块正好是我一直没想过要去的地方。')


# ════════════════════════════════════════════════════════════════
# 05 · BaziQA 数据集测评（数据背书）
#     ⚠️ 数据诚实红线：只用竞赛 5 模型口径，不混 live 榜，不臆造 Claude
# ════════════════════════════════════════════════════════════════
cover('05-baziqa-1.html', '灵伴 AI · 模型测评 · 四届专家赛真题',
      '我们拿四届<br/>专家赛真题，<br/>考了<span class="em">五个大模型</span>',
      'assets/chart.png', illo_h=440, fit='contain', bg='#ffffff')

shot('05-baziqa-2.html', '模型测评 · 01',
     '结果有点意外：<span class="em">通用模型全在下面</span>',
     'assets/chart.png', '灵伴 AI · live benchmark', '2022–2025 四届宏平均', portrait=False,
     note='蓝色三根是历届冠亚季军的成绩，橙色那根是灵伴，灰色是五个通用大模型。'
          '灵伴 <span class="em">37.1%</span> 排在通用模型全部之上、人类季军之下。')

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
# 06 · 使用教程（收藏率天花板）—— 完整 5 张
#     ⚠️ 上一版是废稿：3 张里没有一张交代「这是什么报告」，封面承诺「看懂一个八边形」
#        但正文从没说八个角分别是什么；「第一步」后面没有第二步；术语（边缘系统 / 小脑）
#        直接扔给读者。用户：「文字内容很差劲，完全不知道在讲什么」。
#     教程的核心价值 = **把术语翻译成日常行为**。这一版把翻译表当主菜。
#     配图：封面全图 + 内页放大到最高/最低两角，两个视角各证各的话。
#     ⚠️ 这个功能另外两张截图（最佳赛道推荐 / 整体天赋画像）满屏文字且含
#        日主·偏印·七杀，双重踩线，不能用。
# ════════════════════════════════════════════════════════════════
cover('06-jiaocheng-1.html', '灵伴 AI · 报告怎么读',
      '那张八边形，<br/>其实只用看<br/><span class="em">两个角</span>',
      'assets/radar.png', title_px=150, illo_h=560, fit='contain', card=True)

body('06-jiaocheng-2.html', '报告怎么读 · 01', [
 '天赋脑图跑完，出来的是一个八边形：八个角是八个脑区，每个角带一个分数。',
 '多数人打开先找最高分，看完一句「哦我边缘系统 85」，然后就没有然后了。',
 '<span class="em">分数本身没什么用</span>——它不是排名，也不跟别人比。'
 '有用的是这张图的形状：哪个角鼓出来，哪个角凹下去。',
])

shot('06-jiaocheng-3.html', '报告怎么读 · 02',
     '第一步：把<span class="em">最高和最低</span>那两个角找出来',
     'assets/radar-zoom.jpg', '灵伴 AI · 天赋脑图', '八个维度 · 只用记两个', portrait=False,
     note='我这张最高是边缘系统 85，最低是小脑 60，差 <span class="em">25 分</span>。'
          '差得越多，这两件事在你身上的省力和费力就越明显。')

body('06-jiaocheng-4.html', '报告怎么读 · 03', [
 '第二步：把这两个名字翻成人话。八个脑区听着像医学名词，'
 '对应的其实都是<span class="em">日常行为</span>——',
 '<span class="em">前额叶</span>　做计划、忍住不做某事<br/>'
 '<span class="em">颞叶</span>　　听人说话、记人记事<br/>'
 '<span class="em">顶叶</span>　　方向感、身体的空间协调<br/>'
 '<span class="em">枕叶</span>　　对画面和视觉信息敏感<br/>'
 '<span class="em">边缘系统</span>　对情绪和气氛敏感<br/>'
 '<span class="em">运动皮层</span>　动手、把事真做出来<br/>'
 '<span class="em">小脑</span>　　手上的精细活<br/>'
 '<span class="em">基底神经节</span>　养习惯、扛重复',
])

body('06-jiaocheng-5.html', '报告怎么读 · 04', [
 '第三步：把这两句连起来读。我那张最高是边缘系统、最低是小脑，'
 '翻译过来就是——对气氛和情绪敏感得过头，但手上的精细活一做就烦。',
 '这解释了我为什么能坐着写一天字，装个柜子能装到砸手。'
 '<span class="em">不是不认真，是那件事在我这儿本来就更费。</span>',
 '<span class="last">你那张最高最低是哪两个，基本就是你最省力和最费力的两件事。'
 '知道这个，比知道分数有用得多。</span>',
])


# ════════════════════════════════════════════════════════════════
# 07 · 灵体大赏（活动 · UGC 共创比赛）
#     用户拍板：不办抽奖，办「灵体好看比赛」，奖品月度会员。
#     比抽奖好在三处：产出 UGC、展示产品最美的部分、合规风险低得多
#     （带话题 tag 正常发笔记 ≠ 引导评论）。
# ════════════════════════════════════════════════════════════════
cover('07-dashang-1.html', '灵伴 AI · 灵体大赏 · 征集中',
      '灵体大赏：<br/>谁的那颗<br/><span class="em">最好看</span>',
      'assets/orbs-dashang.jpg', illo_h=420, pos='center 50%')

body('07-dashang-2.html', '灵体大赏 · 01', [
 '每个人的灵体都是按自己那份出生时间数据算出来的一颗，颜色、形状、亮的位置全不一样。'
 '看得多了会发现，有些人的那颗<span class="em">是真的好看</span>。',
 '所以办一次灵体大赏：带话题标签发一条自己的笔记，把你那颗放出来就行。'
 '我们挑十个，各送<span class="em">一个月会员</span>。',
 '<span class="last">不用在评论区做什么，也不用来找我，正常发笔记就行。'
 '挑完发一条公示，把入选的十颗放一起——那张图应该会很好看。</span>',
])


# ════════════════════════════════════════════════════════════════
# 08 · 节令热点（三伏 → 命理体检 health-wuyun）—— 完整 5 张
#     ⚠️ 上一版是废稿：封面问「最先扛不住的地方」，三张读完从没回答是哪儿；
#        配图是「五运六气」界面条，读者不知道那是什么，也没一句话解释。
#        用户：「文字内容很差劲，完全不知道在讲什么」。
#     这一版按 tuwen-seasonal 的 A+B 混合走：节气文化桥 + 实用清单收尾，
#     并且**把答案说出来**（长夏对应脾），产品截图正好证明它（脾 45 是最低角）。
# ════════════════════════════════════════════════════════════════
cover('08-jieling-1.html', '灵伴 AI · 节气手记',
      '一入伏就没胃口、<br/>吃完就困，<br/><span class="em">不是你懒</span>',
      'assets/wuyun-body.jpg', illo_h=520, fit='contain', card=True)

body('08-jieling-2.html', '节气手记 · 01', [
 '入伏这几天，很多人会同时出现这几样：早上起不来，中午吃两口就饱，'
 '下午三四点整个人是沉的，晚上又睡不踏实。',
 '这不是意志力的问题。三伏是一年里最特殊的一段——'
 '<span class="em">外面最热，人身上的热却都浮在体表，里头反而是空的</span>。',
 '古人干脆把这段从夏天里单拎出来，另给了个名字叫「长夏」。'
 '单独命名，就是因为它跟前面两个月的规律不一样。',
])

body('08-jieling-3.html', '节气手记 · 02', [
 '长夏在这套模型里对应的脏是<span class="em">脾</span>。'
 '脾管的是把吃进去的东西转成能用的力气。',
 '湿气一重它就转不动，于是第一反应就是不想吃、吃完困、身上发沉——'
 '正好是上面那几样。',
 '所以「最先扛不住的地方」不是硬套出来的，'
 '是长夏配土、土配脾这条对应关系直接推下来的。',
])

shot('08-jieling-4.html', '节气手记 · 03',
     '换成形状看，<span class="em">凹得最深的那个角</span>',
     'assets/wuyun-radar.jpg', '灵伴 AI · 五脏读数', '越往里凹越吃力', portrait=False,
     note='封面那张标的是数字：我这份是肝 85、心 70、肾 60、肺 50、<span class="em">脾 45</span>。'
          '这个五边形画的是同一组数——最靠里的那一角就是土（脾），入伏这几天最先撑不住的就是它。'
          '你那张最靠里的是哪一角，值得点开看一眼。')

body('08-jieling-5.html', '节气手记 · 04', [
 '知道是脾在硬撑，这几天该怎么过就清楚了。',
 '<span class="em">少碰冰的</span>——热在体表、里头本来就是凉的，一杯冰饮下去，最先受不了的就是它。<br/>'
 '<span class="em">把午觉睡回来</span>——长夏最耗的是白天那段，补在中午比熬到晚上有用。<br/>'
 '<span class="em">出微汗就行</span>——出汗是散湿的，但汗出大了力气也跟着走。',
 '<span class="last">都是常识，只是这几天格外要紧。'
 '你觉得累，真的不是你懒——是这段时间它本来就难。</span>',
])


print('生成了 8 个 demo 共', len([f for f in os.listdir(HERE) if f.endswith('.html')]), '张 slide')
