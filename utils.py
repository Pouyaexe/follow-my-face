import cv2

# Function to zoom on the detected face and follow it.
def zoom_in(image, x, y, w, h, zoom_factor):
    """Zoom in on the face and follow it.

    Args:
        image: input image
        x: x coordinate of the face bounding box
        y: y coordinate of the face bounding box
        w: width of the face bounding box
        h: height of the face bounding box
        zoom_factor: zoom factor

    Returns:
        image: output image
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
def text_overlay(image, text, x, y, color, font_size):
    """Overlay text on image using cv.putText() but filip the image first, display the text, then flip the image back.

    Args:
        image (): input image
        text (_type_): overlay text
        x (_type_): x coordinate of the text
        y (_type_): y coordinate of the text
        color (_type_): color of the text
        font_size (_type_): font size of the text

    Returns:
        _type_: output image
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


def hand_zoom_factor(x, y, w, h, hand_landmarks, zoom_factor = 1):
    
    # Get the coordinates of the index finger tip.
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
    return zoom_factor

if __name__ == "__main__":
    pass