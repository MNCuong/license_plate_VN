import cv2
import numpy as np
from ultralytics import YOLO
from config import MODEL_VEHICLE_PATH, VEHICLE_CLASSES, vehicle_plates, track_classes
from ocr import detect_plate_from_vehicle
from database import save_to_mongo
from utils import draw_label, in_rectangle
import logging

logger = logging.getLogger(__name__)

model_vehicle = YOLO(MODEL_VEHICLE_PATH)  # Có thể thêm .to('cuda') nếu dùng GPU
vehicle_class_ids = [k for k, v in model_vehicle.names.items() if v in VEHICLE_CLASSES]

def detect_vehicles(frame: np.ndarray) -> list:
    return model_vehicle.track(
        source=frame,
        conf=0.6,
        iou=0.6,
        device='cpu',
        persist=True,
        verbose=False
    )

def is_person_on_motorcycle(person_box: tuple, motorcycle_box: tuple, iou_thresh: float = 0.5) -> bool:
    x1 = max(person_box[0], motorcycle_box[0])
    y1 = max(person_box[1], motorcycle_box[1])
    x2 = min(person_box[2], motorcycle_box[2])
    y2 = min(person_box[3], motorcycle_box[3])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    person_area = (person_box[2] - person_box[0]) * (person_box[3] - person_box[1])
    motorcycle_area = (motorcycle_box[2] - motorcycle_box[0]) * (motorcycle_box[3] - motorcycle_box[1])
    union_area = person_area + motorcycle_area - inter_area
    if union_area == 0:
        return False
    iou = inter_area / union_area
    return iou > iou_thresh

def process_vehicle(frame: np.ndarray, frame_clone: np.ndarray, box: object, track_id: int) -> tuple[np.ndarray, dict]:
    cls_id = int(box.cls[0])
    vehicle_type = model_vehicle.names[cls_id]

    if track_id in track_classes:
        prev_type = track_classes[track_id]
        if prev_type == "motorcycle" and vehicle_type == "person":
            return frame, None
        if prev_type == "person" and vehicle_type == "motorcycle":
            vehicle_type = "person"
    track_classes[track_id] = vehicle_type

    if cls_id not in vehicle_class_ids:
        return frame, None

    vx1, vy1, vx2, vy2 = box.xyxy[0].cpu().numpy().astype(int)
    vehicle_crop = frame[vy1:vy2, vx1:vx2]
    vehicle_crop_clone = frame_clone[vy1:vy2, vx1:vx2]
    conf_vehicle = float(box.conf[0].cpu().numpy())

    plate_text_final = vehicle_plates.get(track_id)
    plate_ocr_conf = 0.0

    result = None
    if plate_text_final is None and vehicle_crop.size > 0:
        plate_text_detected, plate_ocr_conf = detect_plate_from_vehicle(track_id, vehicle_crop, vehicle_type)
        if plate_text_detected:
            plate_text_final = plate_text_detected
            vehicle_plates[track_id] = plate_text_final
            result = {
                "track_id": track_id,
                "vehicle_img": vehicle_crop_clone,
                "plate_text": plate_text_final,
                "vehicle_type": vehicle_type,
                "vehicle_conf": conf_vehicle,
                "ocr_conf": plate_ocr_conf
            }
        else:
            vehicle_plates[track_id] = None
            result = {
                "track_id": track_id,
                "vehicle_img": vehicle_crop_clone,
                "plate_text": "None6",
                "vehicle_type": vehicle_type,
                "vehicle_conf": conf_vehicle,
                "ocr_conf": plate_ocr_conf
            }

    draw_label(frame, (vx1, vy1, vx2, vy2), plate_text_final, (track_id, conf_vehicle))
    return frame, result