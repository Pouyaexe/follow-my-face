import cv2
import mediapipe as mp
from utils import zoom_in, hand_zoom_factor, process_hands
from mouse import move_mouse, click_mouse
from face import detect_face

mp_hands = mp.solutions.hands

# Global zoom factor. if the zoom factor goes higher than 1, the image will zoom in on the detected face.
zoom_factor = 1


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
        faces = detect_face(image)

        # Draw a rectangle around each detected face. The color is BGR. so for a white rectangle, we use (255, 255, 255).
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Process the hands in the image.
        image, zoom_factor = process_hands(image, results, x, y, w, h, zoom_factor)
                        
        # if the zoom factor is greater than 1, then we are zoomed in on the face.
        if zoom_factor > 1:
            image = zoom_in(image, x, y, w, h, zoom_factor)

        # Flip the image horizontally for a selfie horizontally for a selfie-view display. 
        cv2.namedWindow("MediaPipe Hands", cv2.WINDOW_KEEPRATIO)
        # Display the image.
        cv2.imshow("MediaPipe Hands", cv2.flip(image, 1) )
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
