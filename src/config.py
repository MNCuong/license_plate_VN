from ultralytics import YOLO

# Model paths
MODEL_VEHICLE_PATH = "../models/best.pt"
MODEL_LPR_PATH = "../models/yolov8sLPR.pt"
MODEL_OCR_PATH = "../models/ocr.pt"

# Vehicle classes
VEHICLE_CLASSES = ["car", "motorcycle", "truck", "person", "bus"]

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'vehicle_db'
COLLECTION_NAME = 'vehicle_plates'

# Global variables
vehicle_plates = {}
logged_track_ids = set()
track_classes = {}