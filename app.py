import os
import cv2
import time
import face_recognition
from flask import Flask, render_template, Response, request, redirect, session
from utils.liveness import check_liveness

# ------------------- APP CONFIG -------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

ATTEMPTS = {}
MAX_ATTEMPTS = 5
BLOCK_TIME = 60

KNOWN_FACES = []
KNOWN_NAMES = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACES_DIR = os.path.join(BASE_DIR, "users", "faces")

# ------------------- LOAD KNOWN FACES -------------------
def load_faces():
    if not os.path.exists(FACES_DIR):
        print("Face directory not found:", FACES_DIR)
        return

    print("Loading faces from:", FACES_DIR)

    for file in os.listdir(FACES_DIR):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            print("Skipping non-image file:", file)
            continue

        path = os.path.join(FACES_DIR, file)

        # Load with OpenCV instead of face_recognition
        img = cv2.imread(path)

        if img is None:
            print("Failed to read image:", file)
            continue

        # Convert BGR → RGB
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        try:
            encodings = face_recognition.face_encodings(rgb_img)

            if len(encodings) == 0:
                print("No face found in:", file)
                continue

            KNOWN_FACES.append(encodings[0])
            KNOWN_NAMES.append(os.path.splitext(file)[0])

            print("Loaded face:", file)

        except Exception as e:
            print("Failed to encode:", file, "Reason:", e)



load_faces()

# ------------------- CAMERA -------------------
camera = cv2.VideoCapture(0)

# ------------------- VIDEO STREAM -------------------
def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

# ------------------- ROUTES -------------------
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/video")
def video():
    return Response(gen_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/authenticate", methods=["POST"])
def authenticate():
    ip = request.remote_addr
    now = time.time()

    # Rate limiting
    if ip in ATTEMPTS:
        count, last_time = ATTEMPTS[ip]
        if count >= MAX_ATTEMPTS and now - last_time < BLOCK_TIME:
            return "Too many attempts. Try later.", 403

    success, frame = camera.read()
    if not success:
        return "Camera error", 500

    # Liveness check
    if not check_liveness(frame):
        ATTEMPTS[ip] = (ATTEMPTS.get(ip, (0, 0))[0] + 1, now)
        return "Liveness failed", 401

    # Convert BGR → RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    for enc in encodings:
        matches = face_recognition.compare_faces(KNOWN_FACES, enc, tolerance=0.5)
        if True in matches:
            index = matches.index(True)
            session["user"] = KNOWN_NAMES[index]
            return redirect("/dashboard")

    ATTEMPTS[ip] = (ATTEMPTS.get(ip, (0, 0))[0] + 1, now)
    return "Face not recognized", 401


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ------------------- MAIN -------------------
if __name__ == "__main__":
    print("Starting Facial Authentication System...")
    app.run(debug=True)
