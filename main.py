import cv2
import mediapipe as mp
from utils import zoom_in, hand_zoom_factor
from mouse import move_mouse, click_mouse
import tkinter as tk
from tkinter import PhotoImage
import PIL.Image, PIL.ImageTk
mp_hands = mp.solutions.hands

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.label = tk.Label(self)
        self.label.pack()

        self.geometry("800x600")
        self.title("MediaPipe Hands")


# Load the Haar cascade classifier for face detection.
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

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
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw a rectangle around each detected face. The color is BGR. so for a white rectangle, we use (255, 255, 255).
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape

        if results.multi_hand_landmarks:            
            # Get the zoom factor and draw the hand landmarks and connections on the image.
            image, zoom_factor = hand_zoom_factor(image, results, x, y, w, h, zoom_factor)           
            # Move the mouse cursor.
            move_mouse(results.multi_hand_landmarks[0].landmark[8].x, results.multi_hand_landmarks[0].landmark[8].y)
                    
        # if the zoom factor is greater than 1, then we are zoomed in on the face.
        if zoom_factor > 1:
            # Draw the zoomed in face on the screen.
            image = zoom_in(image, x, y, w, h, zoom_factor)

        # Convert the image to a PhotoImage object
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        image = PIL.ImageTk.PhotoImage(image)

        # Update the label with the new image
        self.label.configure(image=image)
        self.label.image = image

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()

if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()
