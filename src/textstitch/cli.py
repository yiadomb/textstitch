"""Command-line interface for Textstitch."""
import json, pathlib, click
from textstitch.engine.layout import Layout

# stubs we'll fill in later
def write_dst(layout, path): path.write_bytes(b'')
def render_png(layout, path): path.write_bytes(b'')

@click.command()
@click.argument("layout_json", type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("--dst-out", default="output.dst", type=click.Path(path_type=pathlib.Path))
@click.option("--png-out", default="preview.png", type=click.Path(path_type=pathlib.Path))
def app(layout_json: pathlib.Path, dst_out: pathlib.Path, png_out: pathlib.Path):
    """Convert a layout JSON into DST + PNG (stub)."""
    data = json.loads(layout_json.read_text(encoding="utf-8"))
    layout = Layout.from_dict(data)
    write_dst(layout, dst_out)
    render_png(layout, png_out)
    click.echo(f"✅  Saved {dst_out} and {png_out}")

if __name__ == "__main__":
    app()
