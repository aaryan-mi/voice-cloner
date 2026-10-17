# Voice Cloner 🎙️

An open-source, local zero-shot Text-to-Speech (TTS) and voice cloning studio. Provide 10–20 seconds of clear reference speech to synthesize new audio matching the vocal identity and tone of the speaker.

Developed by **Aaryan Atul Mishra** ([@aaryan-mi](https://github.com/aaryan-mi)).

---

## ✨ Features

- **Zero-Shot Voice Cloning**: Clones timbre, pitch, and vocal cadence from a 10–20 second clean `.wav` or `.mp3` sample.
- **Interactive Web Studio**: Built-in modern browser interface with live microphone recording, audio file upload, and waveform playback.
- **CLI Support**: Simple command-line interface for batch processing and script automation.
- **Robust Audio Pipeline**: Dynamic FFmpeg integration, audio normalization, and silence trimming.
- **Privacy-First**: Runs 100% locally on your machine without third-party cloud APIs or character caps.

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10 or 3.11 recommended.
- Git.

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/aaryan-mi/voice-cloner.git
cd voice-cloner

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

### Web Studio (Recommended)

To launch the web interface:

```bash
python web_app.py
```

Or on Windows, simply double-click `run_web_studio.bat`.

The studio will start at `http://127.0.0.1:7860`. You can:
1. Record directly from your microphone or upload a sample.
2. Enter the text you wish to synthesize.
3. Click **Synthesize Voice** and listen to or download the generated audio.

---

### Command-Line Interface (CLI)

You can also run one-shot synthesis or interactive CLI mode:

```bash
# Direct synthesis
python clone_voice.py --voice sample.wav --text "Hello world! This is my cloned voice." --output output.wav

# Interactive mode
python clone_voice.py --voice sample.wav
```

---

## 📁 Project Structure

```text
voice-cloner/
├── web_app.py             # Web UI studio application (Gradio)
├── clone_voice.py         # CLI voice cloning tool
├── audio_fix.py           # Audio loader & FFmpeg portability layer
├── run_web_studio.bat     # Windows 1-click launcher
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

**Author:** Aaryan Atul Mishra  
**GitHub:** [@aaryan-mi](https://github.com/aaryan-mi)  
**Email:** m.aaryan4094@gmail.com
