import json
import re
from pathlib import Path

from openai import OpenAI


PROMPT_PATH = Path(__file__).parent / "prompt.txt"


def extract_json(text: str):
    if not text:
        return "{}"

    text = text.strip()

    text = re.sub(
        r"```(?:json)?",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL,
    )

    if match:
        return match.group(0)

    return "{}"


def load_prompt():
    return PROMPT_PATH.read_text()


def analyze_solo(
    client: OpenAI,
    transcribed_solo_text: dict,
    chord_text: str,
    metadata: dict,
):
    prompt = load_prompt().format(
        transcribed_solo_text=transcribed_solo_text,
        chord_text=chord_text,
        instrument=metadata.get("instrument"),
        tempo=metadata.get("tempo"),
        time_signature=metadata.get("time_signature"),
        measure_start=metadata.get("measure_start"),
        chord_timeline=metadata.get("chord_timeline"),
    )

    try:
        response = client.responses.create(
            model="google/gemma-3-12b-it",
            input=prompt,
            temperature=0.4,
        )

        raw = ""

        if getattr(response, "output", None):
            for item in response.output:
                if getattr(item, "type", None) == "message":
                    for content in item.content:
                        if getattr(content, "type", None) == "output_text":
                            raw += content.text

        parsed = json.loads(
            extract_json(raw)
        )

    except Exception:
        parsed = {
            "phrase_structure": "",
            "harmonic_alignment": "",
            "motif_building": "",
            "actionable_feedback": "",
        }

    return {
        "phrase_structure": parsed.get(
            "phrase_structure",
            "",
        ),
        "harmonic_alignment": parsed.get(
            "harmonic_alignment",
            "",
        ),
        "motif_building": parsed.get(
            "motif_building",
            "",
        ),
        "actionable_feedback": parsed.get(
            "actionable_feedback",
            "",
        ),
    }
