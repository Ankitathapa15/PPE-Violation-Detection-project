import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ------------------------------
# CONFIG
# ------------------------------
MODEL_PATH = "yoloweights/best.pt"
SNAPSHOT_DIR = "snapshots"

EMAIL_SENDER = "ankita.thapa1519@gmail.com"
EMAIL_PASSWORD = ""   # Gmail App password
EMAIL_RECEIVER = ""

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Load model
model = YOLO(MODEL_PATH)
print("Model Classes:", model.names)

# PPE class names
REQUIRED_PPE = {
    "Gloves",
    "Hard_hat",
    "Mask",
    "Safety_boots",
    "Vest"
}

# ------------------------------
# EMAIL SENDING
# ------------------------------
def send_email_alert(image_path, missing_items, frame_number):
    try:
        subject = f"PPE Violation Detected - Frame {frame_number}"
        body = f"The following PPE items were missing: {', '.join(missing_items)}"

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Attach snapshot
        with open(image_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
        msg.attach(part)

        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print("Email sending failed:", e)


# ------------------------------
# CHECK MISSING PPE
# ------------------------------
def check_violation(result):
    detected = set(model.names[int(box.cls)] for box in result.boxes)
    missing = REQUIRED_PPE - detected
    return len(missing) > 0, missing


# ------------------------------
# STREAMLIT UI
# ------------------------------
st.title("🦺 PPE Violation Detection System")
uploaded_video = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

if uploaded_video:
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())

    st.video(video_path)

    if st.button("Start Detection"):
        cap = cv2.VideoCapture(video_path)
        frame_placeholder = st.empty()

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            results = model(frame)[0]

            # Check violation
            violation, missing = check_violation(results)

            if violation:
                st.warning(f"Violation at frame {frame_count} - Missing: {', '.join(missing)}")

                snapshot_path = f"{SNAPSHOT_DIR}/violation_{frame_count}.jpg"

                # RGBA → RGB fix
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                img.save(snapshot_path)

                # Send email alert
                send_email_alert(snapshot_path, missing, frame_count)

            # Show output frame
            annotated = results.plot()
            frame_placeholder.image(annotated, channels="BGR")

        cap.release()
        st.success("Detection complete!")
