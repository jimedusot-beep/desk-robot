"""Compare a cleaned prompt to the transcription of its synthesized audio."""
import re

def transcript_warning(expected, heard, *, original=None):
    said = set(re.findall(r"[a-z']+", expected.lower()))
    got = set(re.findall(r"[a-z']+", heard.lower()))
    extra = got - said
    if len(extra) >= 3 or (len(extra) >= 2 and len(extra) >= len(got) / 3):
        return f"  !! TTS CHECK: audio contains words not in the text: {sorted(extra)}\n     text : {expected if original is None else original}\n     heard: {heard}"
    if len(said - got) >= max(3, len(said) // 2):
        return f"  !! TTS CHECK: audio is missing much of the text. heard: {heard}"
    return None
