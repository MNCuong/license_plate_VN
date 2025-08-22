import cv2
import time
import queue
import concurrent.futures
from vehicle_detection import detect_vehicles, process_vehicle, is_person_on_motorcycle, model_vehicle
from database import save_to_mongo
from utils import in_rectangle
from ocr import ocr_license_plate
import numpy as np
from config import track_classes
import logging

logger = logging.getLogger(__name__)

ocr_queue = queue.Queue()

def ocr_task(track_id: int, plate_crop: np.ndarray, vehicle_type: str) -> tuple[int, str, float]:
    plate_crop_sharp = cv2.resize(plate_crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    plate_text, conf = ocr_license_plate(track_id, plate_crop_sharp, vehicle_type)
    if plate_text:
        logger.info(f"[Background OCR] Track {track_id}: {plate_text} (conf={conf:.2f})")
    return track_id, plate_text, conf

def process_video(video_path: str, output_path: str) -> None:
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error("Không thể mở video/camera!")
            return

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = min(cap.get(cv2.CAP_PROP_FPS), 25)
        out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'XVID'),
            fps,
            (frame_width, frame_height)
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_clone = frame.copy()
                start_vehicle = time.time()
                vehicle_results = detect_vehicles(frame)
                h, w, _ = frame.shape

                if vehicle_results:
                    boxes = vehicle_results[0].boxes
                    ids = boxes.id.cpu().numpy().astype(int) if boxes.id is not None else []

                    motorcycles = []
                    persons = []
                    for i, box in enumerate(boxes):
                        cls_id = int(box.cls[0])
                        if model_vehicle.names[cls_id] == "motorcycle":
                            motorcycles.append((i, box))
                        elif model_vehicle.names[cls_id] == "person":
                            persons.append((i, box))

                    ignore_person_idx = set()
                    for pid, pbox in persons:
                        px1, py1, px2, py2 = pbox.xyxy[0].cpu().numpy().astype(int)
                        for mid, mbox in motorcycles:
                            mx1, my1, mx2, my2 = mbox.xyxy[0].cpu().numpy().astype(int)
                            if is_person_on_motorcycle((px1, py1, px2, py2), (mx1, my1, mx2, my2)):
                                ignore_person_idx.add(pid)

                    futures = []
                    results = []

                    for i, box in enumerate(boxes):
                        if i in ignore_person_idx:
                            continue 

                        track_id = int(ids[i]) if i < len(ids) else -1
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        if not in_rectangle(x1, y1, x2, y2, w, h, margin=10):
                            continue

                        frame, result = process_vehicle(frame, frame_clone, box, track_id)
                        if result:
                            results.append(result)
                            if result["plate_text"] is None:
                                futures.append(
                                    executor.submit(
                                        ocr_task,
                                        track_id,
                                        result["vehicle_img"],
                                        result["vehicle_type"], 
                                    )
                                )

                    for result in results:
                        save_to_mongo(
                            result["track_id"],
                            result["vehicle_img"],
                            result["plate_text"],
                            result["vehicle_type"],
                            result["vehicle_conf"],
                            result["ocr_conf"],
                        )

                    for future in concurrent.futures.as_completed(futures):
                        track_id, plate_text, conf = future.result()
                        if plate_text and plate_text != "N/A":
                            save_to_mongo(
                                track_id,
                                frame_clone,
                                plate_text,
                                track_classes.get(track_id, "unknown"),
                                0.0,
                                conf,
                            )

                end_vehicle = time.time()
                logger.info(f"[Vehicle Detection] Thời gian phát hiện xe: {end_vehicle - start_vehicle:.2f} giây")
                out.write(frame)

        cap.release()
        out.release()
    except Exception as e:
        logger.error(f"Lỗi khi xử lý video: {str(e)}")
        raise
