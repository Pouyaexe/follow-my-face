import cv2
import mediapipe as mp
import math

# Create a cascade classifier object
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Create a MediaPipe hand detector
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# Create a MediaPipe drawing helper
mpDraw = mp.solutions.drawing_utils

# Open the default camera
cap = cv2.VideoCapture(0)

# Loop until the user hits the 'Esc' key
while True:
    # Read the next frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray)

    # Draw a rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Detect hands in the frame
    hands_frame = hands.process(frame)

    # Check if the person is showing the "L" sign
    if hands_frame.multi_hand_landmarks:
        for hand_landmarks in hands_frame.multi_hand_landmarks:
            # Get the positions of the index and thumb fingers
            index_finger_pos = hand_landmarks.landmark(mpHands.INDEX_FINGER_TIP)
            thumb_finger_pos = hand_landmarks.landmark(mpHands.THUMB_TIP)

            # Calculate the angle between the index and thumb fingers
            dx = index_finger_pos.x - thumb_finger_pos.x
            dy = index_finger_pos.y - thumb_finger_pos.y
            angle = math.atan2(dy, dx)

            # Check if the angle is approximately "L" shaped
            if angle > 0.5 and angle < 1.5:
                # Draw a circle around the hand to indicate that the "L" sign was detected
                mpDraw.draw_circle(frame, (int(index_finger_pos.x), int(index_finger_pos.y)), radius=10, color=(0, 255, 0), thickness=-1)
                print("L sign detected")
    # Draw the detected hands and landmarks on the frame
    if hands_frame.multi_hand_landmarks:
        for hand_landmarks in hands_frame.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

    # Show the frame
    cv2.imshow("Hand and Face Detection", frame)

    # Check if the user hit the 'Esc' key
    c = cv2.waitKey(1)
    if c == 27:
        break

# Release the camera
cap.release()
