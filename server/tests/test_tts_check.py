import unittest
from brain.tts_check import transcript_warning

class TranscriptTests(unittest.TestCase):
    def test_apostrophes_case_and_punctuation_match(self):
        self.assertIsNone(transcript_warning("Don't stop, ROCKY!", "don't stop rocky"))

    def test_foreign_and_missing_words_are_reported(self):
        self.assertIn("['hello', 'there']", transcript_warning("stop", "stop hello there"))
        self.assertIn("missing", transcript_warning("one two three four", "one"))
