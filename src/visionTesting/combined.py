import cv2
import mediapipe as mp
import threading
import cv2
import numpy as np
import time


cap = cv2.VideoCapture(0)
reader = cv2.QRCodeDetector()
model = r'C:\Users\leaht\Desktop\Modules\roboticsAssignment\EE413-Assignment1\src\visionTesting\task\gesture_recognizer.task' 
# ^will need to change if running on other laptops!!
latest_result = None

def main():
    #initialise camera
    while True: 
        ret, frame = cap.read()
        qrCode = None
        gesture = None

        if not ret:
            break
            
        #read qr code
        #loops until qr is detected
        if qrCode is None:
            qrCode = readCode(frame)

            if qrCode:
                print('QR Code detected')
                print(qrCode)

        #display & ask for response


        #analyse gesture response
        if gesture == None:
            gesture = readGesture(frame)

            if gesture:
                print(gesture, 'detected')

                if gesture == 'Thumbs up':      #if thumbs up, robot carries out task 
                    taskToComplete = qrCode  #corresponding to that QR code
                    print('Gesture detected: ', gesture)
                    print('Carrying out Pallet ', qrCode)
                    return taskToComplete
                

                elif gesture == 'Thumbs down':       #if thumbs down, robot picks up a 
                    taskToComplete = 'Next QR Code'  #different QR code & repeats process
                    print('Gesture detected: ', gesture)
                    print('Showing next QR code')
                    return taskToComplete


        cv2.imshow('Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()


def readCode(frame):
    data, bbox, _ = reader.detectAndDecode(frame)
    if data:
        return data
    return None

def render_callback(result, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    latest_result = result

def readGesture(frame):
    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model), #, delegate=python.BaseOptions.Delegate.GPU),
        running_mode=VisionRunningMode.LIVE_STREAM,
        #num_hands=1,
        result_callback=render_callback
    )

    HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),      #thumb
        (0, 5), (5, 6), (6, 7), (7, 8),      #index finger
        (9, 10), (10, 11), (11, 12),         #middle finger
        (13, 14), (14, 15), (15, 16),        # ring finger
        (0, 17), (17, 18), (18, 19), (19, 20),#pinky
        (5, 9), (9, 13), (13, 17)            #palm 
    ]

    with GestureRecognizer.create_from_options(options) as recognizer:
        h,w,_ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        frame_timestamp_ms = int(time.time() * 1000)
    
        recognizer.recognize_async(mp_image, frame_timestamp_ms)

        if latest_result is not None:
                        
            if latest_result.gestures:
                for hand_index, hand_gestures in enumerate(latest_result.gestures):
                    if hand_gestures:
                        top_gesture = hand_gestures[0]
                        gesture_name = top_gesture.category_name

                        score = top_gesture.score
                        text = f"Hand {hand_index}: {gesture_name} ({score:.2f})"
                        cv2.putText(frame, text, (10, 50 + (hand_index * 40)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                        if gesture_name == 'Thumb_Up':
                            gesture = 'Thumbs up'
                            return gesture

                        if gesture_name == 'Thumb_Down':
                            gesture = 'Thumbs down'
                            return gesture


if __name__ == "__main__":
    main()