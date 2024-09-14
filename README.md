**Virtual Painter Using Hand Tracking with OpenCV and Mediapipe**

This project is a virtual painter application where users can draw on the screen using their hands. The application uses hand tracking to detect finger movements and simulates painting on a canvas. Users can select different colors and draw on the canvas in real-time using gestures.


**Features**

1. **Real-time hand tracking:** Tracks hand and finger movements using Mediapipe and OpenCV.

2. **Gesture-based drawing:** Uses specific hand gestures to enter "selection" or "drawing" modes.

3. **Color selection:** Choose different colors by pointing at the color palette displayed at the top of the screen.

4. **High FPS:** The application displays the current frames per second (FPS) to monitor performance.


**Project Structure**

1. **Hand_tracking_module.py:** A custom hand-tracking module that contains the logic for detecting and processing hand landmarks.

2. **Virtual Painter:** The main Python script that combines hand tracking with drawing functionality.


**Requirements**

To run this project, you will need the following libraries:

**OpenCV:** For image and video processing.
**Mediapipe:** For hand tracking and gesture recognition.
**Numpy:** For handling canvas operations.


**How It Works**

**HandTracking Module:**

1. Detects hand landmarks and returns the positions of key finger joints.

2. The landmarks are used to determine whether the user is selecting a color or drawing on the screen.


**Selection Mode:**

1. When the index and middle fingers are up, and all other fingers are down, the program enters selection mode.
2. In this mode, the user can select a color from the color palette at the top of the screen by pointing their fingers.


**Drawing Mode:**

1. When only the index finger is up, the user can draw on the canvas.

2. Drawing starts from the position of the index finger, and the color can be chosen from the palette.


**Virtual Canvas:**

A virtual canvas is created to track the drawing. The canvas is merged with the real-time webcam feed, so it looks like the drawing is happening live on the video.


**Control Instructions:**

**Selecting Colors:**

Move your hand over the color palette at the top of the screen. Colors will be selected based on the position of your index and middle fingers.

**Drawing:**

Use only your index finger to draw on the screen. The drawing will be done in the selected color.

**Clear Screen:**

Select the black color from the palette to reset the screen (erase everything).

**Exit:**

Press the q key to quit the program.

**Files and Folders**

**images for painting/:** This folder contains the color palette images used for selection.

**Hand_tracking_module.py:** The hand tracking module used to detect hand landmarks.

**virtual_painter.py:** The main script for running the virtual painter application.
