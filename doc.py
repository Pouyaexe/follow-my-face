import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Load the Haar cascade classifier for face detection.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
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
        # Calculate the angle between the index finger and thumb.
        image_height, image_width, _ = image.shape
        
        index_finger_tip_coords = (
            hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width,
            hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height,
        )
        thumb_base_coords = (
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x * image_width,
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * image_height,
        )
        import math
        delta_x = index_finger_tip_coords[0] - thumb_base_coords[0]
        delta_y = index_finger_tip_coords[1] - thumb_base_coords[1]
        angle = math.atan2(delta_y, delta_x)
        angle = math.degrees(angle)
        
        image = cv2.flip(image, 1)
        # Write the angle on the webcam feed in the top left corner in white.
        cv2.putText(image, f"Angle: {angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        image = cv2.flip(image, 1)
        
        # Draw the hand landmarks and connections on the image.
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    # Flip the image horizontally for a selfie horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()