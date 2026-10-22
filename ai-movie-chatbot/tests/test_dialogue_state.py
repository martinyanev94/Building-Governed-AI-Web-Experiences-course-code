import unittest

from src.dialogue_state import DialogueState, ParsedRequest, advance


class DialogueStateTests(unittest.TestCase):
    def test_missing_genre_is_preserved_as_pending(self):
        state, response = advance(
            DialogueState(), ParsedRequest(intent="recommend_movie")
        )

        self.assertEqual(state.intent, "recommend_movie")
        self.assertEqual(state.genre, None)
        self.assertEqual(state.pending_field, "genre")
        self.assertEqual(response, "What genre would you like?")

    def test_follow_up_fills_pending_genre(self):
        state, _ = advance(
            DialogueState(), ParsedRequest(intent="recommend_movie")
        )
        state, response = advance(state, ParsedRequest(genre="comedy"))

        self.assertEqual(state.intent, "recommend_movie")
        self.assertEqual(state.genre, "comedy")
        self.assertIsNone(state.pending_field)
        self.assertIn("comedy", response)

    def test_unknown_request_uses_safe_fallback(self):
        state, response = advance(DialogueState(), ParsedRequest())

        self.assertEqual(state.intent, None)
        self.assertIn("Tell me a genre", response)


if __name__ == "__main__":
    unittest.main()
