import librosa


def build_chord_timeline(
    chord_text: str,
    tempo: float,
    time_signature: tuple,
    measure_start: float,
    audio_path: str,
):
    y, sr = librosa.load(audio_path, sr=None)
    audio_duration = librosa.get_duration(
        y=y,
        sr=sr,
    )

    beats_per_measure, beat_unit = time_signature

    seconds_per_beat = (
        60.0 / tempo * (4.0 / beat_unit)
    )

    seconds_per_measure = (
        beats_per_measure * seconds_per_beat
    )

    measures = [
        line.strip()
        for line in chord_text.splitlines()
        if line.strip()
    ]

    if not measures:
        return []

    timeline = []

    current_time = measure_start
    end_time = measure_start + audio_duration

    while current_time < end_time:
        for measure in measures:
            chords = measure.split()

            if not chords:
                current_time += seconds_per_measure
                continue

            chord_spacing = (
                seconds_per_measure / len(chords)
            )

            for i, chord in enumerate(chords):
                chord_start = round(
                    current_time + i * chord_spacing,
                    2,
                )

                if chord_start <= end_time:
                    timeline.append(
                        {
                            "c": chord,
                            "s": chord_start,
                        }
                    )

            current_time += seconds_per_measure

            if current_time >= end_time:
                break

    return timeline
