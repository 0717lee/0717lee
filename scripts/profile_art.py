"""Animated engineering notes for the light and dark GitHub profile themes."""
import base64
from pathlib import Path

ASSET_NAMES = ("chiikawa-engineering", "chiikawa-engineering-dark")
CROPS = {
    0:(24,180,400,440), 1:(449,174,401,443), 2:(855,102,377,520),
    6:(6,184,458,468), 7:(466,190,364,465), 8:(924,97,782,746),
    9:(48,73,814,786), 10:(440,738,420,430),
}
CAST = [(0,"吉伊"),(1,"小八"),(2,"乌萨奇"),(6,"飞鼠"),
        (7,"古本屋"),(8,"狮萨"),(9,"师傅"),(10,"栗子馒头")]
# Align perceived character size rather than including ears, tails or capes.
FACE_WIDTH = {0:280,1:285,2:260,6:305,7:285,8:590,9:605,10:315}
FEET = {0:584,1:591,2:593,6:632,7:635,8:831,9:847,10:1147}


def sprite(index,center_x,baseline,face_width,motion):
    cx,cy,cw,ch = CROPS[index]
    scale = face_width / FACE_WIDTH[index]
    w,h = cw * scale,ch * scale
    x,y = center_x - w / 2,baseline - (FEET[index] - cy) * scale
    atlas = "refined-atlas" if index in (8,9) else "atlas" if index < 6 else "friends-atlas"
    return f'<g class="{motion}" data-character="{index}"><svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{cx} {cy} {cw} {ch}" overflow="hidden" preserveAspectRatio="xMidYMid meet"><g clip-path="url(#crop-{index})"><use href="#{atlas}"/></g></svg></g>'


def engineering(name, definitions, clips):
    dark = name.endswith("-dark")
    ink, muted, line = ("#e7ebe8", "#a9b8b1", "#52625c") if dark else ("#33463e", "#687f73", "#c6d4cd")
    people = (
        sprite(0,250,166,37,"working")
        + sprite(7,30,180,24,"reading-note")
        + sprite(1,594,165,37,"working-late")
        + sprite(2,353,159,23,"reading-note")
        + sprite(9,881,164,37,"working")
        + sprite(6,936,114,23,"floating-note")
        + sprite(8,323,217,24,"working-late")
        + sprite(10,641,217,24,"reading-note")
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="224" viewBox="0 0 960 224" fill="none" role="img" aria-labelledby="title">
<title id="title">Frontend interfaces, AI agents and applications</title>
<defs>{definitions}{clips}</defs>
<style>
text {{ font-family: "Microsoft YaHei", sans-serif; fill: {ink}; }}
.meta {{ font-family: "Consolas", monospace; font-size: 12px; letter-spacing: 1.4px; fill: {muted}; }}
.label {{ font-size: 19px; font-weight: 600; }}
.detail {{ font-size: 13px; fill: {muted}; }}
.working {{ animation: work 4s ease-in-out infinite; }}
.working-late {{ animation: work 4s ease-in-out -1s infinite; }}
.reading-note {{ transform-box: fill-box; transform-origin: bottom center; animation: note 4s ease-in-out infinite; }}
.floating-note {{ animation: float-note 4s ease-in-out infinite; }}
.signal {{ animation: signal 4s linear infinite; }}
.cursor {{ animation: cursor 4s ease-in-out infinite; }}
@keyframes work {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
@keyframes note {{ 0%,100% {{ transform: rotate(0); }} 50% {{ transform: rotate(-2deg); }} }}
@keyframes float-note {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-4px); }} }}
@keyframes signal {{ 0% {{ transform: translateX(0); opacity: 0; }} 15%,75% {{ opacity: 1; }} 90%,100% {{ opacity: 0; }} 100% {{ transform: translateX(47px); }} }}
@keyframes cursor {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
</style>
<text class="meta" x="28" y="26">FRONTEND / AI AGENTS</text>
<path d="M208 22H932" stroke="{line}"/>
<g stroke="{line}" stroke-width="1.3">
<path d="M30 57H288V153H30ZM350 57H608V153H350ZM670 57H928V153H670"/>
<path d="M294 104H344m270 0h50"/>
</g>
<g class="signal"><rect x="296" y="101" width="6" height="6" fill="{muted}"/><rect x="616" y="101" width="6" height="6" fill="{muted}"/></g>
<g stroke="{muted}" stroke-width="1.5"><rect x="46" y="80" width="43" height="37" rx="3"/><path d="M46 90H89M57 97V111M64 99H82M64 107H76"/><circle cx="52" cy="85" r="1" fill="{muted}"/><circle cx="57" cy="85" r="1" fill="{muted}"/></g>
<text class="label" x="107" y="99">前端交互</text>
<text class="detail" x="107" y="125">React / TypeScript</text>
<g stroke="{muted}" stroke-width="1.7"><path d="M385 89H407M382 94L393 114M409 94L399 114"/><circle cx="380" cy="89" r="5"/><circle cx="412" cy="89" r="5"/><circle cx="396" cy="119" r="5"/></g>
<text class="label" x="447" y="99">AI Agent</text>
<text class="detail" x="447" y="125">LangGraph / tools</text>
<g stroke="{muted}" stroke-width="1.5" stroke-linejoin="round"><path d="M691 87Q701 82 711 87Q721 82 731 87V121Q721 116 711 121Q701 116 691 121ZM711 87V121M697 95L706 97M697 103L706 105M716 97L725 95M716 105L725 103"/></g>
<text class="label" x="754" y="99">AI 应用</text>
<text class="detail" x="754" y="125">RAG / OCR</text>
<text class="meta" x="61" y="188">01 / COLLABBOARD</text>
<text class="meta" x="384" y="188">02 / MAINTAINER</text>
<text class="meta" x="697" y="188">03 / WENDAO</text>
{people}
<path d="M28 219H290m68 0h248m70 0h256" stroke="{line}"/>
<rect class="cursor" x="921" y="24" width="9" height="2" fill="{muted}"/>
</svg>'''


def render_svg(name: str, atlas_path: Path) -> str:
    if name not in ASSET_NAMES:
        raise ValueError(f"Unknown asset: {name}")
    images = [
        ("atlas",atlas_path,1254,1254),
        ("friends-atlas",atlas_path.with_name("chiikawa-friends.png"),1254,1254),
        ("refined-atlas",atlas_path.with_name("chiikawa-refined.png"),1774,887),
    ]
    definitions = "".join(
        f'<image id="{id_}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(path.read_bytes()).decode("ascii")}"/>'
        for id_,path,w,h in images
    )
    clips = "".join(f'<clipPath id="crop-{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>' for i,(x,y,w,h) in CROPS.items())
    return engineering(name, definitions, clips)
