 Vietnamese Vehicle License Plate Recognition (ALPR/ANPR) System

 **Overview**

This project is a **Vietnamese Vehicle License Plate Recognition (ALPR/ANPR) system** built in Python.
It detects vehicles from video streams, extracts license plates, and performs OCR (Optical Character Recognition) to read license plate numbers.

Applications include:

- Parking management
- Traffic monitoring
- Security systems


 **Features**

- **Vehicle Detection:** Detects vehicles in images and video streams.
- **License Plate Recognition:** Extracts license plates from detected vehicles.
- **OCR:** Reads Vietnamese license plates accurately.
- **Video Processing:** Processes video streams frame by frame.
- **Configurable:** Easily change model paths, thresholds, and video sources.
- **Logging:** All operations are logged for debugging and analysis.
- **MongoDB Storage:** Recognized plates and timestamps are automatically stored in MongoDB.


 **Installation**

1. **Clone the repository**

bash
```git clone https://github.com/MNCuong/license_plate.git```
```cd vehicle_lpr```


2. **Create a virtual environment**

bash
```python -m venv venv```
 Activate environment:
```source venv/bin/activate ```   Linux/macOS
```venv\Scripts\activate   ```    Windows


3. **Install required packages**

bash
pip install -r requirements.txt


 **Usage**

Run the main script to start the system:

bash
python main.py


- Ensure `config.py` has the correct video source, model paths, and MongoDB configuration.
- Logs are saved in the `logs/` directory for monitoring.
- Recognized plates are stored automatically in MongoDB.


 **Configuration**

`config.py` contains all key settings:

python
from ultralytics import YOLO

//Model paths
MODEL_VEHICLE_PATH = "../models/best.pt"        YOLO model for vehicle detection
MODEL_LPR_PATH = "../models/yolov8sLPR.pt"     YOLO model for license plate recognition
MODEL_OCR_PATH = "../models/ocr.pt"            OCR model for reading plate numbers

//Vehicle classes
VEHICLE_CLASSES = ["car", "motorcycle", "truck", "person", "bus"]

//MongoDB settings
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'vehicle_db'
COLLECTION_NAME = 'vehicle_plates'

//Global variables
vehicle_plates = {}        Temporary storage of recognized plates
logged_track_ids = set()   Track IDs already logged
track_classes = {}         Class of each track ID


 **Database**

`database.py` handles storage of recognized plates and timestamps in **MongoDB** by default.
You can adjust `config.py` to point to your MongoDB instance.

Example default configuration:

python
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vehicle_db'
MONGO_COLLECTION = 'vehicle_plates'


 **Logging**

All system operations, errors, and results are logged under `logs/` for easy monitoring and debugging.

 **Contribution**

- Fork the project and submit pull requests.
- For major changes, please open an issue first to discuss.

 **License**
This project is licensed under the VCONNEX License.
© 2025 VCONNEX Việt Nam. All rights reserved.
