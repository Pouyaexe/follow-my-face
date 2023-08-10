# Follow My Face Project

The "Follow My Face" project is a Python program designed to track hands in a video feed using the MediaPipe framework. It utilizes the hand tracking capabilities of MediaPipe to detect the position of the index finger. This information is then used to implement facial zoom functionality, where the program zooms in on a detected face and keeps it in focus. Additionally, the project empowers users to control the mouse pointer through the hand tracking feature.

## Modules

The project is structured into distinct modules to enhance code organization:

- **main.py**: Serving as the program's entry point, this module initializes video capture and the hand tracker. It subsequently initiates the face tracking loop.

- **mouse.py**: This module incorporates the `MouseController` class, facilitating mouse pointer manipulation on the screen. The `MouseController` class encompasses methods for precise mouse movement to designated screen positions and mouse button clicks.

- **utils.py**: Various utility functions critical to the project are housed within this module. Notably, the `zoom_in` and `hand_zoom_factor` functions are pivotal in calculating the appropriate zoom level based on the index finger's position.

## Additional Files

The project repository includes several supplementary files:

- **pip_freeze.txt**: This file provides an exhaustive list of the Python packages essential for running the project seamlessly.

- **versions.txt**: Within this file, you can find version details for the libraries and packages used throughout the project.

## Getting Started

To begin using the program, follow these steps:

1. Ensure you have the required Python packages by referring to `pip_freeze.txt`.

2. Run the following command in your command line:

   ```
   python main.py
   ```

3. This command initializes the video capture and hand tracker. The program instantly starts detecting faces and hands in the video feed.

4. To leverage the facial zoom feature, position your index finger accordingly. The program will adjust the zoom level and track your face's movement.

5. Additionally, you can control the mouse pointer by utilizing hand gestures. The hand tracking functionality empowers you to interact with the program seamlessly.

Enjoy experimenting with the "Follow My Face" program and exploring its diverse capabilities!

Feel free to contribute, offer suggestions, or report issues. Happy coding!
