
import os
import cv2
import numpy as np
import argparse
import pickle

from utils import ensure_dir

def read_images_and_labels(base_dir):
    images, labels, label_map = [], [], {}
    current_label = 0

    for name in sorted(os.listdir(base_dir)):
        person_dir = os.path.join(base_dir, name)
        if not os.path.isdir(person_dir):
            continue
        label_map[current_label] = name
        for fname in sorted(os.listdir(person_dir)):
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(person_dir, fname)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                images.append(img)
                labels.append(current_label)
        current_label += 1

    return images, np.array(labels, dtype=np.int32), label_map

def main():
    parser = argparse.ArgumentParser(description="Train LBPH model from captured faces.")
    parser.add_argument("--faces", default=os.path.join("..", "data", "faces"), help="Faces base dir.")
    parser.add_argument("--model", default=os.path.join("..", "models", "lbph_model.xml"), help="Output model path.")
    parser.add_argument("--labels", default=os.path.join("..", "models", "labels.pkl"), help="Output labels map.")
    args = parser.parse_args()

    ensure_dir(os.path.dirname(args.model))

    images, labels, label_map = read_images_and_labels(args.faces)
    if len(images) == 0:
        raise RuntimeError("No training images found. Run capture_faces.py first.")

    recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
    recognizer.train(images, labels)
    recognizer.save(args.model)

    with open(args.labels, "wb") as f:
        pickle.dump(label_map, f)

    print(f"[OK] Trained. Model -> {args.model}, labels -> {args.labels}")
    print("[INFO] You can run face_unlock.py now.")

if __name__ == "__main__":
    main()
