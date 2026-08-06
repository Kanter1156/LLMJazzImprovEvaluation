from openai import OpenAI

from audio.load_audio import load_audio
from audio.pitch_extraction import extract_pitch
from audio.note_segmentation import segment_notes
from audio.note_conversion import notes_to_json
from harmony.chord_timeline import build_chord_timeline
from llm.analyze import analyze_solo


AUDIO_PATH = "examples/example.wav"
CHORD_FILE = "examples/chords.txt"


TEMPO = 120
TIME_SIGNATURE = (4, 4)
MEASURE_START = 0
SLOWDOWN_FACTOR = 0.6


with open(CHORD_FILE) as f:
    chord_text = f.read()


y, sr = load_audio(
    AUDIO_PATH,
    SLOWDOWN_FACTOR,
)

time, freq, confidence = extract_pitch(
    y,
    sr,
)

notes = segment_notes(
    time,
    freq,
    confidence,
)

note_json = notes_to_json(
    notes,
    TEMPO,
    MEASURE_START,
    SLOWDOWN_FACTOR,
)


timeline = build_chord_timeline(
    chord_text,
    TEMPO,
    TIME_SIGNATURE,
    MEASURE_START,
    AUDIO_PATH,
)


client = OpenAI()

analysis = analyze_solo(
    client,
    note_json,
    chord_text,
    {
        "instrument": "Unknown",
        "tempo": TEMPO,
        "time_signature": "4/4",
        "measure_start": MEASURE_START,
        "chord_timeline": timeline,
    },
)


print(analysis)
