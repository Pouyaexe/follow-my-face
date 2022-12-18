import cv2

# Load the Haar cascade classifier for face detection.
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def detect_face(image):
    """d

    Args:
        image (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Detect faces in the image.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces
