
# DIY Face Unlock (OpenCV - LBPH)

This project adds a **DIY face unlock** flow to your PC using your regular webcam. 
It uses **OpenCV's LBPH face recognizer** (from `opencv-contrib-python`) to learn your face and recognize it live.
> ⚠️ Security note: This is for learning/demo purposes. It is **not as secure** as Windows Hello. If you choose to auto-type your PIN/password, you accept the risk.

## Folder Structure
```
FaceUnlockDIY/
├─ README.md
├─ requirements.txt
├─ src/
│  ├─ capture_faces.py
│  ├─ train_model.py
│  ├─ face_unlock.py
│  └─ utils.py
├─ models/
│  └─ (generated) lbph_model.xml
└─ data/
   └─ faces/
      └─ person_1/  (captured images)
```

## Quick Start (Windows)
1. (Optional but recommended) Create a virtual environment:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Capture face samples (keep your face centered, neutral light):
   ```powershell
   python src/capture_faces.py --name you --count 60
   ```
4. Train the model:
   ```powershell
   python src/train_model.py
   ```
5. (Optional) Set an environment variable with your **Windows PIN** for auto-unlock (RISKY):
   ```powershell
   setx FACE_UNLOCK_PIN 1234
   ```
   Restart your terminal/apps so the variable is available.
6. Run live unlock demo:
   ```powershell
   python src/face_unlock.py --user you --confidence 60
   ```

### Auto-run on wake/lock (Task Scheduler)
Create a basic task that triggers **on workstation unlock** and runs:
```
python "C:\path\to\FaceUnlockDIY\src\face_unlock.py" --user you --confidence 60
```
Alternatively, use `schtasks`:
```powershell
schtasks /Create /TN "FaceUnlockDIY" /TR "python C:\path\to\FaceUnlockDIY\src\face_unlock.py --user you --confidence 60" /SC ONEVENT /EC Security /MO "*[System[(EventID=4801)]]"
```
> Event ID 4801 = "The workstation was unlocked." Make sure your Python path is correct and your venv is activated in the task (use a wrapper .bat if needed).

## Tips
- Good lighting improves accuracy.
- Capture 60–120 images with slight angles/expressions.
- If you add more users, run `capture_faces.py` for each, then retrain.

## Uninstall
Delete the folder. If you added a Task Scheduler task:
```powershell
schtasks /Delete /TN "FaceUnlockDIY" /F
```
If you created `FACE_UNLOCK_PIN`, remove it in **System Properties → Environment Variables**.
