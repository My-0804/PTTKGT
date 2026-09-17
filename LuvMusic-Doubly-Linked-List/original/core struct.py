# ==============================================================================
# FILE: core_struct.py
# ==============================================================================
import random

class Node:
    def __init__(self, title: str, artist: str):

        if title == "" or artist == "":
            raise ValueError("Ten bai hat va ca si khong duoc de trong!")

        self.title = title
        self.artist = artist
        self.next = None
        self.prev = None


class PlaylistManager:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def add_song(self, title: str, artist: str):
        new_node = Node(title, artist)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.size += 1

    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return True
        return False

    def prev_song(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return True
        return False

    def delete_song_by_title(self, title: str):
        if self.is_empty():
            return False

        curr = self.head
        while curr:

            if curr.title.lower() == title.lower():
 
                if self.size == 1:
                    self.head = None
                    self.tail = None
                    if self.current == curr:
                        self.current = None

                elif curr == self.head:
                    self.head = curr.next
                    self.head.prev = None
                    if self.current == curr:
                        self.current = self.head
                elif curr == self.tail:
                    self.tail = curr.prev
                    self.tail.next = None
                    if self.current == curr:
                        self.current = self.tail
                else:
                    curr.prev.next = curr.next
                    curr.next.prev = curr.prev
                    if self.current == curr:
                        self.current = curr.next

                self.size -= 1
                return True
            curr = curr.next

        return False

    def validate_links(self):
        if self.is_empty():
            return self.head is None and self.tail is None

        # Kiểm tra con trỏ đầu và cuối
        if self.head.prev is not None or self.tail.next is not None:
            return False

        # Đếm thực tế số Node
        count = 0
        curr = self.head
        while curr:
            count += 1
            curr = curr.next

        return count == self.size

    def search_song(self, title: str):
        if self.is_empty():
            return None
            
        curr = self.head
        index = 0
        while curr:
            if curr.title.lower() == title.lower():
                return curr, index
            curr = curr.next
            index += 1
            
        return None

    def shuffle_playlist(self):
        if self.size < 2:
            return
            
        nodes = []
        curr = self.head
        while curr:
            nodes.append(curr)
            curr = curr.next
            
        random.shuffle(nodes)
        
        self.head = nodes[0]
        self.tail = nodes[-1]
        
        for i in range(len(nodes)):
            nodes[i].prev = nodes[i - 1] if i > 0 else None
            nodes[i].next = nodes[i + 1] if i < len(nodes) - 1 else None

    def print_playlist(self):
        if self.is_empty():
            print("-> Danh sach rong!")
            return
        curr = self.head
        i = 1
        print("\n--- DANH SACH PHAT NHAC ---")
        while curr:
            if curr == self.current:
                print(f"{i}. {curr.title} - {curr.artist}  <== [DANG PHAT]")
            else:
                print(f"{i}. {curr.title} - {curr.artist}")
            curr = curr.next
            i += 1

# --- CHƯƠNG TRÌNH CHÍNH (MENU) ---
def main():
    my_music = PlaylistManager()
    my_music.add_song("Bai hat 1", "Ca si A")
    my_music.add_song("Bai hat 2", "Ca si B")
    my_music.add_song("Bai hat 3", "Ca si C")

    while True:
        print("\n=== QUAN LY PLAYLIST ===")
        print("1. Xem danh sach bai hat")
        print("2. Them bai hat moi")
        print("3. Next (Bai tiep)")
        print("4. Prev (Bai truoc)")
        print("5. Xoa bai hat")
        print("6. Tim kiem bai hat")
        print("7. Xao tron danh sach")
        print("0. Thoat")
        
        try:
            chon = int(input("Chon chuc nang (0-7): "))
        except ValueError:
            print("Vui long nhap so!")
            continue

        if chon == 1:
            my_music.print_playlist()
        elif chon == 2:
            title = input("Nhap ten bai hat: ")
            artist = input("Nhap ten ca si: ")
            try:
                my_music.add_song(title, artist)
                print("-> Da them bai hat thanh cong!")
            except ValueError as e:
                print("-> Loi:", e)
        elif chon == 3:
            if my_music.next_song():
                print("-> Dang phat:", my_music.current.title)
            else:
                print("-> Da den bai cuoi cung (hoac danh sach rong)!")
        elif chon == 4:
            if my_music.prev_song():
                print("-> Dang phat:", my_music.current.title)
            else:
                print("-> Dang o bai dau tien (hoac danh sach rong)!")
        elif chon == 5:
            title = input("Nhap ten bai hat can xoa: ")
            if my_music.delete_song_by_title(title):
                print(f"-> Da xoa bai hat '{title}'!")
            else:
                print("-> Khong tim thay bai hat nay trong danh sach!")
        elif chon == 6:
            title = input("Nhap ten bai hat can tim: ")
            result = my_music.search_song(title)
            if result:
                node, idx = result
                print(f"-> Tim thay '{node.title} - {node.artist}' tai vi tri so {idx + 1}.")
            else:
                print(f"-> Khong tim thay '{title}' trong danh sach.")
        elif chon == 7:
            my_music.shuffle_playlist()
            print("-> Da xao tron danh sach phat thanh cong!")
        elif chon == 0:
            print("Tam biet!")
            break
        else:
            print("Loi, yeu cau nhap lai!")

if __name__ == "__main__":
    main()