# PPE Violation Detection

## 📌 Overview
Short explanation of the project.

## 🎯 Key Features
- PPE violation detection
- YOLO-based object detection
- Video analysis
- Email alerts
- Streamlit interface
- Docker deployment

## 🛠️ Tech Stack
Python | YOLO | OpenCV | Streamlit | Docker

## 📂 Project Structure

```text
PPE-Violation-Detection/
│
├── 📄 app.py                    # Main Streamlit application
├── 📄 train.py                  # YOLO model training script
├── 📄 requirements.txt          # Python dependencies
├── 📄 dockerfile                # Docker configuration
├── 📄 yolo11n.pt                # YOLO base model
├── 📄 violation_output.jpg      # Sample detection output
│
├── 📁 Images/                   # Project screenshots
│   ├── 🖼️ Email Alert.png
│   ├── 🖼️ Project UI 1.png
│   ├── 🖼️ Project UI 2.png
│   ├── 🖼️ Project UI 3.png
│   └── 🖼️ Project on Docker.png
│
└── 📄 README.md                 # Project documentation
```

## 🖥️ Project Screenshots

### Application Interface
![Project UI 1](Images/Project%20UI%201.png)

### Detection Results
![Project UI 2](Images/Project%20UI%202.png)

![Project UI 3](Images/Project%20UI%203.png)

### Email Alert System
![Email Alert](Images/Email%20Alert.png)

### Docker Deployment
![Docker](Images/Project%20on%20Docker.png)

## ⚙️ How It Works
1. Input image/video
2. Frames are processed using OpenCV
3. YOLO detects PPE-related objects
4. Violations are identified
5. Results are displayed
6. Email alerts are generated when required

