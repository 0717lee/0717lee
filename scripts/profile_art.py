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
    pixels = "".join(
        f'<rect x="{48+col*14}" y="{80+row*14}" width="10" height="10" rx="1" fill="{color}"/>'
        for row, colors in enumerate([
            ["#b1cfc0", "#b1cfc0", "#dfc9b2"],
            ["#b1cfc0", "#6b9a87", "#dfc9b2"],
            ["#acc4d2", "#6b9a87", "#acc4d2"],
        ]) for col, color in enumerate(colors)
    )
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
<title id="title">Engineering notes — image processing, runtime interfaces and maintainer tools</title>
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
<text class="meta" x="28" y="26">ENGINEERING NOTES</text>
<path d="M208 22H932" stroke="{line}"/>
<g stroke="{line}" stroke-width="1.3">
<path d="M30 57H288V153H30ZM350 57H608V153H350ZM670 57H928V153H670"/>
<path d="M294 104H344m270 0h50"/>
</g>
<g class="signal"><rect x="296" y="101" width="6" height="6" fill="{muted}"/><rect x="616" y="101" width="6" height="6" fill="{muted}"/></g>
{pixels}
<text class="label" x="107" y="99">图像处理</text>
<text class="detail" x="107" y="125">pixels / codecs</text>
<g stroke="{muted}" stroke-width="1.7" stroke-linejoin="round"><path d="M385 83l-14 14 14 14m29-28 14 14-14 14m-8-31-13 37"/></g>
<text class="label" x="447" y="99">运行时接口</text>
<text class="detail" x="447" y="125">Wasm-GC / ABI</text>
<g stroke="{muted}" stroke-width="1.5"><path d="M691 82h38v12h-38Zm0 19h29v12h-29Zm0 19h20v12h-20Z"/></g>
<text class="label" x="754" y="99">维护工具</text>
<text class="detail" x="754" y="125">triage / review</text>
<text class="meta" x="61" y="188">01 / PIXELFORGE</text>
<text class="meta" x="384" y="188">02 / MOONHOSTABI</text>
<text class="meta" x="697" y="188">03 / MAINTAINER</text>
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
