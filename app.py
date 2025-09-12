import cv2
import json
from flask import Flask, Response

app = Flask(__name__)

# Map each location to (video, slots JSON)
locations = {
    "Basement": ("D:\\Data_Science_cllg\\SelfLearning\\Projects\\VisionPark-Parking-Space-Mangement\\location1.mp4", "D:\\Data_Science_cllg\\SelfLearning\\Projects\\VisionPark-Parking-Space-Mangement\\location1.json"),
    "NUV School Ground": ("D:\\Data_Science_cllg\\SelfLearning\\Projects\\VisionPark-Parking-Space-Mangement\\location2.mp4", "D:\\Data_Science_cllg\\SelfLearning\\Projects\\VisionPark-Parking-Space-Mangement\\location2.json"),
    "Viklang Parking": ("C:\\Users\\Admin\\Desktop\\internship_projects\\parking_system\\final_website_integration\\videos\\location3.mp4", "C:\\Users\\Admin\\Desktop\\internship_projects\\parking_system\\annotate+direct\\location3.json"),
    "Amphitheatre": ("C:\\Users\\Admin\\Desktop\\internship_projects\\parking_system\\final_website_integration\\videos\\location4.mp4", "C:\\Users\\Admin\\Desktop\\internship_projects\\parking_system\\annotate+direct\\location4.json"),
    "Slope": ("C:\\Users\\Admin\\Desktop\\internship_projects\\parking_system\\final_website_integration\\videos\\location5.mp4", "C:\\Users\\Admin\\Desktop\\internship_projects\\parking_system\\annotate+direct\\location5.json"),
}

def check_slot_status(frame, slot):
    x, y, w, h = slot["x"], slot["y"], slot["w"], slot["h"]

    if w < 0:  # fix negative width
        x += w
        w = abs(w)
    if h < 0:  # fix negative height
        y += h
        h = abs(h)

    roi = frame[y:y+h, x:x+w]
    if roi.size == 0:
        return "unknown"

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 3)
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    non_zero = cv2.countNonZero(th)
    total = th.size
    filled_ratio = non_zero / total

    return "occupied" if filled_ratio > 0.3 else "empty"


def generate_frames(video_path, slots_path):
    with open(slots_path, "r") as f:
        slots = json.load(f)

    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Draw slots
        for slot in slots:
            status = check_slot_status(frame, slot)
            color = (0, 0, 255) if status == "occupied" else (0, 255, 0)
            cv2.rectangle(frame,
                          (slot["x"], slot["y"]),
                          (slot["x"] + slot["w"], slot["y"] + slot["h"]),
                          color, 2)
            cv2.putText(frame, status, (slot["x"], slot["y"] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Convert to jpg
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()


@app.route("/video/<location>")
def video_feed(location):
    if location not in locations:
        return "Invalid location", 404

    video_path, slots_path = locations[location]
    return Response(generate_frames(video_path, slots_path),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
