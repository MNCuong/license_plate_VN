````markdown
# Vietnamese Vehicle License Plate Recognition (ALPR/ANPR) System

## Overview

The Vietnamese Vehicle License Plate Recognition (ALPR/ANPR) System is a robust Python-based solution designed to:

- Detect vehicles in images and video streams.
- Extract license plates from detected vehicles.
- Perform OCR to read Vietnamese license plate numbers.
- Store results in MongoDB for efficient data management.

This system is ideal for:

- **Parking Management:** Automate vehicle entry and exit tracking.
- **Traffic Monitoring:** Analyze traffic flow in real-time.
- **Security Systems:** Enhance surveillance with automated license plate recognition.

It leverages YOLO models for detection and OCR, with a focus on scalability and performance.

---

## Features

- **Vehicle Detection:** Identifies vehicles (cars, motorcycles, trucks, buses, etc.).
- **License Plate Extraction:** Isolates license plates from detected vehicles.
- **OCR Processing:** Accurately reads Vietnamese license plates.
- **Real-Time Video Processing:** Processes video streams frame by frame.
- **Configurable Settings:** Allows customization of models, thresholds, and sources.
- **Comprehensive Logging:** Records operations, errors, and results.
- **MongoDB Integration:** Stores license plates and timestamps.
- **Scalable Architecture:** Designed for easy integration into larger systems.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MNCuong/license_plate.git
cd VEHICLE_LPR
```
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

> **Note:** Requires Python 3.8 or higher. For GPU support, install compatible versions of PyTorch and CUDA.

---

## Usage

Run the main script:

```bash
python src/main.py
```

---

## Configuration Steps

Update `src/config.py` with:

- Video source (e.g., camera feed or video file).
- YOLO model paths (vehicle detection, license plate, OCR).
- MongoDB connection settings.

Logs are saved in `src/logs/`. Recognized plates are automatically stored in MongoDB.

### Example Configuration (`src/config.py`)

```python
from ultralytics import YOLO

# Model paths
MODEL_VEHICLE_PATH = "../models/best.pt"        # Vehicle detection model
MODEL_LPR_PATH = "../models/yolov8sLPR.pt"      # License plate recognition model
MODEL_OCR_PATH = "../models/ocr.pt"             # OCR model

# Supported vehicle classes
VEHICLE_CLASSES = ["car", "motorcycle", "truck", "person", "bus"]

# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'vehicle_db'
COLLECTION_NAME = 'vehicle_plates'

# Runtime globals
vehicle_plates = {}         # Temporary storage for recognized plates
logged_track_ids = set()    # Track IDs already logged
track_classes = {}          # Class of each track ID
```

---

## Database Integration

### Default MongoDB Configuration

```python
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vehicle_db'
MONGO_COLLECTION = 'vehicle_plates'
```

Update settings in `src/config.py` as needed. Ensure MongoDB is running locally or on a remote server.

---

## Logging

Logs are stored in: `src/logs/`.

Includes timestamps, operation details, and error messages for debugging.

---

## Project Structure

```
VEHICLE_LPR/
├── img/                 # Sample images
├── models/              # YOLO and OCR model files
├── output/              # Processed output files
├── plate/               # License plate-related data
├── src/                 # Source code
│   ├── __pycache__/
│   ├── logs/            # Log files
│   ├── __init__.py
│   ├── config.py        # Configuration settings
│   ├── database.py      # MongoDB integration
│   ├── main.py          # Main ALPR script
│   ├── ocr.py           # OCR processing logic
│   ├── utils.py         # Utility functions
│   ├── vehicle_detection.py  # Vehicle detection logic
│   └── video_processor.py    # Video processing logic
├── templates/           # Web UI templates
│   └── index.html
├── video/               # Video samples
├── app.py               # Flask application (if enabled)
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

---

## Contribution

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a Pull Request.

> For major changes, please open an Issue to discuss first.

---

## License

Licensed under the **MNC License**.
© 2025 MNC Việt Nam. All rights reserved.

---

## Contact

For support or feedback: **[cuong.mai@vconnex.vn](mailto:cuong.mai@vconnex.vn)**

