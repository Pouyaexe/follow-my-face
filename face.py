import cv2

# Open the webcam
capture = cv2.VideoCapture(0)

while True:
    # Capture the frame from the webcam
    ret, frame = capture.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(gray)

    # Draw a rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Show the frame
    cv2.imshow('Webcam', frame)

    # Wait for the user to press a key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
capture.release()
cv2.destroyAllWindows()
