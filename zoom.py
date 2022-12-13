import cv2

# Function to zoom on the detected face and follow it.
def zoom_in(image, x, y, w, h, zoom_factor):
    """_summary_

    Args:
        image (_type_): _description_
        x (_type_): _description_
        y (_type_): _description_
        w (_type_): _description_
        h (_type_): _description_
        zoom_factor (_type_): _description_

    Returns:
        _type_: _description_
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