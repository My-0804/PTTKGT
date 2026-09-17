import tempfile
import unittest
from pathlib import Path

import app as webapp
from core_struct import PlaylistManager


class FlaskApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        webapp.DATA_FILE = Path(self.temp.name) / "data" / "playlist.json"
        webapp.DATA_FILE.parent.mkdir(parents=True)
        webapp.playlist = PlaylistManager()
        webapp.app.config.update(TESTING=True)
        self.client = webapp.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def test_complete_api_flow(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"LuvMusic", page.data)

        response = self.client.post("/api/songs", json={
            "title": "Waiting For You",
            "artist": "MONO",
            "youtube_url": "https://www.youtube.com/watch?v=M7lc1UVf-VE",
        })
        self.assertEqual(response.status_code, 201)
        song = response.get_json()["song"]
        song_id = song["id"]
        self.assertEqual(song["youtube_id"], "M7lc1UVf-VE")

        self.assertEqual(self.client.get("/api/songs?q=mono").get_json()["size"], 1)
        self.assertEqual(self.client.post(f"/api/current/{song_id}").status_code, 200)
        self.assertEqual(self.client.post("/api/shuffle").status_code, 200)
        self.assertEqual(self.client.delete(f"/api/songs/{song_id}").status_code, 200)
        self.assertEqual(self.client.get("/api/songs").get_json()["size"], 0)

    def test_youtube_url_formats_and_invalid_url(self):
        self.assertEqual(webapp.extract_youtube_id("https://youtu.be/M7lc1UVf-VE"), "M7lc1UVf-VE")
        self.assertEqual(webapp.extract_youtube_id("https://youtube.com/shorts/M7lc1UVf-VE"), "M7lc1UVf-VE")
        response = self.client.post("/api/songs", json={"title":"A", "artist":"B", "youtube_url":"definitely-invalid"})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
