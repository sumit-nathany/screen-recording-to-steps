import cv2
import pytesseract
import subprocess
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
VIDEO_PATH = "amazon_steps.mov"   # Change to your video file
SAMPLE_FPS = 4                  # Frames per second to sample
USE_OLLAMA = True               # Set True for offline llama3, False for OpenAI API

# -----------------------------
# STEP 1 - Extract raw OCR text
# -----------------------------
def extract_raw_text(video_path, sample_fps=4):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps // sample_fps) if fps > 0 else 1

    texts = []
    frame_idx = 0
    prev_text = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray, config="--psm 6").strip()

            if text and text[:40] != prev_text[:40]:
                texts.append(text.replace("\n", " "))
                prev_text = text

        frame_idx += 1

    cap.release()
    return texts


# -----------------------------
# STEP 2A - Summarize with Ollama (local llama3)
# -----------------------------
def summarize_with_ollama(ocr_texts):
    raw_text = "\n".join(ocr_texts)

    prompt = (
        "You are an assistant that extracts clear, human-readable steps "
        "from noisy OCR output of a screen recording.\n\n"
        f"Here is the OCR text:\n\n{raw_text}\n\n"
        "Convert this into a numbered list of high-level user actions."
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"⚠️ Ollama summarization failed: {e}")
        return None


# -----------------------------
# STEP 2B - Summarize with OpenAI (fallback if needed)
# -----------------------------
def summarize_with_openai(ocr_texts):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    raw_text = "\n".join(ocr_texts)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts clear, human-readable steps from noisy OCR output of a screen recording."},
                {"role": "user", "content": f"Here is the OCR text:\n\n{raw_text}\n\nConvert this into a numbered list of high-level user actions."},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ OpenAI summarization failed: {e}")
        return None


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("🔍 Extracting OCR text from video...")
    ocr_texts = extract_raw_text(VIDEO_PATH, SAMPLE_FPS)
    print(f"✅ Extracted {len(ocr_texts)} text snippets.")

    # Save raw OCR
    with open("ocr_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ocr_texts))
    print("📂 Saved raw OCR text to ocr_output.txt")

    steps = None
    if USE_OLLAMA:
        print("\n🤖 Summarizing using Ollama (local llama3)...")
        steps = summarize_with_ollama(ocr_texts)
    else:
        print("\n🤖 Summarizing using OpenAI API...")
        steps = summarize_with_openai(ocr_texts)

    if steps:
        print("\n--- High-Level Steps ---\n")
        print(steps)
        with open("steps_output.txt", "w", encoding="utf-8") as f:
            f.write(steps)
        print("📂 Saved summarized steps to steps_output.txt")
    else:
        print("\n❌ Summarization failed. Check logs. Raw OCR still saved in ocr_output.txt.")
