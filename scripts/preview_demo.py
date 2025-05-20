# test_preview.py
import json
from pathlib import Path

from textstitch.engine.layout import Layout
from textstitch.preview.render import render_png

layout_json = Path("assets/samples/sample_layout.json")
data = json.loads(layout_json.read_text(encoding="utf-8"))
layout = Layout.from_dict(data)

print("Calling render_png directly …")
render_png(layout, Path("test_preview.png"))
print("Done!")
