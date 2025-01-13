import mediapipe as mp

# Initialize Mediapipe Hands
MPHands = mp.solutions.hands
hands = MPHands.Hands(min_detection_confidence=0.01)
MPDraw = mp.solutions.drawing_utils


def detect_hand_gesture(frame):
    result = hands.process(frame)
    img_height, img_width = frame.shape[:2]

    x_pos, y_pos = None, None

    if result.multi_hand_landmarks:
        for handLM in result.multi_hand_landmarks:
            for i, lm in enumerate(handLM.landmark):
                if i == 8:
                    x_pos = int(lm.x * img_width)
                    y_pos = int(lm.y * img_height)
                    return x_pos, y_pos

    return x_pos, y_pos
