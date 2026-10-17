"""
Voice Cloner - Zero-Shot Text-to-Speech Studio
Author: Aaryan Atul Mishra (https://github.com/aaryan-mi)
"""

import os
import sys
from pathlib import Path
from datetime import datetime

import audio_fix
import gradio as gr
from f5_tts.api import F5TTS

print("[*] Initializing Voice Cloning Engine...")
tts_engine = F5TTS(device="cpu")
print("[+] Model loaded successfully!")

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

DEFAULT_VOICE_FILE = "voice_profile.wav"

def get_default_voice():
    if os.path.exists(DEFAULT_VOICE_FILE):
        return DEFAULT_VOICE_FILE
    if os.path.exists("voice_sample.wav"):
        return "voice_sample.wav"
    return None

def clone_and_speak(ref_audio, text_to_speak, save_as_permanent, speed=1.2, steps=16):
    if not ref_audio:
        raise gr.Error("Please record or upload a sample of your reference voice first!")
    if not text_to_speak or not text_to_speak.strip():
        raise gr.Error("Please enter the text you want the voice to speak!")

    # Persist reference audio if enabled
    if save_as_permanent and ref_audio:
        try:
            import shutil
            if os.path.abspath(ref_audio) != os.path.abspath(DEFAULT_VOICE_FILE):
                shutil.copyfile(ref_audio, DEFAULT_VOICE_FILE)
            print("[+] Voice saved as default profile.")
        except Exception as e:
            print(f"[!] Warning: Could not save default profile: {e}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = str(output_dir / f"cloned_{timestamp}.wav")

    print(f"[*] Synthesizing: '{text_to_speak}' (speed={speed}, steps={steps})")

    wav, sr, _ = tts_engine.infer(
        ref_file=ref_audio,
        ref_text="",
        gen_text=text_to_speak.strip(),
        speed=float(speed),
        nfe_step=int(steps),
        remove_silence=True,
        file_wave=out_path
    )

    return out_path

custom_css = """
.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.header-box {
    text-align: center;
    margin-bottom: 24px;
}
"""

with gr.Blocks(title="Voice Cloner Studio", css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎙️ Voice Cloner Studio
        **Zero-Shot Neural Text-to-Speech & Voice Cloning System**
        
        Record or upload 10–20 seconds of clear speech, enter your text, and synthesize speech matching the reference voice profile.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            has_saved = get_default_voice() is not None
            gr.Markdown("### 1. Reference Voice Sample")
            if has_saved:
                gr.Markdown("🟢 *Default reference voice profile detected.*")

            ref_audio_input = gr.Audio(
                label="Voice Sample (Upload or Record via Microphone)",
                type="filepath",
                value=get_default_voice(),
                sources=["microphone", "upload"]
            )
            save_perm_checkbox = gr.Checkbox(
                label="Save as default voice profile",
                value=True
            )

            with gr.Accordion("Synthesis Parameters", open=False):
                speed_slider = gr.Slider(minimum=0.8, maximum=1.6, value=1.2, step=0.05, label="Speech Speed")
                steps_slider = gr.Slider(minimum=8, maximum=32, value=16, step=4, label="Inference Steps")

        with gr.Column(scale=1):
            gr.Markdown("### 2. Speech Synthesis")
            gen_text_input = gr.Textbox(
                label="Text to Speak",
                placeholder="Enter text to synthesize...",
                value="Hello, this is a test of the zero-shot voice cloning studio.",
                lines=5
            )
            generate_btn = gr.Button("✨ Synthesize Voice", variant="primary", size="lg")

            gr.Markdown("### 3. Generated Audio")
            audio_output = gr.Audio(label="Output Speech", type="filepath")

    generate_btn.click(
        fn=clone_and_speak,
        inputs=[ref_audio_input, gen_text_input, save_perm_checkbox, speed_slider, steps_slider],
        outputs=audio_output
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    print(f"[*] Starting Voice Cloner Studio on http://127.0.0.1:{port}")
    demo.launch(server_name="127.0.0.1", server_port=port, inbrowser=True)
