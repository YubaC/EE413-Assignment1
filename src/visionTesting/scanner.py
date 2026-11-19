from pathlib import Path
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

reader = cv2.QRCodeDetector()
latest_result = None


def render_callback(result, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    latest_result = result


def readCode(frame):
    try:
        data, bbox, _ = reader.detectAndDecode(frame)
        if data:
            return data
    except cv2.error:
        # OpenCV error
        pass
    return None


def readGesture(frame, recognizer):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    frame_timestamp_ms = int(time.time() * 1000)

    recognizer.recognize_async(mp_image, frame_timestamp_ms)

    if latest_result is not None and latest_result.gestures:
        for hand_index, hand_gestures in enumerate(latest_result.gestures):
            if hand_gestures:
                top_gesture = hand_gestures[0]
                gesture_name = top_gesture.category_name
                score = top_gesture.score

                text = f"Hand {hand_index}: {gesture_name} ({score:.2f})"
                cv2.putText(
                    frame, text, (10, 50 + (hand_index * 40)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA
                )

                if gesture_name == "Thumb_Up":
                    return "Thumbs up"
                if gesture_name == "Thumb_Down":
                    return "Thumbs down"
    return None


def main():
    # Portable path anchored to this script's folder (works on any laptop)
    model_path = Path(__file__).resolve().parent / "task" / "gesture_recognizer.task"

    options = vision.GestureRecognizerOptions(
        base_options=python.BaseOptions(model_asset_path=str(model_path)),
        running_mode=vision.RunningMode.LIVE_STREAM,
        result_callback=render_callback,
    )

    cap = cv2.VideoCapture(0)
    qrCode = None
    gesture = None
    taskToComplete = None

    with vision.GestureRecognizer.create_from_options(options) as recognizer:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            #scan until a QR code is detected
            if qrCode is None:
                qrCode = readCode(frame)
                if qrCode is not None:
                    print("QR Code detected:", qrCode)
                    print("Show Thumbs Up to confirm or Thumbs Down to skip...")

            # once QR code is found scan frames for a gesture
            elif gesture is None:
                cv2.putText(
                    frame, f"QR: {qrCode} - Show Thumb Up/Down", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2
                )
                gesture = readGesture(frame, recognizer)

                if gesture == "Thumbs up":
                    taskToComplete = qrCode
                    print("Gesture detected:", gesture)
                    print("Carrying out Pallet", qrCode)
                    time.sleep(3)
                    break

                elif gesture == "Thumbs down":
                    taskToComplete = "Next QR Code"
                    print("Gesture detected:", gesture)
                    print("Showing next QR code...")
                    break

            cv2.imshow("Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    return taskToComplete



