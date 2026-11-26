"""Camera and detection settings. Adjust these values for your camera."""
from pathlib import Path

# Most Windows USB/UVC cameras are camera index 0 or 1.
CAMERA_INDEX = 1

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# On Windows, DirectShow is often reliable for USB cameras.
CAMERA_BACKEND = "DSHOW"  # Options: "DSHOW", "MSMF", "ANY"

# Correct Ultralytics YOLO11 nano model filename.
# The model is downloaded automatically by Ultralytics when first used.
MODEL_PATH = Path("models") / "yolo11n.pt"

CONFIDENCE = 0.40
IOU_THRESHOLD = 0.45
DISPLAY_WINDOW = True
