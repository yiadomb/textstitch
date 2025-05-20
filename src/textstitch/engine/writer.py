"""DST writer stub (Phase 1).

For now it just creates an empty file so the CLI doesn’t crash.
We will replace this with real stitch generation once the satin
algorithm is ready.
"""

from pathlib import Path

from textstitch.engine.layout import Layout


def write_dst(layout: Layout, dst_out: Path) -> None:
    """Write a placeholder 0-byte DST file."""
    dst_out.write_bytes(b"")
