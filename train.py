from ultralytics import YOLO

# Choose your model — YOLO11n is best for small systems
model = YOLO("yolo11n.pt")

# Train model
model.train(
    data=r"C:\Users\ankit\Desktop\ppe_violation_project\yoloweights\PPE DETECTION.v1i.yolov11\data.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    device="cpu"  # use "0" for GPU if available
)
