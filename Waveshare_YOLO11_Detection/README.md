# Waveshare USB Camera - YOLO11n Object Detection

Real-time object detection on a Windows PC using a Waveshare USB/UVC camera,
OpenCV and Ultralytics YOLO11n.

## 1. Requirements

- Windows 10 or Windows 11
- Python 3.10-3.12 recommended
- Waveshare USB camera connected to the PC
- Internet connection for the first model download
- A CUDA-compatible NVIDIA GPU is optional; CPU inference is supported

## 2. Project structure

```text
Waveshare_YOLO11_Detection/
├── main.py
├── camera_config.py
├── requirements.txt
├── README.md
├── models/
│   └── (yolo11n.pt is downloaded here if you place it here)
├── output/
│   └── detections/
└── utils/
    ├── __init__.py
    └── camera.py
```

## 3. Create and activate a virtual environment

Open PowerShell in this project folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Connect and configure the camera

Connect the Waveshare camera using USB. Close Windows Camera and other apps that
may be using it.

Open `camera_config.py` and set `CAMERA_INDEX`:
- `0`: first camera (often the built-in webcam)
- `1`: second camera (often an external USB camera)
- `2`: third camera, and so on

If the camera does not open with `DSHOW`, try `MSMF` or `ANY`.

## 5. Run the detector

```powershell
python main.py
```

The first run downloads the official Ultralytics `yolo11n.pt` model automatically.
The file may be stored in the Ultralytics cache. To keep a local copy in this
project, download/copy it into `models/yolo11n.pt`; the configured path will then
use that local file.

## 6. Keyboard controls

| Key | Action |
|---|---|
| `q` or `Esc` | Quit |
| `s` | Save the current annotated frame as JPG |
| `r` | Start or stop MP4 video recording |

Images and recordings are saved in `output/detections/`.

## 7. Settings

Edit `camera_config.py`:
- `CAMERA_INDEX`: camera number
- `FRAME_WIDTH`, `FRAME_HEIGHT`: requested camera resolution
- `CAMERA_BACKEND`: `DSHOW`, `MSMF`, or `ANY`
- `CONFIDENCE`: minimum detection confidence (0.0-1.0)
- `IOU_THRESHOLD`: NMS intersection-over-union threshold

## 8. Notes and troubleshooting

- If you see a camera-open error, try camera index 1, then 2.
- If another application is using the camera, close that application and retry.
- If the requested resolution is unsupported, the camera may choose a different
  resolution; the actual resolution is printed when the camera opens.
- CPU inference can be slower than GPU inference. Start with 640x480 if needed.
- The standard YOLO11 COCO pretrained model detects 80 common classes. It will
  not automatically recognize every custom object. Custom training is needed
  for objects outside its training classes.
- The model name is **`yolo11n.pt`**, not `yolov11n.pt`.

## References

- Ultralytics documentation: https://docs.ultralytics.com/
- Ultralytics prediction mode: https://docs.ultralytics.com/modes/predict/
