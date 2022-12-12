import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Load the Haar cascade classifier for face detection.
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Global zoom factor. if the zoom factor goes higher than 1, the image will zoom in on the detected face.
zoom_factor = 1

# Function to overlay text on image using cv.putText() but filip the image first, display the text, then flip the image back.
def text_overlay(image, text, x, y, color, font_size):
    image = cv2.flip(image, 1)
    cv2.putText(
        img=image,
        text=text,
        org=(x, y),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=font_size,
        color=color,
        thickness=2,
    )
    image = cv2.flip(image, 1)
    return image


# Function to zoom on the detected face and follow it.
def zoom_in(image, x, y, w, h, zoom_factor):

    # Zoom factor must be greater than 1.
    zoom_factor = zoom_factor**4
    # Get the width and height of the face bounding box.
    face_width, face_height = w, h

    # Get the center of the face.
    face_x, face_y = x + face_width / 2, y + face_height / 2

    # Calculate the starting and ending x and y coordinates of the face in the image.
    start_x, start_y, end_x, end_y = (
        face_x - face_width / 2 * zoom_factor,
        face_y - face_height / 2 * zoom_factor,
        face_x + face_width / 2 * zoom_factor,
        face_y + face_height / 2 * zoom_factor,
    )

    # Make sure the starting and ending x and y coordinates are within the bounds of the image.
    start_x = max(0, start_x)
    start_y = max(0, start_y)
    end_x = min(image.shape[1] - 1, end_x)
    end_y = min(image.shape[0] - 1, end_y)

    # Get the sub-image of the face.
    face_image = image[int(start_y) : int(end_y), int(start_x) : int(end_x)]

    # Resize the face image to fit the original image size, keep the aspect ratio.
    face_image = cv2.resize(
        face_image,
        (image.shape[1], image.shape[0]),
        interpolation=cv2.INTER_LANCZOS4,
        dst=face_image,
    )
    image = face_image
    # Overlay the face image on the original image.
    # image = cv2.addWeighted(src1=image, alpha=0, src2=face_image, beta=1, gamma=0)
    return image


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
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the index finger tip.
                image_height, image_width, _ = image.shape

                index_finger_tip_coords = (
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                    * image_width,
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    * image_height,
                )
                wrist_coords = (
                    hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                    * image_width,
                    hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
                    * image_height,
                )
                # See if the index finger is in the right bezel of the screen.
                if index_finger_tip_coords[0] > image_width * 0.75:
                    # See if the index finger is in the top bezel of the screen.
                    if index_finger_tip_coords[1] < image_height * 0.25:
                        # Zoom in on the face.
                        zoom_factor = 1.25
                    # See if the index finger is in the bottom bezel of the screen.
                    elif index_finger_tip_coords[1] > image_height * 0.75:
                        # Zoom out on the face.
                        zoom_factor = 1.1
                # See if the index finger is in the left bezel of the screen.
                if index_finger_tip_coords[0] < image_width * 0.25:
                    # See if the index finger is in the top bezel of the screen.
                    if index_finger_tip_coords[1] < image_height * 0.25:
                        # Zoom in on the face.
                        zoom_factor = 1.25
                    # See if the index finger is in the bottom bezel of the screen.
                    elif index_finger_tip_coords[1] > image_height * 0.75:
                        # Zoom out on the face.
                        zoom_factor = 1.1
                # see if both of the wrist are in the face bounding box, zoom out.
                if (
                    wrist_coords[0] > x
                    and wrist_coords[0] < x + w
                    and wrist_coords[1] > y
                    and wrist_coords[1] < y + h
                ):
                    zoom_factor = 1

                # Write the hand detcted text on the down right corner of the screen.
                image = text_overlay(image,"Hand detected",image_width - 200,image_height - 30,(0, 255, 0))
                    

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

        cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
