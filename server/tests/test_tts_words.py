"""Dependency-free regression for the TTS word-set comparison.

Locks the exact regex that caused the F821 missing-import incident. Imports
nothing with third-party dependencies (stdlib + ``brain.tts_words`` only), so it
runs without audio, numpy, or a speech model.
"""

import unittest

from brain.tts_words import word_set


class TtsWordSetTests(unittest.TestCase):
    def test_case_insensitive(self):
        self.assertEqual(word_set("Rocky, Look AT This"), {"rocky", "look", "at", "this"})

    def test_apostrophes_kept_as_word_chars(self):
        self.assertEqual(word_set("I don't think you're wrong"),
                         {"i", "don't", "think", "you're", "wrong"})

    def test_non_word_characters_split_and_drop(self):
        # Hyphens, numbers, punctuation, emoji: none are words under [a-z']+.
        self.assertEqual(word_set("Rocky-2: stop! (he said) — no #@! #"),
                         {"rocky", "stop", "he", "said", "no"})

    def test_empty_and_whitespace(self):
        self.assertEqual(word_set(""), set())
        self.assertEqual(word_set("   \n\t  "), set())

    def test_hallucination_comparison_still_works(self):
        # Mirror check_tts's comparison: strictly greater foreign words, no
        # third-party machinery involved.
        said = word_set("turn left and slow down")
        got_extra = word_set("turn left and slow down hello hello hello") - said
        self.assertEqual(got_extra, {"hello"})
        got_missing = said - word_set("turn left")
        self.assertEqual(got_missing, {"and", "slow", "down"})


if __name__ == "__main__":
    unittest.main()
