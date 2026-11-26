"""OpenCV USB camera initialization helpers."""
import cv2


def _backend_from_name(name):
    name = name.upper()
    backends = {
        "DSHOW": cv2.CAP_DSHOW,
        "MSMF": cv2.CAP_MSMF,
        "ANY": cv2.CAP_ANY,
    }
    if name not in backends:
        raise ValueError(f"Unsupported camera backend: {name}")
    return backends[name]


def open_camera(camera_index=0, width=1280, height=720, backend="DSHOW"):
    api = _backend_from_name(backend)
    cap = cv2.VideoCapture(camera_index, api)

    if not cap.isOpened():
        cap.release()
        # Try OpenCV's automatic backend as a fallback.
        cap = cv2.VideoCapture(camera_index, cv2.CAP_ANY)

    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open camera index {camera_index}. "
            "Check the USB connection, close other camera applications, "
            "and try CAMERA_INDEX = 1 or 2 in camera_config.py."
        )

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera opened: index={camera_index}, resolution={actual_width}x{actual_height}")
    return cap
