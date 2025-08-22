import cv2
import numpy as np
import re
from ultralytics import YOLO
from config import MODEL_LPR_PATH, MODEL_OCR_PATH
from utils import is_valid_plate, align_plate_with_paddle
import logging

logger = logging.getLogger(__name__)

model_lpr = YOLO(MODEL_LPR_PATH)  # Có thể thêm .to('cuda') nếu dùng GPU
model_ocr = YOLO(MODEL_OCR_PATH)  # Có thể thêm .to('cuda') nếu dùng GPU

def ocr_license_plate(track_id: int, plate_crop: np.ndarray, vehicle_type: str = "car") -> tuple[str, float]:
    plate_resized = cv2.resize(plate_crop, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    ocr_results = model_ocr.predict(source=plate_resized, conf=0.5, iou=0.7, device='cpu', verbose=False)
    chars, confs = [], []
    
    for ocr_res in ocr_results:
        for char_box in ocr_res.boxes:
            cx1, cy1, cx2, cy2 = char_box.xyxy[0].cpu().numpy().astype(int)
            conf_char = float(char_box.conf[0].cpu().numpy())
            if conf_char < 0.5:
                continue
            label_id = int(char_box.cls[0])
            label_name = ocr_res.names[label_id]
            cx = (cx1 + cx2) / 2
            cy = (cy1 + cy2) / 2
            h = cy2 - cy1
            chars.append((cx, cy, h, label_name))
            confs.append(conf_char)

    if not chars:
        return "None4", 0.0

    chars.sort(key=lambda x: (x[1], x[0]))
    lines, current_line = [], [chars[0]]
    for ch in chars[1:]:
        avg_h = np.mean([c[2] for c in current_line])
        if abs(ch[1] - current_line[-1][1]) < avg_h * 0.7:
            current_line.append(ch)
        else:
            lines.append(current_line)
            current_line = [ch]
    lines.append(current_line)
    for li in range(len(lines)):
        lines[li] = sorted(lines[li], key=lambda x: x[0])

    recognized_text = ""
    if vehicle_type in ["car", "bus", "truck"]:
        if len(lines) == 2:
            recognized_text = ''.join([c[3] for c in lines[0]]) + "-" + ''.join([c[3] for c in lines[1]])
        else:
            recognized_text = ''.join([c[3] for c in lines[0]])
    elif vehicle_type == "motorcycle":
        if len(lines) == 2:
            line1 = ''.join([c[3] for c in lines[0]])
            line2 = ''.join([c[3] for c in lines[1]])
            candidate = f"{line1}-{line2}"
            if 6 <= len(line1 + line2) <= 10:
                recognized_text = candidate
            else:
                recognized_text = line1 + line2 
        else:
            recognized_text = ''.join([c[3] for line in lines for c in line])

    else:
        recognized_text = ''.join([c[3] for line in lines for c in line])

    recognized_text = re.sub(r'[^A-Z0-9]', '', recognized_text)
    avg_conf = sum(confs) / len(confs) if confs else 0.0

    if (
        not recognized_text
        or not is_valid_plate(recognized_text, vehicle_type)
        or not (7 <= len(recognized_text.replace("-", "")) <= 10)
    ):
        recognized_text = "N/A"
        avg_conf = 0.0
    return recognized_text, avg_conf

def detect_plate_from_vehicle(track_id: int, vehicle_crop: np.ndarray, vehicle_type: str = "car") -> tuple[str, float]:
    lpr_results = model_lpr.predict(source=vehicle_crop, conf=0.6, iou=0.7, device='cpu', verbose=False)
    for pr in lpr_results:
        for pbox in pr.boxes:
            px1, py1, px2, py2 = pbox.xyxy[0].cpu().numpy().astype(int)
            w, h = px2 - px1, py2 - py1
            pad_w, pad_h = int(w * 0.1), int(h * 0.15)
            px1, py1 = max(px1 - pad_w, 0), max(py1 - pad_h, 0)
            px2, py2 = min(px2 + pad_w, vehicle_crop.shape[1]), min(py2 + pad_h, vehicle_crop.shape[0])
            plate_crop = vehicle_crop[py1:py2, px1:px2]
            plate_crop=align_plate_with_paddle(plate_crop, output_size=(240, 80))
            plate_text, ocr_conf = ocr_license_plate(track_id, plate_crop, vehicle_type)
            if plate_text:
                return plate_text, ocr_conf
    return "None1", 0.0