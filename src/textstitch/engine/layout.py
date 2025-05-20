"""Data classes for layout JSON."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal, Any

Anchor = Literal["left", "centre", "right"]

@dataclass
class TextObject:
    text: str
    font: str
    font_size_mm: float
    x_mm: float
    y_mm: float
    anchor: Anchor = "left"
    orientation_deg: int = 0  # 0 or 90

@dataclass
class LogoObject:
    file: str
    x_mm: float
    y_mm: float
    scale: float = 1.0

@dataclass
class Layout:
    canvas_width_mm: float
    canvas_height_mm: float
    objects: List[Any]

    @classmethod
    def from_dict(cls, data: dict) -> "Layout":
        objs = []
        for obj in data.get("objects", []):
            kind = obj.get("type")
            if kind == "text":
                # copy obj and remove the 'type' key before unpacking
                t = obj.copy()
                t.pop("type", None)
                objs.append(TextObject(**t))
            elif kind == "logo":
                l = obj.copy()
                l.pop("type", None)
                objs.append(LogoObject(**l))
            else:
                raise ValueError(f"Unknown object type: {kind}")
        canvas = data.get("canvas", {})
        return cls(
            canvas_width_mm=canvas.get("width_mm", 130),
            canvas_height_mm=canvas.get("height_mm", 250),
            objects=objs,
        )
