"""Render lossless, looping APNGs at each asset's declared pixel scale."""

import argparse
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import Browser, sync_playwright

from profile_art import ASSETS, render_svg


REPO = Path(__file__).resolve().parents[1]
ATLAS = REPO / "assets" / "chiikawa-sprites.png"


def render_asset(browser: Browser, spec: dict, work_dir: Path) -> dict:
    name = spec["name"]
    width, height = spec["width"], spec["height"]
    fps = spec["fps"]
    scale = spec["scale"]
    expected_size = (width * scale, height * scale)
    frame_count = round(spec["duration"] * fps)
    frame_duration_ms = 1000 / fps
    asset_work_dir = work_dir / name
    asset_work_dir.mkdir(parents=True, exist_ok=True)
    source = asset_work_dir / "source.svg"
    source.write_text(render_svg(name, ATLAS), encoding="utf-8")

    page = browser.new_page(
        viewport={"width": width, "height": height},
        device_scale_factor=scale,
        reduced_motion="no-preference",
    )
    source_frames = []
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
            frame_path = asset_work_dir / f"frame_{frame:05d}.png"
            page.screenshot(
                path=str(frame_path),
                animations="allow",
                omit_background=True,
                scale="device",
            )
            with Image.open(frame_path) as captured:
                source_frames.append(captured.convert("RGBA"))
    finally:
        page.close()

    output = REPO / "assets" / f"{name}.png"
    source_frames[0].save(
        output,
        format="PNG",
        save_all=True,
        append_images=source_frames[1:],
        duration=frame_duration_ms,
        loop=0,
        disposal=0,
        blend=0,
        optimize=True,
        compress_level=9,
    )

    with Image.open(output) as animation:
        if animation.format != "PNG" or not animation.is_animated:
            raise ValueError(f"{name}: expected an animated PNG")
        actual_size = animation.size
        frames = animation.n_frames
        loop = animation.info.get("loop")
        if actual_size != expected_size:
            raise ValueError(f"{name}: expected {expected_size}, got {actual_size}")
        if frames != frame_count:
            raise ValueError(f"{name}: expected {frame_count} frames, got {frames}")
        duration_ms = 0
        transparent_frames = 0
        soft_alpha_frames = 0
        disposal_ops = set()
        blend_ops = set()
        for index, source_frame in enumerate(source_frames):
            animation.seek(index)
            decoded = animation.convert("RGBA")
            if decoded.tobytes() != source_frame.tobytes():
                raise ValueError(f"{name}: frame {index} differs from the source RGBA")
            duration_ms += animation.info.get("duration", 0)
            disposal_ops.add(animation.info.get("disposal"))
            blend_ops.add(animation.info.get("blend"))
            alpha_histogram = decoded.getchannel("A").histogram()
            if alpha_histogram[0]:
                transparent_frames += 1
            if sum(alpha_histogram[1:255]):
                soft_alpha_frames += 1
    expected_ms = spec["duration"] * 1000
    if loop != 0:
        raise ValueError(f"{name}: expected infinite looping, got loop={loop}")
    if transparent_frames != frames or soft_alpha_frames != frames:
        raise ValueError(f"{name}: every frame must preserve transparency and soft alpha")
    if disposal_ops != {0} or blend_ops != {0}:
        raise ValueError(f"{name}: expected APNG disposal 0 and source blend 0")
    if abs(duration_ms - expected_ms) > 1:
        raise ValueError(
            f"{name}: expected {expected_ms} ms, got {duration_ms} ms"
        )
    for source_frame in source_frames:
        source_frame.close()

    result = {
        "name": name,
        "format": "APNG",
        "width": actual_size[0],
        "height": actual_size[1],
        "css_width": width,
        "css_height": height,
        "scale": scale,
        "frames": frames,
        "source_frames": frame_count,
        "fps": fps,
        "duration_ms": duration_ms,
        "expected_duration_ms": expected_ms,
        "loop": loop,
        "exact_source_frames": frames,
        "transparent_frames": transparent_frames,
        "soft_alpha_frames": soft_alpha_frames,
        "disposal_ops": sorted(disposal_ops),
        "blend_ops": sorted(blend_ops),
        "bytes": output.stat().st_size,
        "output": str(output),
    }
    print(
        f"{name}: {actual_size[0]}x{actual_size[1]} APNG, {frames} frames, {duration_ms} ms, "
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
    work_dir.mkdir(parents=True, exist_ok=True)

    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for name in names:
                results.append(render_asset(browser, specs[name], work_dir))
        finally:
            browser.close()
    (work_dir / "render-checks.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
