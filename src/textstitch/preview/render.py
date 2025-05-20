"""PNG proof rendering for Nsadua Textstitch (Phase 1).

Given a Layout object, draws text and logo placeholders onto a
130 mm × 250 mm (default) canvas and saves a PNG.
"""

from __future__ import annotations

import math
import pathlib
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = pathlib.Path(__file__).resolve().parents[3] / "assets" / "fonts"
DPI = 300  # high-res proof (≈ 12 px per mm)

# ------------------------- helpers ------------------------- #


def mm_to_px(mm: float) -> int:
    """Convert millimetres to integer pixels at chosen DPI."""
    return int(round(mm / 25.4 * DPI))


def find_font_file(font_name: str) -> pathlib.Path:
    """
    Very small helper that tries to map a 'friendly' font name
    (e.g. 'Arial Bold') to a .ttf stored in assets/fonts/.
    You can extend this mapping as you add fonts.
    """
    mapping = {
        "Arial Bold": "Arial-Bold.ttf",
        "Bloodhound Bold": "Bloodhound-Bold.ttf",
    }
    filename = mapping.get(font_name, None)
    if filename:
        path = ASSETS_DIR / filename
        if path.exists():
            return path
    # Fallback to a PIL default font
    return ImageFont.load_default().path  # type: ignore


def draw_text(draw: ImageDraw.ImageDraw, obj, canvas_h_px):
    """Render a TextObject onto the image."""
    # Convert font size mm → points (1 pt ≈ 0.3528 mm)
    pt_size = obj.font_size_mm / 0.3528
    font_path = find_font_file(obj.font)
    font = ImageFont.truetype(str(font_path), size=int(pt_size))

    # Measure text
    text_w, text_h = draw.textsize(obj.text, font=font)

    # Compute anchor offsets
    if obj.anchor == "centre":
        dx = -text_w // 2
    elif obj.anchor == "right":
        dx = -text_w
    else:
        dx = 0

    # Position in px
    x_px = mm_to_px(obj.x_mm) + dx
    # Y origin in our spec is top-down from canvas origin,
    # but PIL also draws top-down. No inversion needed.
    y_px = mm_to_px(obj.y_mm) - text_h // 2

    if obj.orientation_deg == 0:
        draw.text((x_px, y_px), obj.text, font=font, fill="black")
    elif obj.orientation_deg == 90:
        # Rotate text by drawing onto its own image
        txt_img = Image.new("RGBA", (text_w, text_h), (255, 0, 0, 0))
        ImageDraw.Draw(txt_img).text((0, 0), obj.text, font=font, fill="black")
        txt_img = txt_img.rotate(90, expand=True)
        draw.bitmap(
            (x_px, y_px),
            txt_img,
        )
    else:
        raise ValueError("Only 0° or 90° orientations are supported.")


# ------------------------- main entry ------------------------- #


def render_png(layout, png_out: pathlib.Path, bg="white"):
    print("🖼️ render_png() has started...")

    """Draw the entire layout onto a PNG proof."""
    w_px = mm_to_px(layout.canvas_width_mm)
    h_px = mm_to_px(layout.canvas_height_mm)

    img = Image.new("RGB", (w_px, h_px), color=bg)
    draw = ImageDraw.Draw(img)

    for obj in layout.objects:
        if obj.__class__.__name__ == "TextObject":
            draw_text(draw, obj, h_px)
        elif obj.__class__.__name__ == "LogoObject":
            # Phase 1: draw a placeholder box for logos
            box_w = box_h = mm_to_px(20 * obj.scale)
            x_px = mm_to_px(obj.x_mm) - box_w // 2
            y_px = mm_to_px(obj.y_mm) - box_h // 2
            draw.rectangle([x_px, y_px, x_px + box_w, y_px + box_h],
                           outline="black", width=2)
            draw.text((x_px + 4, y_px + 4), "LOGO", fill="black")
        else:
            raise ValueError("Unknown object type:", obj)

    img.save(png_out, format="PNG")
