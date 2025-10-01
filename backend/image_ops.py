# activity/Back-end/image_ops.py
import io
import json
import numpy as np
import cv2
from skimage.filters import threshold_local

# Utility conversions
def load_image_bytes(image_bytes: bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError("Unable to decode image bytes")
    # If grayscale (2d), make BGR
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # If 4 channels (with alpha), drop alpha to keep 3 channels
    if img.shape[2] == 4:
        b, g, r, a = cv2.split(img)
        img = cv2.merge([b, g, r])
    return img


def image_to_bytes(img, fmt="png"):
    ext = ".png" if fmt.lower().startswith("p") else ".jpg"
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise ValueError("Failed encoding image")
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return buf.tobytes(), mime


# Basic ops
def to_grayscale(img, params):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def adjust_brightness(img, params):
    # params: {"value": -100..100}
    value = int(params.get("value", 0))
    return cv2.convertScaleAbs(img, alpha=1.0, beta=value)


def flip_image(img, params):
    mode = params.get("mode", "horizontal")
    if mode == "horizontal":
        return cv2.flip(img, 1)
    if mode == "vertical":
        return cv2.flip(img, 0)
    if mode == "both":
        return cv2.flip(img, -1)
    return img


def crop_image(img, params):
    # params: {"x":int,"y":int,"w":int,"h":int}
    h, w = img.shape[:2]
    x = int(params.get("x", 0))
    y = int(params.get("y", 0))
    cw = int(params.get("w", w - x))
    ch = int(params.get("h", h - y))
    x = max(0, min(x, w - 1))
    y = max(0, min(y, h - 1))
    cw = max(1, min(cw, w - x))
    ch = max(1, min(ch, h - y))
    return img[y : y + ch, x : x + cw]


# Blur / filter
def gaussian_blur(img, params):
    k = int(params.get("ksize", 5))
    if k % 2 == 0:
        k += 1
    return cv2.GaussianBlur(img, (k, k), 0)


def median_blur(img, params):
    k = int(params.get("ksize", 5))
    if k % 2 == 0:
        k += 1
    return cv2.medianBlur(img, k)


def bilateral_filter(img, params):
    d = int(params.get("d", 9))
    sigmaColor = int(params.get("sigmaColor", 75))
    sigmaSpace = int(params.get("sigmaSpace", 75))
    return cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)


def box_blur(img, params):
    k = int(params.get("ksize", 3))
    return cv2.blur(img, (k, k))


# Enhancement
def sharpen_image(img, params):
    # Simple unsharp / sharpening kernel
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)


def denoise_image(img, params):
    h = int(params.get("h", 10))
    return cv2.fastNlMeansDenoisingColored(img, None, h, h, 7, 21)


# Thresholding
def threshold_binary(img, params):
    thresh = int(params.get("thresh", 127))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)


def threshold_adaptive(img, params):
    block = int(params.get("block", 11))
    C = int(params.get("C", 2))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, block, C)
    return cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)


def threshold_otsu(img, params):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)


def threshold_local_skimage(img, params):
    block = int(params.get("block", 35))
    offset = float(params.get("offset", 10.0))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    local_thresh = threshold_local(gray, block_size=block, offset=offset)
    binary_local = (gray > local_thresh).astype("uint8") * 255
    return cv2.cvtColor(binary_local, cv2.COLOR_GRAY2BGR)


# Morphology
def morphology_erosion(img, params):
    k = int(params.get("ksize", 3))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
    return cv2.erode(img, kernel, iterations=1)


def morphology_dilation(img, params):
    k = int(params.get("ksize", 3))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
    return cv2.dilate(img, kernel, iterations=1)


def morphology_opening(img, params):
    k = int(params.get("ksize", 3))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


def morphology_closing(img, params):
    k = int(params.get("ksize", 3))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


# Edge detection
def canny_edge_detection(img, params):
    th1 = int(params.get("th1", 100))
    th2 = int(params.get("th2", 200))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, th1, th2)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def auto_canny(img, params):
    sigma = float(params.get("sigma", 0.33))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    v = np.median(gray)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(gray, lower, upper)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


# Dispatcher
_OPS = {
    "grayscale": (to_grayscale, {"desc": "Convert to grayscale", "params": {}}),
    "brightness": (adjust_brightness, {"desc": "Adjust brightness -100..100", "params": {"value": {"min": -100, "max": 100, "default": 0}}}),
    "flip": (flip_image, {"desc": "Flip image", "params": {"mode": {"options": ["horizontal", "vertical", "both"], "default": "horizontal"}}}),
    "crop": (crop_image, {"desc": "Crop image", "params": {"x": {}, "y": {}, "w": {}, "h": {}}}),
    "gaussian_blur": (gaussian_blur, {"desc": "Gaussian blur", "params": {"ksize": {"min": 1, "max": 61, "default": 5}}}),
    "median_blur": (median_blur, {"desc": "Median blur", "params": {"ksize": {"min": 1, "max": 61, "default": 5}}}),
    "bilateral": (bilateral_filter, {"desc": "Bilateral filter", "params": {"d": {"default": 9}}}),
    "box_blur": (box_blur, {"desc": "Box blur", "params": {"ksize": {"default": 3}}}),
    "sharpen": (sharpen_image, {"desc": "Sharpen", "params": {}}),
    "denoise": (denoise_image, {"desc": "Denoise (Non-local means)", "params": {"h": {"default": 10}}}),
    "threshold_binary": (threshold_binary, {"desc": "Binary threshold", "params": {"thresh": {"min": 0, "max": 255, "default": 127}}}),
    "threshold_adaptive": (threshold_adaptive, {"desc": "Adaptive threshold", "params": {"block": {"default": 11}, "C": {"default": 2}}}),
    "threshold_otsu": (threshold_otsu, {"desc": "Otsu threshold", "params": {}}),
    "threshold_local_skimage": (threshold_local_skimage, {"desc": "Local (skimage) threshold", "params": {"block": {"default": 35}, "offset": {"default": 10}}}),
    "erode": (morphology_erosion, {"desc": "Erosion", "params": {"ksize": {"default": 3}}}),
    "dilate": (morphology_dilation, {"desc": "Dilation", "params": {"ksize": {"default": 3}}}),
    "opening": (morphology_opening, {"desc": "Opening", "params": {"ksize": {"default": 3}}}),
    "closing": (morphology_closing, {"desc": "Closing", "params": {"ksize": {"default": 3}}}),
    "canny": (canny_edge_detection, {"desc": "Canny edges", "params": {"th1": {"default": 100}, "th2": {"default": 200}}}),
    "auto_canny": (auto_canny, {"desc": "Auto Canny", "params": {"sigma": {"default": 0.33}}}),
}


def get_operations():
    out = {}
    for k, (fn, meta) in _OPS.items():
        out[k] = meta
    return out


def process_image(image_bytes: bytes, operation: str, params: dict):
    """
    Main entry point:
    - returns (bytes, mime)
    """
    if operation not in _OPS:
        raise ValueError(f"Unknown operation '{operation}'")
    img = load_image_bytes(image_bytes)
    fn, _meta = _OPS[operation]
    out_img = fn(img, params or {})
    return image_to_bytes(out_img, fmt="png")
