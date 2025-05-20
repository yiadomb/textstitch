# Nsadua Textstitch

Phase 1 goal: **CLI tool** that converts a layout JSON into  
* `output.dst` — Tajima-compatible stitches  
* `preview.png` — 130 mm × 250 mm proof image  

## Quick start

```bash
python -m venv .venv      # one-time
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -e .
textstitch --help
