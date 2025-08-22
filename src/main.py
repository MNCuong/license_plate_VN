import logging
from pymongo import MongoClient
from video_processor import process_video
from database import create_collection_if_not_exist
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
import os
import logging
import sys

os.makedirs("logs", exist_ok=True)

sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout) 
    ]
)


logger = logging.getLogger(__name__)

def main():

    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        create_collection_if_not_exist(db, COLLECTION_NAME)
        
        video_path = "../video/261374963_3734554484420037573.mp4"
        output_path = "../output/out2.avi"
    
        logger.info("==============>>>>>Start LPR<<<<<===============")
        process_video(video_path, output_path)
        logger.info("==============>>>>>End LPR<<<<<===============")
        
    except Exception as e:
        logger.error(f"Lỗi trong chương trình chính: {str(e)}")
        raise
    finally:
        client.close()  

if __name__ == "__main__":
    main()