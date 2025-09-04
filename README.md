# Screen Recording to Steps

This project converts a **screen recording video** into a set of **high-level human-readable steps**.  
It works in two modes:
- **Online**: Uses OpenAI's GPT models.
- **Offline**: Uses a local LLaMA 3 model via [Ollama](https://ollama.ai/).

---

## 🚀 Features
- Extracts text from video frames using **OCR (Tesseract + OpenCV)**  
- Summarizes noisy OCR text into **clean, high-level steps**  
- Supports both **OpenAI GPT (online)** and **LLaMA 3 via Ollama (offline)**  

---

## 🖥️ Requirements
- macOS (tested on Apple Silicon)  
- Python 3.9+  
- [Tesseract OCR](https://tesseract-ocr.github.io/)  
- [Ollama](https://ollama.ai) (for offline summarization)  

## 🛠️ Setup Instructions

### 1. Install Python Dependencies
Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. 📦 Install Tesseract (OCR)
On macOS, install via Homebrew:

```bash
brew install tesseract
```

### 3. 🦙 Install Ollama (for Offline Mode)
Download and install Ollama for macOS from:
👉 https://ollama.ai/download

After installation, pull the LLaMA 3 model:

```bash
ollama pull llama3:8b
```

Verify installation:

```bash
ollama run llama3 "Hello"
```

### 4. 🔑 Environment Variables (for Online Mode)
If you want to use OpenAI instead of local models, set your API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## ▶️ Usage

Run the script on a sample video:

```bash
python main.py --video sample.mp4 --mode offline
```

The output will be saved as `steps.txt`.

## 📋 Example Output
For a recording of browsing Amazon and adding an item to the cart, the generated steps might look like:

```
1. Open Amazon India website
2. Search for "Samsung Galaxy Tablet"
3. Click on a docking station product
4. View product details
5. Add item to cart
```