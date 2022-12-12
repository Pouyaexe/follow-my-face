import cv2
import numpy as np

# Create a cascade classifier object
face_cascade: cv2.CascadeClassifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Open the default camera
cap: cv2.VideoCapture = cv2.VideoCapture(0)

# Loop until the user hits the 'Esc' key
while True:
    # Read the next frame from the camera
    ret, frame: np.ndarray = cap.read()

    # Convert the frame to grayscale
    gray: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces: np.ndarray = face_cascade.detectMultiScale(gray)

    # Draw a rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Show the frame
    cv2.imshow("Face Detection", frame)

    # Check if the user hit the 'Esc' key
    c: int = cv2.waitKey(1)
    if c == 27:
        break

# Release the camera
cap.release()
