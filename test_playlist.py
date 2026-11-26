"""Unit tests for the Playlist Manager (run with: python -m unittest)."""
import unittest

from playlist import Playlist, Song


class TestSong(unittest.TestCase):
    def test_duration_str(self):
        self.assertEqual(Song("X", "A", 215).duration_str(), "3:35")

    def test_duration_str_pads_seconds(self):
        self.assertEqual(Song("X", "A", 61).duration_str(), "1:01")


class TestPlaylist(unittest.TestCase):
    def setUp(self):
        self.pl = Playlist("Chill Mix")
        self.pl.add_song(Song("Ocean Eyes", "Billie Eilish", 200))
        self.pl.add_song(Song("Blinding Lights", "The Weeknd", 200))
        self.pl.add_song(Song("Lofi Beat", "Chill Guy", 95))

    def test_add_song(self):
        self.assertEqual(len(self.pl.songs), 3)

    def test_add_negative_duration_raises(self):
        with self.assertRaises(ValueError):
            self.pl.add_song(Song("Bad", "X", -5))

    def test_total_duration(self):
        self.assertEqual(self.pl.total_duration_sec(), 495)
        self.assertEqual(self.pl.total_duration_str(), "8:15")

    def test_by_artist_case_insensitive(self):
        self.assertEqual(len(self.pl.by_artist("billie eilish")), 1)
        self.assertEqual(len(self.pl.by_artist("Unknown Artist")), 0)

    def test_sorted_by_duration(self):
        ordered = [s.duration_sec for s in self.pl.sorted_by_duration()]
        self.assertEqual(ordered, [95, 200, 200])

    def test_to_json(self):
        data = self.pl.to_json()
        self.assertIn('"title": "Ocean Eyes"', data)
        self.assertIn('"duration_sec": 200', data)


if __name__ == "__main__":
    unittest.main()
