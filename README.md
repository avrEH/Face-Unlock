DIY Face Unlock (OpenCV + LBPH)

This is a little side project that lets you unlock your PC with your face using your regular webcam.
It’s built with OpenCV’s LBPH face recognizer (from opencv-contrib-python) and can recognize your face in real time.

⚠️ Heads up: This is just for learning and fun. It’s nowhere near as secure as Windows Hello. If you set it up to type your PIN/password automatically, do it at your own risk.

Project Structure
FaceUnlockDIY/
├─ README.md
├─ requirements.txt
├─ src/
│  ├─ capture_faces.py
│  ├─ train_model.py
│  ├─ face_unlock.py
│  └─ utils.py
├─ models/
│  └─ lbph_model.xml (created after training)
└─ data/
   └─ faces/
      └─ person_1/  (captured images go here)

Getting Started (Windows)

(Optional) Create a virtual environment:

py -3 -m venv .venv
.\.venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Capture some face samples (look straight at the camera, good lighting helps):

python src/capture_faces.py --name you --count 60


Train the face recognition model:

python src/train_model.py


(Optional) Save your Windows PIN as an environment variable (⚠️ not secure):

setx FACE_UNLOCK_PIN 1234


Run the face unlock demo:

python src/face_unlock.py --user you --confidence 60

Auto-run on Unlock

You can make this run automatically whenever you unlock your PC with Task Scheduler:

python "C:\path\to\FaceUnlockDIY\src\face_unlock.py" --user you --confidence 60


Or with schtasks:

schtasks /Create /TN "FaceUnlockDIY" /TR "python C:\path\to\FaceUnlockDIY\src\face_unlock.py --user you --confidence 60" /SC ONEVENT /EC Security /MO "*[System[(EventID=4801)]]"


Event ID 4801 = “The workstation was unlocked.”
If you’re using a virtual environment, create a small .bat file to activate it first, then call Python.

Tips

More samples (60–120) = better accuracy.

Capture at slightly different angles/expressions.

Good lighting makes a big difference.

Add more users by capturing faces for each one, then retrain.

Uninstall

Just delete the folder.

If you added a Task Scheduler task:

schtasks /Delete /TN "FaceUnlockDIY" /F


To remove the FACE_UNLOCK_PIN, go to System Properties → Environment Variables.
