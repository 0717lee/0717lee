"""Export self-contained native SVG animations for the GitHub profile."""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

from profile_art import ASSETS, CAST, render_svg

REPO = Path(__file__).resolve().parents[1]
ATLAS = REPO / "assets" / "chiikawa-sprites.png"


def export_asset(name: str) -> Path:
    source = render_svg(name, ATLAS)
    tree = ET.fromstring(source)
    characters = sorted(
        int(node.attrib["data-character"])
        for node in tree.iter()
        if "data-character" in node.attrib
    )
    if characters != sorted(index for index, _ in CAST):
        raise ValueError(f"{name}: character roster differs from CAST")
    if "steps(" in source:
        raise ValueError(f"{name}: stepped timing breaks continuous motion")
    for node in tree.iter():
        if node.tag.rsplit("}", 1)[-1] in {"script", "foreignObject"}:
            raise ValueError(f"{name}: SVG must remain an image-only document")
        href = node.attrib.get("href", "")
        if href and not href.startswith(("#", "data:image/png;base64,")):
            raise ValueError(f"{name}: external SVG resource: {href}")
    output = REPO / "assets" / f"{name}.svg"
    output.write_text(source, encoding="utf-8")
    print(f"{name}: native SVG, {len(characters)} characters, {output.stat().st_size} bytes")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assets", nargs="*", help="Asset names; defaults to both themes")
    args = parser.parse_args()
    known = {spec["name"] for spec in ASSETS}
    names = list(dict.fromkeys(args.assets)) if args.assets else [s["name"] for s in ASSETS]
    unknown = [name for name in names if name not in known]
    if unknown:
        parser.error(f"Unknown assets: {', '.join(unknown)}")
    for name in names:
        export_asset(name)


if __name__ == "__main__":
    main()
