import crepe
from scipy.signal import medfilt

def extract_pitch(y, sr, step_ms):
    time, freq, conf, _ = crepe.predict(
        y,
        sr,
        model_capacity="small",
        step_size=step_ms,
        viterbi=True,
    )

    freq = medfilt(freq, kernel_size=3)

    return time, freq, conf
