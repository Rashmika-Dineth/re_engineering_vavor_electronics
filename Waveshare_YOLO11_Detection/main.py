"""
Waveshare USB Camera - YOLO11n real-time object detection
Run: python main.py
Keys:
  q / ESC : quit
  s       : save the current annotated frame
  r       : start/stop video recording
"""
from pathlib import Path
import time
import cv2
from ultralytics import YOLO

from camera_config import (
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, CAMERA_BACKEND,
    MODEL_PATH, CONFIDENCE, IOU_THRESHOLD, DISPLAY_WINDOW,
)
from utils.camera import open_camera

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output" / "detections"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    model_path = BASE_DIR / MODEL_PATH
    # Ultralytics downloads yolo11n.pt automatically if it is not present.
    model = YOLO(str(model_path))

    cap = open_camera(
        camera_index=CAMERA_INDEX,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT,
        backend=CAMERA_BACKEND,
    )

    window_name = "Waveshare USB Camera - YOLO11n"
    recording = False
    video_writer = None
    fps = 0.0
    previous_time = time.perf_counter()

    print("Detection started. Press q/ESC to quit, s to save an image, r to record.")
    try:
        while True:
            success, frame = cap.read()
            if not success or frame is None:
                print("Warning: Could not read a frame from the camera.")
                break

            results = model.predict(
                source=frame,
                conf=CONFIDENCE,
                iou=IOU_THRESHOLD,
                verbose=False,
            )
            annotated = results[0].plot()

            now = time.perf_counter()
            elapsed = now - previous_time
            previous_time = now
            if elapsed > 0:
                instant_fps = 1.0 / elapsed
                fps = instant_fps if fps == 0 else (0.9 * fps + 0.1 * instant_fps)

            status = "REC" if recording else "LIVE"
            color = (0, 0, 255) if recording else (0, 220, 0)
            cv2.putText(
                annotated, f"FPS: {fps:.1f}  {status}", (12, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA
            )

            if recording and video_writer is not None:
                video_writer.write(annotated)

            if DISPLAY_WINDOW:
                cv2.imshow(window_name, annotated)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("s"):
                filename = OUTPUT_DIR / f"detection_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
                if cv2.imwrite(str(filename), annotated):
                    print(f"Saved image: {filename}")
            elif key == ord("r"):
                if not recording:
                    height, width = annotated.shape[:2]
                    filename = OUTPUT_DIR / f"recording_{time.strftime('%Y%m%d_%H%M%S')}.mp4"
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                    video_writer = cv2.VideoWriter(str(filename), fourcc, 20.0, (width, height))
                    if not video_writer.isOpened():
                        print("Could not start video recording.")
                        video_writer.release()
                        video_writer = None
                    else:
                        recording = True
                        print(f"Recording to: {filename}")
                else:
                    recording = False
                    if video_writer is not None:
                        video_writer.release()
                        video_writer = None
                    print("Recording stopped.")
    finally:
        if video_writer is not None:
            video_writer.release()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
