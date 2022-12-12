# Print the version of the Python interpreter, opencv, numpy, matplotlib, mediapipe and save the output to a text file.
import sys
import cv2
import numpy as np
import matplotlib
import mediapipe as mp
import datetime

# Wrtie the versions to a text file.
with open("versions.txt", "w") as f:
    f.write("Python version: " + sys.version + "\n")
    f.write("OpenCV version: " + cv2.__version__ + "\n")
    f.write("Numpy version: " + np.__version__ + "\n")
    f.write("Matplotlib version: " + matplotlib.__version__ + "\n")
    f.write("Mediapipe version: " + mp.__version__ + "\n")
    f.write("numpy version: " + np.__version__ + "\n")
    