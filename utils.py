import cv2
import mediapipe as mp
from typing import Tuple
import numpy as np
from mouse import move_mouse
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Function to zoom on the detected face and follow it.
def zoom_in(image: np.ndarray, x: int, y: int, w: int, h: int, zoom_factor: float) -> np.ndarray:
    """Zoom in on the face and follow it.

    Args:
        image (np.ndarray): input image
        x (int): x coordinate of the face bounding box
        y (int): y coordinate of the face bounding box
        w (int): width of the face bounding box
        h (int): height of the face bounding box
        zoom_factor (float): zoom factor

    Returns:
        np.ndarray: zoomed in image
    """

    # Zoom factor must be greater than 1.
    zoom_factor = zoom_factor**4

    # Get the width and height of the face bounding box.
    face_width, face_height = w, h

    # Get the center of the face.
    face_x, face_y = x + face_width / 2, y + face_height / 2

    # Calculate the starting and ending x and y coordinates of the face in the image.
    start_x, start_y, end_x, end_y = face_x - face_width / 2 * zoom_factor, face_y - face_height / 2 * zoom_factor, face_x + face_width / 2 * zoom_factor, face_y + face_height / 2 * zoom_factor

    # Make sure the starting and ending x and y coordinates are within the bounds of the image. 
    start_x = max(0, start_x)
    start_y = max(0, start_y)
    end_x = min(image.shape[1] - 1, end_x)
    end_y = min(image.shape[0] - 1, end_y)

    # Get the sub-image of the face.
    face_image = image[int(start_y) : int(end_y), int(start_x) : int(end_x)]

    # Resize the face image to fit the original image size, keep the aspect ratio.
    face_image = cv2.resize(
        face_image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LANCZOS4, dst=face_image )
    image = face_image
    # Overlay the face image on the original image.
    # image = cv2.addWeighted(src1=image, alpha=0, src2=face_image, beta=1, gamma=0)
    return image

# Function to overlay text on image using cv.putText() but filip the image first, display the text, then flip the image back.
def text_overlay(image: np.ndarray, text: str, x: int, y: int, color: Tuple[int, int, int], font_size: float) -> np.ndarray:
    """Overlay text on image using cv.putText() but filip the image first, display the text, then flip the image back.

    Args:
        image (np.ndarray): input image
        text (str): text to overlay
        x (int): x coordinate of the text
        y (int): y coordinate of the text
        color (Tuple[int, int, int]): color of the text
        font_size (float): font size of the text

    Returns:
        np.ndarray: output image
    """
    # flip the image horizontally
    image = cv2.flip(image, 1)
    # create the text overlay
    cv2.putText(
        img=image,
        text=text,
        org=(x, y),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=font_size,
        color=color,
        thickness=2,
    )
    # flip the image back to its original orientation
    image = cv2.flip(image, 1)
    return image


def hand_zoom_factor(image: np.ndarray, results: mp_hands.Hands, x:int, y:int, w:int, h:int, zoom_factor:float = 1)-> Tuple[np.ndarray, float] :   
    """Get the zoom factor based on the hand landmarks.
    
    Args:
        image (np.ndarray): input image
        results (mp_hands.Hands): hand landmarks
        x (int): x coordinate of the face bounding box
        y (int): y coordinate of the face bounding box
        w (int): width of the face bounding box
        h (int): height of the face bounding box
        zoom_factor (float, optional): zoom factor. Defaults to 1.

    Returns:
        Tuple[np.ndarray, float]: output image and zoom factor
    """    
    
    image_height, image_width, _ = image.shape

    for hand_landmarks in results.multi_hand_landmarks:
                    # Get the zoom factor based on the hand landmarks.    
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

        if index_finger_tip_coords[0] > image_width * 0.75:
            if index_finger_tip_coords[1] < image_height * 0.25:
                zoom_factor = 1.25
            elif index_finger_tip_coords[1] > image_height * 0.75:
                zoom_factor = 1.1
        if index_finger_tip_coords[0] < image_width * 0.25:
            if index_finger_tip_coords[1] < image_height * 0.25:
                zoom_factor = 1.25
            elif index_finger_tip_coords[1] > image_height * 0.75:
                zoom_factor = 1.1
        if (
            wrist_coords[0] > x
            and wrist_coords[0] < x + w
            and wrist_coords[1] > y
            and wrist_coords[1] < y + h
        ):
            zoom_factor = 1
            
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
    return image, zoom_factor

def process_hands(image, results, x, y, w, h, zoom_factor):
    """Process the hand landmarks.

    Args:
        image (np.ndarray): input image
        results (mp_hands.Hands): hand landmarks
        x (int): x coordinate of the face bounding box
        y (int): y coordinate of the face bounding box
        w (int): width of the face bounding box
        h (int): height of the face bounding box
        zoom_factor (float): zoom factor

    Returns:
        np.ndarray: output image
    """
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape

    if results.multi_hand_landmarks:            
        # Get the zoom factor and draw the hand landmarks and connections on the image.
        image, zoom_factor = hand_zoom_factor(image, results, x, y, w, h, zoom_factor)           
        # Move the mouse cursor.
        move_mouse(results.multi_hand_landmarks[0].landmark[8].x, results.multi_hand_landmarks[0].landmark[8].y)
    return image, zoom_factor

if __name__ == "__main__":
    pass