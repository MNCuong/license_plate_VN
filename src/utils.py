import re
import cv2
import numpy as np
from paddleocr import PaddleOCR
import logging
logger = logging.getLogger(__name__)
def in_rectangle(px1, py1, px2, py2, frame_width, frame_height, margin=30):
    x_min, y_min = margin, margin
    x_max, y_max = frame_width - margin, frame_height - margin
    return (px1 >= x_min and py1 >= y_min and
            px2 <= x_max and py2 <= y_max)

def is_valid_plate(plate: str, vehicle_type: str = "car") -> bool:
    plate = plate.upper().strip()
    patterns = {
        "car": [
            r'^\d{2}[A-Z0-9]{1,2}\d{4,5}$',
            r'^\d{2}C\d{5}$',
            r'^\d{2}[AB]\d{5}$',
            r'^[A-Z]{2}\d{4,5}$',
            r'^80NG\d{3}\d{2}$',
            r'^80NN\d{3}\d{2}$',
            r'^80QT\d{3}\d{2}$',
            r'^80LD\d{3}\d{2}$',
            r'^80CD\d{3}\d{2}$',
        ],
        "motorcycle": [
            r'^\d{2}[A-Z]{1,2}\d?-?\d{4,5}$'
        ],
        "bus": [
            r'^\d{2}[A-Z0-9]{1,2}\d{4,5}$',
            r'^\d{2}C\d{5}$',
            r'^\d{2}[AB]\d{5}$',
        ],
        "truck": [
            r'^\d{2}[A-Z0-9]{1,2}\d{4,5}$',
            r'^\d{2}C\d{5}$',
            r'^\d{2}[AB]\d{5}$',
        ]
    }

    selected_patterns = patterns.get(vehicle_type.lower(), [])
    if not selected_patterns:
        return False
    return any(re.match(pattern, plate) for pattern in selected_patterns)

def draw_label(frame, box, label, score, vehicle_type="car"):
    vx1, vy1, vx2, vy2 = box
    cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (0, 255, 0), 2)
    text = f" {label} | conf: {score[1]:.2f}"
    font_scale = 0.6
    thickness = 1
    (tw, th), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    cv2.rectangle(frame, (vx1, vy1 - th - baseline - 5), (vx1 + tw, vy1), (0, 255, 0), -1)
    cv2.putText(frame, text, (vx1, vy1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 1, lineType=cv2.LINE_AA)

def count_digits_after_last_letter(text):
    if not text:
        return 0
    match = re.search(r'[A-Za-z](?!.*[A-Za-z])', text)
    if match:
        pos = match.end()
        digits = re.findall(r'\d', text[pos:])
        return len(digits)
    return 0

ocr_det = PaddleOCR(use_angle_cls=False, lang='en')
def align_plate_with_paddle(plate_crop, output_size=(240, 80)):
    results = ocr_det.ocr(plate_crop)
    logger.debug(f"Aligning plate with PaddleOCR, results: {results}")

    if not results or not results[0]:
        logger.info("Không tìm thấy text box nào")
        return plate_crop  

    try:
        # Lấy box đầu tiên
        box = np.array(results[0][0][0], dtype=np.float32)
    except Exception as e:
        logger.error(f"Lỗi khi lấy box từ PaddleOCR: {e}")
        return plate_crop

    dst = np.array([
        [0, 0],
        [output_size[0] - 1, 0],
        [output_size[0] - 1, output_size[1] - 1],
        [0, output_size[1] - 1]
    ], dtype=np.float32)

    M = cv2.getPerspectiveTransform(box, dst)
    aligned = cv2.warpPerspective(plate_crop, M, output_size)
    return aligned
