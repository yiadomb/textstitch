"""Command-line interface for Nsadua Textstitch.

Usage
-----
textstitch layout.json --dst-out out.dst --png-out preview.png
"""

from __future__ import annotations

import json
from pathlib import Path

import click

from textstitch.engine.layout import Layout
from textstitch.preview.render import render_png

# ── DST writer ──────────────────────────────────────────────────────────────
# We haven’t built engine/writer.py yet.  Try to import it; if it doesn’t
# exist, fall back to a harmless placeholder so the CLI keeps working.

try:
    from textstitch.engine.writer import write_dst  # will implement later
except ModuleNotFoundError:  # pragma: no cover
    def write_dst(layout: Layout, dst_path: Path) -> None:  # type: ignore
        """Temporary stub until writer.py is implemented."""
        dst_path.write_bytes(b"")  # creates 0-byte file as a placeholder


# ── Click entry-point ───────────────────────────────────────────────────────

@click.command()
@click.argument(
    "layout_json",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--dst-out",
    default="output.dst",
    show_default=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Destination Tajima DST file.",
)
@click.option(
    "--png-out",
    default="preview.png",
    show_default=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Destination proof PNG file.",
)
def app(layout_json: Path, dst_out: Path, png_out: Path) -> None:
    """Convert *layout_json* into a DST file and PNG preview."""
    data = json.loads(layout_json.read_text(encoding="utf-8"))
    layout = Layout.from_dict(data)

    # --- generate outputs ---------------------------------------------------
    write_dst(layout, dst_out)      # currently a no-op
    render_png(layout, png_out)     # fully implemented

    click.echo(f"✅  Saved {dst_out}  and  {png_out}")


if __name__ == "__main__":
    app()
