import cv2
import json
from tkinter import Tk, filedialog

annotations = []
slot_id = 0
drawing = False
ix, iy = -1, -1
frame_copy = None

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, slot_id, frame_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        slot_id += 1
        w, h = x - ix, y - iy
        annotations.append({
            "id": slot_id,
            "x": ix,
            "y": iy,
            "w": w,
            "h": h,
            "status": "unknown"
        })
        cv2.rectangle(frame_copy, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow("Annotator", frame_copy)

def select_video():
    """Open a file dialog to select video file."""
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select a Video",
        filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")]
    )
    return file_path

def annotate_video(output_json="slots.json"):
    global annotations, slot_id, frame_copy
    annotations = []
    slot_id = 0

    video_path = select_video()
    if not video_path:
        print("❌ No video selected. Exiting...")
        return

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Could not read video.")
        return

    frame_copy = frame.copy()
    cv2.imshow("Annotator", frame_copy)
    cv2.setMouseCallback("Annotator", draw_rectangle)

    print("➡️ Draw rectangles with LEFT mouse button. Press 'q' to save and exit.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    with open(output_json, "w") as f:
        json.dump(annotations, f, indent=4)
    print(f"✅ Annotations saved to {output_json}")

if __name__ == "__main__":
    annotate_video()
