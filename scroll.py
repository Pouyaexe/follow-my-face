import cv2
import mediapipe as mp
from utils import zoom_in, text_overlay
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Load the Haar cascade classifier for face detection.
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Global zoom factor. if the zoom factor goes higher than 1, the image will zoom in on the detected face.
zoom_factor = 1

def 

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Detect faces in the webcam feed.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw a rectangle around each detected face. The color is BGR. so for a white rectangle, we use (255, 255, 255).
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:


                # Write the hand detcted text on the down right corner of the screen.
                image = text_overlay(
                    image,
                    "Hand detected",
                    image_width - 200,
                    image_height - 30,
                    (0, 255, 0),
                    1,
                )

                # Draw the hand landmarks and connections on the image.
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )
        # if the zoom factor is greater than 1, then we are zoomed in on the face.
        if zoom_factor > 1:
            # Draw the zoomed in face on the screen.
            image = zoom_in(image, x, y, w, h, zoom_factor)

        # Flip the image horizontally for a selfie horizontally for a selfie-view display. 
        cv2.namedWindow("MediaPipe Hands", cv2.WINDOW_KEEPRATIO)

        cv2.imshow("MediaPipe Hands", cv2.flip(image, 1) )
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
