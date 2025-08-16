
import os
import argparse
import cv2
from utils import detect_faces_bgr, crop_face, draw_faces, ensure_dir, beep

def main():
    parser = argparse.ArgumentParser(description="Capture face images for training.")
    parser.add_argument("--name", required=True, help="User name/label (folder name).")
    parser.add_argument("--count", type=int, default=60, help="Number of images to capture.")
    parser.add_argument("--output", default=os.path.join("..", "data", "faces"), help="Output base folder.")
    args = parser.parse_args()

    user_dir = os.path.join(args.output, args.name)
    ensure_dir(user_dir)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam.")

    print(f"[INFO] Capturing {args.count} images for '{args.name}'… Press 'q' to quit early.")
    saved = 0
    while saved < args.count:
        ret, frame = cap.read()
        if not ret:
            continue

        faces, gray = detect_faces_bgr(frame)
        if len(faces) > 0:
            # Take the largest face (closest to camera)
            faces = sorted(faces, key=lambda b: b[2]*b[3], reverse=True)
            (x, y, w, h) = faces[0]
            face_img = crop_face(gray, x, y, w, h)
            filepath = os.path.join(user_dir, f"{saved:04d}.png")
            cv2.imwrite(filepath, face_img)
            saved += 1
            beep()

        draw_faces(frame, faces)
        cv2.putText(frame, f"Saved: {saved}/{args.count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.imshow("Capture Faces", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[OK] Done. Images saved to:", user_dir)

if __name__ == "__main__":
    main()
