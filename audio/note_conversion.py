def notes_to_json(
    notes,
    tempo: float,
    measure_start: float,
    slowdown_factor: float = 1.0,
    min_note_duration: float = 0.05,
):
    clean_notes = []

    for note in notes:
        start = note["start"] / slowdown_factor
        end = note["end"] / slowdown_factor

        duration = max(
            end - start,
            min_note_duration,
        )

        clean_notes.append(
            {
                "p": int(round(note["midi"])),
                "s": float(round(start, 3)),
                "d": float(round(duration, 3)),
            }
        )

    return {
        "tempo": tempo,
        "measure_start": round(measure_start, 3),
        "notes": clean_notes,
    }
