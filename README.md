###Vietnamese Vehicle License Plate Recognition (ALPR/ANPR) System
Overview
The Vietnamese Vehicle License Plate Recognition (ALPR/ANPR) System is a robust Python-based solution designed to detect vehicles, extract license plates, and perform Optical Character Recognition (OCR) to read Vietnamese license plate numbers from video streams or images. Built with scalability and real-world applications in mind, this system is ideal for:

Parking Management: Automate vehicle entry/exit tracking.
Traffic Monitoring: Monitor and analyze traffic flow in real time.
Security Systems: Enhance surveillance with automated license plate recognition.

This project leverages state-of-the-art computer vision techniques, including YOLO models for detection and OCR, and integrates with MongoDB for efficient data storage.

Features

Vehicle Detection: Accurately identifies vehicles (cars, motorcycles, trucks, buses) in images and video streams.
License Plate Extraction: Detects and isolates license plates from identified vehicles.
OCR Processing: Reads Vietnamese license plate numbers with high accuracy.
Real-Time Video Processing: Processes video streams frame by frame for seamless operation.
Configurable Settings: Easily modify model paths, detection thresholds, and video sources.
Comprehensive Logging: Logs all operations, errors, and results for debugging and monitoring.
MongoDB Integration: Stores recognized license plates and timestamps in a MongoDB database.
Scalable Architecture: Designed for easy integration into larger systems.

Installation
Follow these steps to set up the project locally:

1. Clone the Repository
   git clone https://github.com/MNCuong/license_plate.git
   cd vehicle_lpr

2. Set Up a Virtual Environment
   Create and activate a Python virtual environment to manage dependencies:

# Create virtual environment

python -m venv venv

# Activate virtual environment

# On Linux/macOS

source venv/bin/activate

# On Windows

venv\Scripts\activate

3. Install Dependencies
   Install the required Python packages listed in requirements.txt:
   pip install -r requirements.txt

Note: Ensure you have Python 3.8+ installed. For GPU support, install the appropriate versions of PyTorch and CUDA.

Usage
To start the ALPR system, run the main script:
python main.py

Configuration Steps

Update the config.py file with the correct paths for:
Video source (e.g., camera feed or video file).
YOLO model paths for vehicle detection, license plate recognition, and OCR.
MongoDB connection settings.

Monitor logs in the logs/ directory for system activity and debugging.
Recognized license plates and timestamps are automatically stored in the configured MongoDB database.

Configuration
The config.py file centralizes all system settings for easy customization. Below is an example configuration:
from ultralytics import YOLO

# Model paths for YOLO and OCR

MODEL_VEHICLE_PATH = "../models/best.pt" # YOLO model for vehicle detection
MODEL_LPR_PATH = "../models/yolov8sLPR.pt" # YOLO model for license plate recognition
MODEL_OCR_PATH = "../models/ocr.pt" # OCR model for reading plate numbers

# Supported vehicle classes

VEHICLE_CLASSES = ["car", "motorcycle", "truck", "person", "bus"]

# MongoDB connection settings

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'vehicle_db'
COLLECTION_NAME = 'vehicle_plates'

# Global variables for tracking

vehicle_plates = {} # Temporary storage of recognized plates
logged_track_ids = set() # Track IDs already logged
track_classes = {} # Class of each track ID

Key Configuration Notes

Model Paths: Ensure the paths to the YOLO and OCR models are correct and accessible.
MongoDB URI: Update the MONGO_URI to match your MongoDB instance.
Vehicle Classes: Modify VEHICLE_CLASSES to include or exclude specific vehicle types as needed.

Database Integration
The system uses MongoDB to store recognized license plates and their associated timestamps. The database.py module handles all database interactions.
Default MongoDB Configuration
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vehicle_db'
MONGO_COLLECTION = 'vehicle_plates'

Customization

Update the MongoDB settings in config.py to point to your database instance.
Ensure MongoDB is running locally or on a remote server before starting the application.

Logging
All system activities, including detections, errors, and results, are logged in the logs/ directory. This ensures easy monitoring and debugging of the system.

Log Location: logs/
Log Format: Includes timestamps, operation details, and error messages for traceability.

Project Structure
VEHICLE_LPR/
├── img/ # Directory for images (e.g., input or sample images)
├── models/ # Directory for YOLO and OCR model files
├── output/ # Directory for processed output files
├── plate/ # Directory for license plate-related data or images
├── src/ # Source code directory
│ ├── **pycache**/ # Python bytecode cache
│ ├── logs/ # Log files directory
│ ├── **init**.py # Initialization file for the package
│ ├── config.py # Configuration settings
│ ├── database.py # MongoDB integration
│ ├── main.py # Main script to run the ALPR system
│ ├── ocr.py # OCR processing logic
│ ├── utils.py # Utility functions
│ ├── vehicle_detection.py # Vehicle detection logic
│ └── video_processor.py # Video processing logic
├── templates/ # Directory for HTML templates (e.g., web interface)
│ └── index.html # Main HTML template
├── video/ # Directory for video files
├── app.py # Flask or web application entry point (if applicable)
├── README.md # Project documentation
└── requirements.txt # List of Python dependencies

Contribution
We welcome contributions to enhance the system! To contribute:

Fork the Repository: Create your own copy of the project.
Make Changes: Implement your improvements or bug fixes.
Submit a Pull Request: Share your changes for review.
Open an Issue: For major changes or feature requests, please open an issue to discuss first.

License
This project is licensed under the MNC License.© 2025 MNC Việt Nam. All rights reserved.

Contact
For questions, feedback, or support, please contact the project maintainers at cuong.mai@vconnex.vn.
