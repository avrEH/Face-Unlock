
import os
import time
import argparse
import pickle
import cv2
import numpy as np
import pyautogui

from utils import detect_faces_bgr, crop_face, draw_faces, beep

def type_pin(pin: str):
    # WARNING: Simulates keystrokes to type your PIN then press Enter.
    # Use at your own risk.
    pyautogui.typewrite(pin, interval=0.05)
    pyautogui.press("enter")

def main():
    parser = argparse.ArgumentParser(description="Live face unlock with LBPH.")
    parser.add_argument("--user", required=True, help="Expected user label (folder name used during capture).")
    parser.add_argument("--model", default=os.path.join("..", "models", "lbph_model.xml"))
    parser.add_argument("--labels", default=os.path.join("..", "models", "labels.pkl"))
    parser.add_argument("--confidence", type=int, default=60, help="Max confidence threshold (lower is better).")
    parser.add_argument("--autotype", action="store_true", help="Auto-type FACE_UNLOCK_PIN if user matches.")
    parser.add_argument("--cooldown", type=float, default=5.0, help="Seconds to wait after an unlock attempt.")
    args = parser.parse_args()

    if not os.path.exists(args.model):
        raise FileNotFoundError("Model not found. Train first with train_model.py")
    if not os.path.exists(args.labels):
        raise FileNotFoundError("Labels not found. Train first with train_model.py")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(args.model)
    with open(args.labels, "rb") as f:
        label_map = pickle.load(f)

    # Reverse map: name -> id
    name_to_id = {v: k for k, v in label_map.items()}
    if args.user not in name_to_id:
        raise ValueError(f"User '{args.user}' not found in labels. Known: {list(name_to_id.keys())}")
    target_id = name_to_id[args.user]

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam.")

    last_attempt = 0
    print("[INFO] Looking for your face. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        faces, gray = detect_faces_bgr(frame)
        pred_name, pred_conf = None, None

        if len(faces) > 0:
            faces = sorted(faces, key=lambda b: b[2]*b[3], reverse=True)
            (x, y, w, h) = faces[0]
            face_img = crop_face(gray, x, y, w, h)

            label_id, conf = recognizer.predict(face_img)  # lower conf = better
            pred_name = label_map.get(label_id, "unknown")
            pred_conf = conf

            # Visual feedback
            cv2.putText(frame, f"{pred_name} ({conf:.1f})", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0) if label_id==target_id else (0,0,255), 2)

            if (label_id == target_id) and (conf <= args.confidence) and (time.time() - last_attempt > args.cooldown):
                print(f"[OK] {pred_name} recognized with confidence {conf:.1f} <= {args.confidence}.")
                beep()
                if args.autotype:
                    pin = os.getenv("FACE_UNLOCK_PIN")
                    if pin:
                        print("[INFO] Auto-typing PIN…")
                        type_pin(pin)
                    else:
                        print("[WARN] FACE_UNLOCK_PIN not set. Skipping auto-type.")
                last_attempt = time.time()

        draw_faces(frame, faces)
        if pred_conf is not None:
            cv2.putText(frame, f"ConfThresh: <= {args.confidence} (lower=better)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        cv2.imshow("Face Unlock (LBPH)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
