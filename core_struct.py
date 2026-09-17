"""Cấu trúc dữ liệu Doubly Linked List cho Music Playlist Manager."""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    """Mỗi Node lưu một bài hát và hai liên kết prev/next."""

    title: str
    artist: str
    youtube_id: str = ""
    duration: float = 0
    favorite: bool = False
    song_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    next: Optional["Node"] = field(default=None, repr=False)
    prev: Optional["Node"] = field(default=None, repr=False)

    def __post_init__(self):
        self.title = self.title.strip()
        self.artist = self.artist.strip()
        if not self.title or not self.artist:
            raise ValueError("Tên bài hát và ca sĩ không được để trống!")

    def to_dict(self, current: bool = False) -> dict:
        return {
            "id": self.song_id,
            "title": self.title,
            "artist": self.artist,
            "youtube_id": self.youtube_id,
            "youtube_url": f"https://www.youtube.com/watch?v={self.youtube_id}" if self.youtube_id else "",
            "thumbnail": f"https://i.ytimg.com/vi/{self.youtube_id}/mqdefault.jpg" if self.youtube_id else "",
            "duration": self.duration,
            "favorite": self.favorite,
            "current": current,
        }


class PlaylistManager:
    """Quản lý playlist bằng danh sách liên kết đôi."""

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.current: Optional[Node] = None
        self.size = 0

    def is_empty(self) -> bool:
        return self.head is None

    def add_song(
        self,
        title: str,
        artist: str,
        youtube_id: str = "",
        duration: float = 0,
        favorite: bool = False,
        song_id: Optional[str] = None,
    ) -> Node:
        new_node = Node(
            title=title,
            artist=artist,
            youtube_id=youtube_id,
            duration=duration,
            favorite=favorite,
            song_id=song_id or uuid.uuid4().hex,
        )
        if self.is_empty():
            self.head = self.tail = self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1
        return new_node

    def find_by_id(self, song_id: str) -> Optional[Node]:
        curr = self.head
        while curr:
            if curr.song_id == song_id:
                return curr
            curr = curr.next
        return None

    def delete_song(self, title: str, artist: str) -> bool:
        """Xóa đúng Node có đồng thời title và artist tương ứng."""
        curr = self.head
        while curr:
            if curr.title.casefold() == title.strip().casefold() and curr.artist.casefold() == artist.strip().casefold():
                return self.delete_node(curr)
            curr = curr.next
        return False

    def delete_by_id(self, song_id: str) -> Optional[Node]:
        node = self.find_by_id(song_id)
        return node if node and self.delete_node(node) else None

    def delete_node(self, node: Node) -> bool:
        if not node:
            return False
        replacement = node.next or node.prev
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        if self.current is node:
            self.current = replacement
        node.prev = node.next = None
        self.size -= 1
        return True

    def search_song(self, keyword: str) -> list[Node]:
        """Tìm gần đúng theo tên bài hát hoặc ca sĩ, không phân biệt hoa thường."""
        term = keyword.strip().casefold()
        results = []
        curr = self.head
        while curr:
            if term in curr.title.casefold() or term in curr.artist.casefold():
                results.append(curr)
            curr = curr.next
        return results

    def set_current(self, song_id: str) -> Optional[Node]:
        node = self.find_by_id(song_id)
        if node:
            self.current = node
        return node

    def next_song(self, wrap: bool = True) -> Optional[Node]:
        if not self.current:
            self.current = self.head
        elif self.current.next:
            self.current = self.current.next
        elif wrap:
            self.current = self.head
        return self.current

    def prev_song(self, wrap: bool = True) -> Optional[Node]:
        if not self.current:
            self.current = self.tail
        elif self.current.prev:
            self.current = self.current.prev
        elif wrap:
            self.current = self.tail
        return self.current

    def shuffle_playlist(self) -> None:
        """Trộn các Node rồi nối lại prev/next, không tách cặp title–artist."""
        if self.size <= 1:
            return
        nodes = self.to_list()
        random.shuffle(nodes)
        self.head, self.tail = nodes[0], nodes[-1]
        for index, node in enumerate(nodes):
            node.prev = nodes[index - 1] if index > 0 else None
            node.next = nodes[index + 1] if index < len(nodes) - 1 else None

    def toggle_favorite(self, song_id: str) -> Optional[Node]:
        node = self.find_by_id(song_id)
        if node:
            node.favorite = not node.favorite
        return node

    def to_list(self) -> list[Node]:
        nodes = []
        curr = self.head
        while curr:
            nodes.append(curr)
            curr = curr.next
        return nodes

    def to_dict_list(self, nodes: Optional[list[Node]] = None) -> list[dict]:
        return [node.to_dict(node is self.current) for node in (nodes if nodes is not None else self.to_list())]

    def validate_links(self) -> bool:
        if self.is_empty():
            return self.head is None and self.tail is None and self.size == 0
        if self.head.prev is not None or self.tail.next is not None:
            return False
        count = 0
        previous = None
        curr = self.head
        while curr:
            if curr.prev is not previous:
                return False
            previous = curr
            curr = curr.next
            count += 1
        return previous is self.tail and count == self.size
