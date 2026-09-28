"""Render checked, looping GIFs with each asset's transparency and palette settings.

Asset specs may set transparent=False for opaque, delta-encoded GIFs and
palette_colors=2..256; defaults are transparent=True and palette_colors=128.
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageSequence
from playwright.sync_api import Browser, sync_playwright

from profile_art import ASSETS, render_svg


REPO = Path(__file__).resolve().parents[1]
ATLAS = REPO / "assets" / "chiikawa-sprites.png"


def render_asset(browser: Browser, spec: dict, work_dir: Path, ffmpeg: str) -> dict:
    name = spec["name"]
    width, height = spec["width"], spec["height"]
    fps = spec["fps"]
    transparent = spec.get("transparent", True)
    palette_colors = spec.get("palette_colors", 128)
    if not 2 <= palette_colors <= 256:
        raise ValueError(f"{name}: palette_colors must be between 2 and 256")
    frame_count = round(spec["duration"] * fps)
    asset_work_dir = work_dir / name
    asset_work_dir.mkdir(parents=True, exist_ok=True)
    source = asset_work_dir / "source.svg"
    source.write_text(render_svg(name, ATLAS), encoding="utf-8")

    page = browser.new_page(
        viewport={"width": width, "height": height},
        device_scale_factor=1,
        reduced_motion="no-preference",
    )
    try:
        page.goto(source.as_uri(), wait_until="load")
        page.evaluate("() => document.fonts.ready")
        page.evaluate(
            """() => {
                for (const animation of document.getAnimations()) {
                    animation.pause();
                    animation.currentTime = 0;
                }
            }"""
        )
        for frame in range(frame_count):
            page.evaluate(
                """time => {
                    for (const animation of document.getAnimations()) {
                        animation.currentTime = time;
                    }
                }""",
                frame * 1000 / fps,
            )
            page.screenshot(
                path=str(asset_work_dir / f"frame_{frame:05d}.png"),
                animations="allow",
                omit_background=transparent,
                scale="css",
            )
    finally:
        page.close()

    output = REPO / "assets" / f"{name}.gif"
    # Opaque GIFs also need a transparent palette entry for unchanged delta pixels.
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel", "error",
            "-y",
            "-framerate", str(fps),
            "-start_number", "0",
            "-t", str(spec["duration"]),
            "-i", str(asset_work_dir / "frame_%05d.png"),
            "-filter_complex",
            "[0:v]split[frames][colors];"
            f"[colors]palettegen=max_colors={palette_colors}:stats_mode=diff:"
            "reserve_transparent=1[palette];"
            "[frames][palette]paletteuse=dither=bayer:bayer_scale=5:"
            "diff_mode=rectangle:alpha_threshold=128",
            "-frames:v", str(frame_count),
            *(["-gifflags", "-offsetting-transdiff"] if transparent else []),
            "-loop", "0",
            str(output),
        ],
        check=True,
    )

    with Image.open(output) as gif:
        actual_size = gif.size
        frames = gif.n_frames
        loop = gif.info.get("loop")
        duration_ms = 0
        transparent_frames = 0
        opaque_frames = 0
        disposal_methods = set()
        for frame in ImageSequence.Iterator(gif):
            duration_ms += frame.info.get("duration", 0)
            disposal_methods.add(frame.disposal_method)
            alpha_min = frame.convert("RGBA").getchannel("A").getextrema()[0]
            if alpha_min == 0:
                transparent_frames += 1
            elif alpha_min == 255:
                opaque_frames += 1
    expected_ms = spec["duration"] * 1000
    if actual_size != (width, height):
        raise ValueError(f"{name}: expected {width}x{height}, got {actual_size}")
    if frames <= 1:
        raise ValueError(f"{name}: expected animation, got {frames} frame")
    if loop != 0:
        raise ValueError(f"{name}: expected infinite looping, got loop={loop}")
    if transparent:
        if transparent_frames != frames:
            raise ValueError(f"{name}: {frames - transparent_frames} frames lost transparency")
        if disposal_methods != {2}:
            raise ValueError(f"{name}: expected background disposal 2, got {disposal_methods}")
    elif opaque_frames != frames:
        raise ValueError(f"{name}: {frames - opaque_frames} frames are not fully opaque")
    if abs(duration_ms - expected_ms) > 50:
        raise ValueError(
            f"{name}: expected {expected_ms} ms, got {duration_ms} ms"
        )

    result = {
        "name": name,
        "width": width,
        "height": height,
        "frames": frames,
        "source_frames": frame_count,
        "fps": fps,
        "duration_ms": duration_ms,
        "expected_duration_ms": expected_ms,
        "loop": loop,
        "transparent": transparent,
        "palette_colors": palette_colors,
        "transparent_frames": transparent_frames,
        "opaque_frames": opaque_frames,
        "disposal_methods": sorted(disposal_methods),
        "bytes": output.stat().st_size,
        "output": str(output),
    }
    print(
        f"{name}: {width}x{height}, {frames} frames, {duration_ms} ms, "
        f"loop={loop}, {result['bytes']} bytes",
        flush=True,
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assets", nargs="*", help="Asset names; defaults to all assets")
    parser.add_argument(
        "--work-dir", type=Path, required=True,
        help="Directory outside the repository for temporary SVGs, frames, and checks",
    )
    args = parser.parse_args()
    specs = {spec["name"]: spec for spec in ASSETS}
    names = list(dict.fromkeys(args.assets)) if args.assets else list(specs)
    unknown = [name for name in names if name not in specs]
    if unknown:
        parser.error(f"Unknown assets: {', '.join(unknown)}")
    work_dir = args.work_dir.expanduser().resolve()
    if work_dir.is_relative_to(REPO):
        parser.error("--work-dir must be outside the repository")
    if not ATLAS.is_file():
        parser.error(f"Sprite atlas does not exist: {ATLAS}")
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        parser.error("ffmpeg is not available on PATH")
    work_dir.mkdir(parents=True, exist_ok=True)

    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for name in names:
                results.append(render_asset(browser, specs[name], work_dir, ffmpeg))
        finally:
            browser.close()
    (work_dir / "render-checks.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
