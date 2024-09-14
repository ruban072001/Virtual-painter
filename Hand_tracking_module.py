import cv2   # Importing OpenCV module
import mediapipe as mp  # Importing Mediapipe module for hand tracking
import time  # Importing time module to calculate fps


class HandTracking:
    def __init__(self, mode: bool = False, max_hands: int = 2, detection_confidence: float = 0.5, tracking_confidence: float = 0.5):
        # Hand tracking initialization
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        # Initialize Mediapipe hands module
        self.mphand = mp.solutions.hands
        self.hand = self.mphand.Hands(self.mode, self.max_hands)
        self.draw = mp.solutions.drawing_utils  # Drawing utilities

    def find_hands(self, frame, draw: bool = True):
        """
        Detect and optionally draw hand landmarks on the given frame.
        """
        # Convert BGR to RGB for Mediapipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.hand_process = self.hand.process(rgb_frame)

        # If hands are detected, draw landmarks
        if self.hand_process.multi_hand_landmarks:
            for land_mark in self.hand_process.multi_hand_landmarks:
                if draw:
                    self.draw.draw_landmarks(frame, land_mark, self.mphand.HAND_CONNECTIONS)
        return frame

    def find_position(self, frame, draw: bool = True, landmark_list: list = None):
        """
        Find specific hand landmark positions and optionally draw circles on them.
        Returns the frame and a list of (x, y) positions of the landmarks.
        """
        posi = []
        if landmark_list is None:
            landmark_list = []  # If no specific landmarks are requested

        # If hands are detected, find landmarks
        if self.hand_process.multi_hand_landmarks:
            for land_mark in self.hand_process.multi_hand_landmarks:
                for id, lm in enumerate(land_mark.landmark):
                    h, w, c = frame.shape  # Frame dimensions
                    x_pos, y_pos = int(w * lm.x), int(h * lm.y)  # Landmark positions
                    if id in landmark_list:
                        posi.append((x_pos, y_pos))
                    if draw and id in landmark_list:  # Draw only if the landmark is in the list
                        cv2.circle(frame, (x_pos, y_pos), 8, (255, 0, 0), -1)

        return frame, posi


def run_hand_track():
    # Capture webcam
    vid = cv2.VideoCapture(0)

    # Initialize frame timing
    prev_time = 0

    # Create hand tracking object
    detector = HandTracking()

    while True:
        ret, frame = vid.read()  # Capture frame
        if not ret:
            break

        # Find hands and positions in the frame
        frame = detector.find_hands(frame)
        frame, positions = detector.find_position(frame, True, [4])  # Track specific landmarks

        if positions:
            print(positions)  # Print landmark positions

        # Calculate FPS
        current_time = time.time()
        fps = 1 / max((current_time - prev_time), 1e-6)  # Avoid division by 0
        prev_time = current_time

        # Display FPS on frame
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the frame
        cv2.imshow('Hand Tracking', frame)

        # Break loop with 'q' key
        if cv2.waitKey(1) == ord('q'):
            break

    # Release resources
    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_hand_track()
