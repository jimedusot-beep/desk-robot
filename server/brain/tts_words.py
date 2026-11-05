"""Shared word_set for the TTS hallucination check (imports cleanly, stdlib-only).

The regex is the exact pattern that caused the F821 incident (missing ``re``
import inside a lambda inside ``check_tts``); keep it dependency-free and unit
tested so it can be exercised without audio, numpy, or a model.
"""

from __future__ import annotations

import re

_WORD_RE = re.compile(r"[a-z']+")


def word_set(text: str) -> set[str]:
    """Lowercase word occurrences in ``text`` as a set (apostrophes kept)."""
    return set(_WORD_RE.findall(text.lower()))
