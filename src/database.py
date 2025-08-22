import cv2
import base64
import datetime
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
import logging
import numpy as np

logger = logging.getLogger(__name__)

def create_collection_if_not_exist(db, collection_name: str) -> None:
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        logger.info(f"[MongoDB] Created collection '{collection_name}' in DB '{db.name}'")
    else:
        logger.info(f"[MongoDB] Collection '{collection_name}' already exists")

def save_to_mongo(track_id: int, vehicle_img: np.ndarray, plate_text: str, vehicle_type: str, vehicle_conf: float, ocr_conf: float) -> None:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    _, buffer = cv2.imencode('.jpg', vehicle_img)
    img_base64 = base64.b64encode(buffer.tobytes()).decode('utf-8')

    filter_query = {"track_id": track_id, "vehicle_type": vehicle_type}
    update_data = {
        "$set": {
            "plate": plate_text,
            "vehicle_type": vehicle_type,
            "vehicle_confidence": vehicle_conf,
            "ocr_confidence": ocr_conf,
            "image_base64": img_base64,
            "timestamp": datetime.datetime.now()
        }
    }

    result = collection.update_one(filter_query, update_data, upsert=True)
    if result.matched_count > 0:
        logger.info(f"[MongoDB] Updated record for track_id {track_id} with plate {plate_text}")
    else:
        logger.info(f"[MongoDB] Inserted new record for track_id {track_id} with plate {plate_text}")