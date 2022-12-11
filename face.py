import cv2
import numpy as np

# Create a cascade classifier object
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

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

    # Show the frame
    cv2.imshow("Face Detection", frame)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Extract skin-color pixels using the HSV range
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Erode and dilate the mask to remove small holes and blur the edges
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and check if they form the "L" shape of a hand
    for contour in contours:
        # Approximate the contour to a polygon
        polygon = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # Check if the polygon has exactly 4 vertices and is convex
        if len(polygon) == 4 and cv2.isContourConvex(polygon):
            # Get the bounding box of the polygon
            x, y, w, h = cv2.boundingRect(polygon)

            # Calculate the aspect ratio of the bounding box
            aspect_ratio = float(w) / h

            # Check if the aspect ratio is approximately 1.0 (i.e. the polygon is a square)
            if 0.9 <= aspect_ratio <= 1.1:
                # Check if the polygon forms an "L" shape with 2 long sides and 2 short sides
                sides = [
                    (polygon[i][0][0] - polygon[i - 1][0][0]) ** 2
                    + (polygon[i][0][1] - polygon[i - 1][0][1]) ** 2
                    for i in range(4)
                ]
                sides = sorted(sides)
                if sides[0] < sides[1] < sides[2] < sides[3]:
                    print("Zoom")

                # Print "Zoom" in the terminal
                print("Zoom")

    # Check if the user hit the 'Esc' key
    c = cv2.waitKey(1)
    if c == 27:
        break
