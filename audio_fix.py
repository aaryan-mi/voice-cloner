import os
import sys
import glob
import shutil
import subprocess
import tempfile
import torch
import soundfile as sf
import torchaudio
import pydub
import pydub.utils

# 1. Dynamically locate FFmpeg & ffprobe
ffmpeg_exe = shutil.which("ffmpeg")
ffprobe_exe = shutil.which("ffprobe")

if not (ffmpeg_exe and ffprobe_exe):
    # Check common Windows winget / local installations dynamically
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
    
    candidate_dirs = [
        os.path.join(prog_files, "Krita (x64)", "bin")
    ]
    if local_app_data:
        candidate_dirs.extend(glob.glob(os.path.join(local_app_data, "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg*", "*", "bin")))
        candidate_dirs.extend(glob.glob(os.path.join(local_app_data, "Microsoft", "WinGet", "Links")))

    for d in candidate_dirs:
        if os.path.isdir(d):
            f = os.path.join(d, "ffmpeg.exe")
            p = os.path.join(d, "ffprobe.exe")
            if os.path.exists(f) and not ffmpeg_exe:
                ffmpeg_exe = f
            if os.path.exists(p) and not ffprobe_exe:
                ffprobe_exe = p
            if d not in os.environ["PATH"]:
                os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]

# Fallback to imageio_ffmpeg if available
if not ffmpeg_exe:
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        f_dir = os.path.dirname(ffmpeg_exe)
        if f_dir not in os.environ["PATH"]:
            os.environ["PATH"] = f_dir + os.pathsep + os.environ["PATH"]
    except Exception:
        pass

# Configure pydub
if ffmpeg_exe:
    pydub.AudioSegment.converter = ffmpeg_exe
    pydub.utils.get_encoder_name = lambda: ffmpeg_exe
if ffprobe_exe:
    pydub.utils.get_prober_name = lambda: ffprobe_exe

# 2. Patch torchaudio to use soundfile backend with automatic FFmpeg fallback
def custom_load(filepath, **kwargs):
    """Load audio with soundfile instead of failing torchcodec, with automatic FFmpeg fallback."""
    str_path = str(filepath)
    try:
        data, samplerate = sf.read(str_path, dtype="float32")
    except Exception:
        if ffmpeg_exe:
            tmp_wav = tempfile.mktemp(suffix=".wav")
            cmd = [ffmpeg_exe, "-y", "-i", str_path, "-ar", "24000", "-ac", "1", tmp_wav]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            data, samplerate = sf.read(tmp_wav, dtype="float32")
            try:
                os.remove(tmp_wav)
            except OSError:
                pass
        else:
            raise

    tensor = torch.from_numpy(data)
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)
    else:
        tensor = tensor.t()
    return tensor, samplerate

def custom_save(filepath, src, sample_rate, **kwargs):
    """Save audio with soundfile instead of failing torchcodec."""
    if isinstance(src, torch.Tensor):
        src = src.detach().cpu().numpy()
    if src.ndim == 2:
        src = src.T
    sf.write(str(filepath), src, sample_rate)

torchaudio.load = custom_load
torchaudio.save = custom_save
