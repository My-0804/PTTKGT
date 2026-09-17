"""Flask backend kết nối PlaylistManager với giao diện HTML."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from flask import Flask, jsonify, render_template, request

from core_struct import PlaylistManager


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "playlist.json"

app = Flask(__name__)
DATA_FILE.parent.mkdir(exist_ok=True)

playlist = PlaylistManager()
playlist_lock = threading.RLock()


def extract_youtube_id(value: str) -> str | None:
    """Nhận URL YouTube phổ biến hoặc video ID 11 ký tự."""
    value = value.strip()
    if len(value) == 11 and all(char.isalnum() or char in "-_" for char in value):
        return value
    try:
        parsed = urlparse(value if "://" in value else f"https://{value}")
        host = parsed.netloc.lower().split(":")[0]
        host = host[4:] if host.startswith("www.") else host
        video_id = None
        if host == "youtu.be":
            video_id = parsed.path.strip("/").split("/")[0]
        elif host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
            if parsed.path == "/watch":
                video_id = parse_qs(parsed.query).get("v", [None])[0]
            elif parsed.path.startswith(("/shorts/", "/embed/", "/live/")):
                video_id = parsed.path.strip("/").split("/")[1]
        if video_id and len(video_id) == 11 and all(char.isalnum() or char in "-_" for char in video_id):
            return video_id
    except (ValueError, IndexError):
        pass
    return None


def save_playlist() -> None:
    payload = {
        "current_id": playlist.current.song_id if playlist.current else None,
        "songs": playlist.to_dict_list(),
    }
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_playlist() -> None:
    if not DATA_FILE.exists():
        return
    try:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        for song in payload.get("songs", []):
            playlist.add_song(
                song["title"], song["artist"], song.get("youtube_id", ""),
                song.get("duration", 0), song.get("favorite", False), song.get("id")
            )
        if payload.get("current_id"):
            playlist.set_current(payload["current_id"])
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        pass


def response_state(message: str = "", status: int = 200):
    return jsonify({
        "ok": status < 400,
        "message": message,
        "size": playlist.size,
        "current_id": playlist.current.song_id if playlist.current else None,
        "songs": playlist.to_dict_list(),
        "links_valid": playlist.validate_links(),
    }), status


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/songs")
def get_songs():
    keyword = request.args.get("q", "").strip()
    favorites = request.args.get("favorites") == "1"
    with playlist_lock:
        nodes = playlist.search_song(keyword) if keyword else playlist.to_list()
        if favorites:
            nodes = [node for node in nodes if node.favorite]
        return jsonify({
            "ok": True,
            "size": len(nodes),
            "current_id": playlist.current.song_id if playlist.current else None,
            "songs": playlist.to_dict_list(nodes),
        })


@app.post("/api/songs")
def add_song():
    payload = request.get_json(silent=True) or request.form
    title = payload.get("title", "").strip()
    artist = payload.get("artist", "").strip()
    youtube_url = payload.get("youtube_url", "").strip()
    if not title or not artist:
        return response_state("Tên bài hát và ca sĩ không được để trống.", 400)
    youtube_id = extract_youtube_id(youtube_url)
    if not youtube_id:
        return response_state("Liên kết YouTube hoặc video ID không hợp lệ.", 400)
    with playlist_lock:
        try:
            node = playlist.add_song(title, artist, youtube_id)
            save_playlist()
            return jsonify({"ok": True, "message": "Đã thêm bài hát.", "song": node.to_dict(node is playlist.current)}), 201
        except ValueError as error:
            return response_state(str(error), 400)


@app.delete("/api/songs/<song_id>")
def delete_song(song_id):
    with playlist_lock:
        node = playlist.delete_by_id(song_id)
        if not node:
            return response_state("Không tìm thấy bài hát.", 404)
        save_playlist()
        return response_state(f"Đã xóa “{node.title}”.")


@app.post("/api/current/<song_id>")
def set_current(song_id):
    with playlist_lock:
        if not playlist.set_current(song_id):
            return response_state("Không tìm thấy bài hát.", 404)
        save_playlist()
        return response_state()


@app.post("/api/next")
def next_song():
    with playlist_lock:
        playlist.next_song()
        save_playlist()
        return response_state()


@app.post("/api/previous")
def previous_song():
    with playlist_lock:
        playlist.prev_song()
        save_playlist()
        return response_state()


@app.post("/api/shuffle")
def shuffle():
    with playlist_lock:
        playlist.shuffle_playlist()
        save_playlist()
        return response_state("Đã trộn danh sách phát.")


@app.post("/api/songs/<song_id>/favorite")
def favorite(song_id):
    with playlist_lock:
        if not playlist.toggle_favorite(song_id):
            return response_state("Không tìm thấy bài hát.", 404)
        save_playlist()
        return response_state()


@app.post("/api/songs/<song_id>/duration")
def update_duration(song_id):
    with playlist_lock:
        node = playlist.find_by_id(song_id)
        if not node:
            return response_state("Không tìm thấy bài hát.", 404)
        try:
            node.duration = max(0, float(request.json.get("duration", 0)))
        except (TypeError, ValueError, AttributeError):
            return response_state("Thời lượng không hợp lệ.", 400)
        save_playlist()
        return response_state()


load_playlist()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
