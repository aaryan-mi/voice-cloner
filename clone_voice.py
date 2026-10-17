"""
Voice Cloner CLI - Command-Line Interface for Zero-Shot Voice Synthesis
Author: Aaryan Atul Mishra (https://github.com/aaryan-mi)
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

import audio_fix
import soundfile as sf
from f5_tts.api import F5TTS

def find_default_voice_sample():
    """Locate common voice reference file names in current working directory."""
    candidates = [
        "voice_profile.wav", "voice_sample.wav", "reference.wav",
        "voice_profile.mp3", "voice_sample.mp3", "reference.mp3"
    ]
    for name in candidates:
        if os.path.exists(name):
            return name
    return None

def main():
    parser = argparse.ArgumentParser(description="Zero-Shot Voice Cloner & TTS CLI")
    parser.add_argument("--voice", "-v", type=str, default=None, help="Path to reference audio file (.wav or .mp3)")
    parser.add_argument("--text", "-t", type=str, default=None, help="Text to synthesize in reference voice")
    parser.add_argument("--output", "-o", type=str, default=None, help="Path for output audio file")
    parser.add_argument("--steps", "-s", type=int, default=16, help="Inference steps (default: 16)")
    parser.add_argument("--speed", type=float, default=1.2, help="Playback speed multiplier (default: 1.2)")
    args = parser.parse_args()

    voice_path = args.voice or find_default_voice_sample()
    if not voice_path or not os.path.exists(voice_path):
        print("\n" + "=" * 60)
        print("  [!] Reference Voice Audio Not Found")
        print("=" * 60)
        print("Please provide a 10-20 second audio sample:")
        print("Usage: python clone_voice.py --voice sample.wav --text \"Your text here\"")
        print("=" * 60 + "\n")
        sys.exit(1)

    print(f"[*] Reference Voice: {voice_path}")
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    print("[*] Loading Neural Voice Model...")
    model = F5TTS(device="cpu")
    print("[+] Model ready.")

    while True:
        if args.text:
            gen_text = args.text
        else:
            print("\n" + "-" * 50)
            gen_text = input("[?] Enter text to synthesize (or 'q' to quit): ").strip()
            if not gen_text or gen_text.lower() in ("q", "quit", "exit"):
                print("[*] Exiting.")
                break

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = args.output or str(output_dir / f"cloned_{timestamp}.wav")

        print(f"[*] Synthesizing: \"{gen_text}\" (steps={args.steps}, speed={args.speed})")
        wav, sr, _ = model.infer(
            ref_file=voice_path,
            ref_text="",
            gen_text=gen_text,
            nfe_step=args.steps,
            speed=args.speed,
            remove_silence=True,
            file_wave=out_file
        )

        print(f"[+] Output saved: {out_file} ({sr} Hz)")
        if args.text:
            break

if __name__ == "__main__":
    main()
