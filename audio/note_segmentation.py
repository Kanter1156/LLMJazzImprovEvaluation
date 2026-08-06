import numpy as np
import librosa


def hz_to_midi_safe(freq_hz):
    if freq_hz is None or np.isnan(freq_hz) or freq_hz <= 0:
        return None

    return float(librosa.hz_to_midi(freq_hz))


def merge_consecutive_notes(notes, pitch_merge_cents: int = 30):
    if not notes:
        return []

    merged = [notes[0]]

    for note in notes[1:]:
        last = merged[-1]

        if abs(note["midi"] - last["midi"]) <= pitch_merge_cents / 100:
            last["end"] = note["end"]
        else:
            merged.append(note)

    return merged


def segment_notes(
    time,
    freq,
    confidence,
    confidence_threshold: float = 0.80,
    pitch_merge_cents: int = 30,
):
    notes = []

    current_pitch = None
    note_start = None

    for t, f, c in zip(time, freq, confidence):
        midi = hz_to_midi_safe(f)

        if c < confidence_threshold or midi is None:
            if current_pitch is not None:
                notes.append(
                    {
                        "midi": current_pitch,
                        "start": note_start,
                        "end": t,
                    }
                )

                current_pitch = None
                note_start = None

            continue

        if current_pitch is None:
            current_pitch = midi
            note_start = t

        elif abs(midi - current_pitch) > pitch_merge_cents / 100:
            notes.append(
                {
                    "midi": current_pitch,
                    "start": note_start,
                    "end": t,
                }
            )

            current_pitch = midi
            note_start = t

    if current_pitch is not None and len(time) > 0:
        notes.append(
            {
                "midi": current_pitch,
                "start": note_start,
                "end": time[-1],
            }
        )

    return merge_consecutive_notes(
        notes,
        pitch_merge_cents,
    )
