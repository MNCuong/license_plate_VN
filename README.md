

````markdown
# Vietnamese Vehicle License Plate Recognition (ALPR/ANPR) System

## 📌 Overview
The **Vietnamese Vehicle License Plate Recognition (ALPR/ANPR) System** is a robust Python-based solution designed to:

- 🚗 Detect vehicles in images & video streams  
- 🔍 Extract license plates from vehicles  
- 🔠 Perform OCR to read Vietnamese license plate numbers  
- 📊 Store results in MongoDB for efficient data management  

This system is suitable for:

- **Parking Management**: Automate vehicle entry/exit tracking  
- **Traffic Monitoring**: Analyze traffic flow in real-time  
- **Security Systems**: Enhance surveillance with automated license plate recognition  

It leverages **YOLO models** for detection + OCR and is designed with scalability in mind.

---

## ✨ Features
- ✅ **Vehicle Detection** (cars, motorcycles, trucks, buses, etc.)  
- ✅ **License Plate Extraction**  
- ✅ **OCR Processing** (Vietnamese license plates)  
- ✅ **Real-Time Video Processing**  
- ✅ **Configurable Settings** (models, thresholds, sources)  
- ✅ **Comprehensive Logging**  
- ✅ **MongoDB Integration** (store plates + timestamps)  
- ✅ **Scalable Architecture** (easy system integration)  

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/MNCuong/license_plate.git
cd VEHICLE_LPR
````

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: Requires Python **3.8+**.
> For GPU support, install the correct **PyTorch + CUDA** versions.

---

## 🚀 Usage

Run the main script:

```bash
python src/main.py
```

### Configuration Steps

Update `src/config.py` with:

* Video source (camera feed / video file)
* YOLO model paths (vehicle detection, license plate, OCR)
* MongoDB connection settings

Logs are stored in `src/logs/` and recognized plates are saved in MongoDB.

---

## 🔧 Configuration Example (`src/config.py`)

```python
from ultralytics import YOLO

# Model paths
MODEL_VEHICLE_PATH = "../models/best.pt"
MODEL_LPR_PATH = "../models/yolov8sLPR.pt"
MODEL_OCR_PATH = "../models/ocr.pt"

# Supported vehicle classes
VEHICLE_CLASSES = ["car", "motorcycle", "truck", "person", "bus"]

# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'vehicle_db'
COLLECTION_NAME = 'vehicle_plates'

# Runtime globals
vehicle_plates = {}
logged_track_ids = set()
track_classes = {}
```

---

## 🗄️ Database Integration

* Default MongoDB config:

```python
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vehicle_db'
MONGO_COLLECTION = 'vehicle_plates'
```

* Update in `config.py` as needed
* Ensure MongoDB is running locally or remotely

---

## 📑 Logging

* Logs stored in: `src/logs/`
* Format includes: timestamps, details, error messages

---

## 📂 Project Structure

```plaintext
VEHICLE_LPR/
├── img/                 # Sample images
├── models/              # YOLO & OCR model files
├── output/              # Processed outputs
├── plate/               # License plate-related data
├── src/                 # Source code
│   ├── __pycache__/     
│   ├── logs/            # Log files
│   ├── __init__.py      
│   ├── config.py        # Settings
│   ├── database.py      # MongoDB integration
│   ├── main.py          # Main ALPR script
│   ├── ocr.py           # OCR logic
│   ├── utils.py         # Utilities
│   ├── vehicle_detection.py  # Vehicle detection logic
│   └── video_processor.py    # Video processing logic
├── templates/           # Web UI templates
│   └── index.html       
├── video/               # Video samples
├── app.py               # Flask app (if enabled)
├── README.md            # Documentation
└── requirements.txt     # Python dependencies
```

---

## 🤝 Contribution

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Submit a Pull Request

For major changes, open an Issue first to discuss.

---

## 📜 License

Licensed under the **MNC License**.
© 2025 MNC Việt Nam. All rights reserved.

---

## 📬 Contact

For support or feedback: **[cuong.mai@vconnex.vn](mailto:cuong.mai@vconnex.vn)**

```

