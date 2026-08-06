import librosa
from config import SLOWDOWN_FACTOR

def load_audio(audio_path, slowdown_factor):
    y, sr = librosa.load(audio_path, sr=None)

    if slowdown_factor < 1.0:
        y = librosa.effects.time_stretch(y, rate=slowdown_factor)

    return y, sr
