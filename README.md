# follow-my-face

The "follow my face" project is a python program that uses the MediaPipe framework to track hands in a video feed, and then uses the position of the index finger to zoom in on a detected face and follow it. The program also allows the user to control the mouse pointer using the hand tracker.

The project uses the OpenCV library for basic image processing and video capture, and the MediaPipe framework for hand tracking. The program is organized into several different modules:

main.py: This is the main entry point for the program. It initializes the video capture and the hand tracker, and then starts the face tracking loop.
mouse.py: This module contains the MouseController class, which can be used to move the mouse pointer on the screen. The MouseController class has methods for moving the mouse to a specific screen location, and for clicking the mouse buttons.
utils.py: This module contains various utility functions that are used throughout the project, including the zoom_in and hand_zoom_factor functions, which are used to calculate the zoom level based on the position of the index finger.
The project also includes a few other files:
main.py: This is the main entry point for the program. It initializes the video capture and the hand tracker, and then starts the face tracking loop.
face.py: This module contains the Face class, which represents a detected face in the video feed. The Face class has methods for drawing a bounding box around the face, and for tracking the face as it moves in the frame.
mouse.py: This module contains the MouseController class, which can be used to move the mouse pointer on the screen. The MouseController class has methods for moving the mouse to a specific screen location, and for clicking the mouse buttons.
utils.py: This module contains various utility functions that are used throughout the project, including the zoom_in and hand_zoom_factor functions, which are used to calculate the zoom level based on the position of the index finger.
The project also includes a few other files:

pip_freeze.txt: This is a list of all the python packages that are required to run the project.
versions.txt: This file contains the version numbers of the various libraries and packages that are used in the project.
To use the program, simply run python main.py from the command line. This will start the video capture and the hand tracker, and the program will begin tracking any faces and hands that are detected in the video feed. You can use the position of your index finger to zoom in on a face, and the face tracker will follow your face as you move around. You can also use your hand to move the mouse pointer and interact with the program.