import cv2
from mediapipe import Packet
from mediapipe import module_util

# Open the webcam
capture = cv2.VideoCapture(0)

# Load the face detection model from MediaPipe
face_detection_model = module_util.load_graph('path/to/face_detection_model.pbtxt')

while True:
    # Capture the frame from the webcam
    ret, frame = capture.read()

    # Create a MediaPipe packet containing the frame
    packet = Packet(frame)

    # Pass the packet to the face detection model
    face_detection_model.input_side_packets['input_video'].packet = packet
    face_detection_model.RunAll()

    # Get the detection results from the model
    detections = face_detection_model.output_side_packets['output_detections'].packet.get()

    # Draw a rectangle around each face
    for detection in detections:
        x = detection.location.x
        y = detection.location.y
        w = detection.location.width
        h = detection.location.height
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Show the frame
    cv2.imshow('Webcam', frame)

    # Wait for the user to press a key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
capture.release()
cv2.destroyAllWindows()
