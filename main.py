import cv2
import pytesseract
from pytesseract import Output

# Path to your video (update filename if needed)
VIDEO_PATH = "amazon_steps.mov"

# Frames per second for sampling
SAMPLE_FPS = 4

def extract_steps(video_path, sample_fps=4):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps // sample_fps) if fps > 0 else 1

    steps = []
    prev_text = ""

    frame_idx = 0
    step_count = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % interval == 0:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # OCR
            text = pytesseract.image_to_string(gray, config="--psm 6").strip()

            # If screen text changes significantly, treat as new step
            if text and text[:40] != prev_text[:40]:
                clean_text = text.replace("\n", " ")
                steps.append(f"{step_count}. {clean_text}")
                step_count += 1
                prev_text = text

        frame_idx += 1

    cap.release()
    return steps

if __name__ == "__main__":
    steps = extract_steps(VIDEO_PATH, SAMPLE_FPS)
    print("\n--- High-level Steps ---\n")
    for s in steps:
        print(s)
