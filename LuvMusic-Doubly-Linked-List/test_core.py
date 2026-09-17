import unittest

from core_struct import PlaylistManager


class PlaylistManagerTests(unittest.TestCase):
    def setUp(self):
        self.playlist = PlaylistManager()

    def test_rejects_empty_title_or_artist(self):
        with self.assertRaises(ValueError):
            self.playlist.add_song("", "MONO")
        with self.assertRaises(ValueError):
            self.playlist.add_song("Waiting For You", "  ")

    def test_add_search_and_duplicate_title(self):
        self.playlist.add_song("Hello", "A")
        self.playlist.add_song("Hello", "B")
        self.playlist.add_song("Waiting For You", "MONO")
        self.assertEqual(len(self.playlist.search_song("hello")), 2)
        self.assertEqual(len(self.playlist.search_song("mono")), 1)
        self.assertTrue(self.playlist.validate_links())

    def test_delete_requires_title_and_artist(self):
        self.playlist.add_song("Hello", "A")
        self.playlist.add_song("Hello", "B")
        self.assertFalse(self.playlist.delete_song("Hello", "C"))
        self.assertTrue(self.playlist.delete_song("Hello", "A"))
        self.assertEqual(self.playlist.head.artist, "B")

    def test_next_previous_and_delete_current(self):
        first = self.playlist.add_song("A", "X")
        second = self.playlist.add_song("B", "Y")
        third = self.playlist.add_song("C", "Z")
        self.assertIs(self.playlist.next_song(), second)
        self.assertIs(self.playlist.prev_song(), first)
        self.playlist.current = second
        self.playlist.delete_node(second)
        self.assertIs(self.playlist.current, third)
        self.assertTrue(self.playlist.validate_links())

    def test_shuffle_keeps_song_pairs_and_links(self):
        pairs = {(f"Song {i}", f"Artist {i}") for i in range(8)}
        for title, artist in pairs:
            self.playlist.add_song(title, artist)
        self.playlist.shuffle_playlist()
        actual = {(node.title, node.artist) for node in self.playlist.to_list()}
        self.assertEqual(actual, pairs)
        self.assertTrue(self.playlist.validate_links())


if __name__ == "__main__":
    unittest.main(verbosity=2)
