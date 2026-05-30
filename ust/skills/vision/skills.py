"""
ust.skills.vision
─────────────────
Branch: "vision"

Skills:
  - take_screenshot_hd  → Full-res screenshot with metadata
  - analyze_screenshot  → Screenshot + describe with AI vision (if available)
  - find_on_screen      → Locate an image/icon on screen (template matching)
  - get_screen_size     → Resolution + display info

Dependencies: mss, pillow
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from ust.core.registry import skill


def _require(package: str, pip_name: str | None = None):
    import importlib
    try:
        return importlib.import_module(package)
    except ImportError:
        raise ImportError(
            f"Package '{pip_name or package}' required.\n"
            f"Install: pip install 'universal-skill-tree[vision]'"
        )


@skill(
    name="get_screen_size",
    branch="vision",
    description="Get the screen resolution and number of monitors.",
    parameters={"properties": {}},
)
def get_screen_size() -> str:
    try:
        import mss
        with mss.mss() as sct:
            monitors = []
            for i, m in enumerate(sct.monitors):
                monitors.append({
                    "index":  i,
                    "left":   m["left"],
                    "top":    m["top"],
                    "width":  m["width"],
                    "height": m["height"],
                })
        return json.dumps({"monitors": monitors}, indent=2)
    except Exception as e:
        return f"ERROR: {e}"


@skill(
    name="screenshot",
    branch="vision",
    description=(
        "Take a screenshot of the full screen or a specific region. "
        "Returns the path to the saved PNG file. "
        "Use get_screen_size first to know the dimensions."
    ),
    parameters={
        "properties": {
            "region": {
                "type": "string",
                "description": "'full' for full screen, or 'x,y,width,height' for a region",
                "default": "full",
            },
            "save_path": {
                "type": "string",
                "description": "Where to save. Default: system temp directory.",
            },
            "monitor": {
                "type": "integer",
                "description": "Monitor index (0 = all monitors combined, 1 = primary). Default: 1",
                "default": 1,
            },
        },
    },
)
def screenshot(
    region: str = "full",
    save_path: str | None = None,
    monitor: int = 1,
) -> str:
    try:
        import mss
        import mss.tools
        from PIL import Image

        with mss.mss() as sct:
            if region != "full":
                try:
                    x, y, w, h = map(int, region.split(","))
                    grab_region = {"top": y, "left": x, "width": w, "height": h}
                except ValueError:
                    return "ERROR: region must be 'full' or 'x,y,width,height'"
            else:
                mon_idx = min(monitor, len(sct.monitors) - 1)
                grab_region = sct.monitors[mon_idx]

            raw = sct.grab(grab_region)
            img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")

            if not save_path:
                tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False, prefix="ust_screenshot_")
                save_path = tmp.name
                tmp.close()

            p = Path(save_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(p))

            return json.dumps({
                "path":   str(p),
                "width":  raw.width,
                "height": raw.height,
            }, indent=2)
    except Exception as e:
        return f"ERROR: {e}"


@skill(
    name="find_on_screen",
    branch="vision",
    description=(
        "Find the pixel coordinates of a template image on the current screen. "
        "Useful to locate buttons or UI elements before clicking. "
        "Returns (x, y) center of the match, or 'not found'."
    ),
    parameters={
        "properties": {
            "template_path": {"type": "string", "description": "Path to the template image to search for"},
            "threshold":     {"type": "number",  "description": "Match confidence 0.0-1.0 (default: 0.8)"},
        },
        "required": ["template_path"],
    },
)
def find_on_screen(template_path: str, threshold: float = 0.8) -> str:
    try:
        import numpy as np
        import cv2
        import mss
        from PIL import Image

        # Grab screen
        with mss.mss() as sct:
            raw = sct.grab(sct.monitors[1])
            screen = np.array(Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX"))
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

        # Load template
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            return f"ERROR: Cannot read template image: {template_path}"

        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            th, tw = template.shape
            cx = max_loc[0] + tw // 2
            cy = max_loc[1] + th // 2
            return json.dumps({"found": True, "x": cx, "y": cy, "confidence": round(max_val, 3)})
        else:
            return json.dumps({"found": False, "confidence": round(max_val, 3)})
    except ImportError:
        return "ERROR: Install opencv-python and numpy for find_on_screen"
    except Exception as e:
        return f"ERROR: {e}"
