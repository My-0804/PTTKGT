import random
#cau truc du lieu
class Node:
    def __init__(self, title: str, artist: str):
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

    def is_empty(self) -> bool:
        return self.size == 0

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

    def delete_song(self, title: str, artist: str) -> bool:
        curr = self.head
        while curr:
            if curr.title == title and curr.artist == artist:
                if curr == self.current:
                    self.current = curr.next if curr.next else curr.prev
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next

                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev

                self.size -= 1
                return True
            curr = curr.next
        return False

    def search_song(self, keyword: str) -> list:
        """Tim theo Ten bai hat HOAC Ca si, tra ve danh sach cac Node"""
        results = []
        curr = self.head
        keyword_lower = keyword.lower()
        while curr:
            if keyword_lower in curr.title.lower() or keyword_lower in curr.artist.lower():
                results.append(curr)
            curr = curr.next
        return results

    def shuffle_playlist(self):
        if self.size <= 1:
            return
#thu thap danh sach cap (title, artist)
        pairs = []
        curr = self.head
        while curr:
            pairs.append((curr.title, curr.artist))
            curr = curr.next

#xoa tron danh sach (giu nguyen tung cap title - artist)
        random.shuffle(pairs)

#gan gia tri
        curr = self.head
        for title, artist in pairs:
            curr.title = title
            curr.artist = artist
            curr = curr.next
#Giao dien vs dieu khien

def get_non_empty_string(prompt: str) -> str:
    """Ngan nguoi dung bo trong hoac chi bam Enter"""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Loi: Du lieu khong duoc de trong! Vui long nhap lai.")

def get_valid_choice(min_choice: int, max_choice: int) -> int:
    """Ngan loi nhap chu thay vi so hoac nhap so ngoai pham vi Menu"""
    while True:
        try:
            choice = int(input(f"Bam chon chuc nang ({min_choice} - {max_choice}): "))
            if min_choice <= choice <= max_choice:
                return choice
            else:
                print(f"Loi: Luachon nam ngoai pham vi ({min_choice} - {max_choice}). Chon lai!")
        except ValueError:
            print("Loi: Dau vao phai la so nguyen! Vui long nhap lai.")

def display_menu(manager: PlaylistManager):
    """Hien thi giao dien man hinh Console"""
    print("\n=============================================")
    print("      HE THONG QUAN LY MUSIC PLAYLIST        ")
    print("=============================================")

    if manager.current and not manager.is_empty():
        current_song = f"{manager.current.title} - {manager.current.artist}"
    else:
        current_song = "Khong co"
    print(f" Dang phat: [{current_song}]")
    print(f" Tong so bai hat: {manager.size}")
    print("---------------------------------------------")
    print("1. Them bai hat moi (Add): nhap Ten bai hat va Ca si")
    print("2. Xoa bai hat (Delete): nhap Ten bai hat va Ca si")
    print("3. Tim kiem (Search): tim theo Ten bai hat hoac Ca si")
    print("4. Phat bai ke tiep (Next)")
    print("5. Phat bai truoc do (Previous)")
    print("6. Tron bai ngau nhien (Shuffle)")
    print("7. Hien thi toan bo Danh sach phat")
    print("0. Thoat chuong trinh")
    print("=============================================")

def main_cli(manager: PlaylistManager):
    """Vong lap duy tri dieu khien chuong trinh"""
    while True:
        display_menu(manager)
        choice = get_valid_choice(0, 7)

        if choice == 1:
            print("\n--- THEM BAI HAT MOI ---")
            title = get_non_empty_string("Nhap ten bai hat: ")
            artist = get_non_empty_string("Nhap ten ca si: ")
            manager.add_song(title, artist)
            print(f" Da them bai hat '{title} - {artist}' vao danh sach.")

        elif choice == 2:
            print("\n--- XOA BAI HAT ---")
            if manager.is_empty():
                print(" Danh sach dang rong, khong the xoa!")
            else:
                title = get_non_empty_string("Nhap ten bai hat can xoa: ")
                artist = get_non_empty_string("Nhap ten ca si can xoa: ")
                if manager.delete_song(title, artist):
                    print(f" Da xoa thanh cong bai hat '{title} - {artist}'.")
                else:
                    print(f" Khong tim thay bai hat '{title} - {artist}' trong danh sach.")

        elif choice == 3:
            print("\n--- TIM KIEM BAI HAT ---")
            if manager.is_empty():
                print(" Danh sach dang rong!")
            else:
                keyword = get_non_empty_string("Nhap ten bai hat hoac ca si can tim: ")
                results = manager.search_song(keyword)
                if results:
                    print(f" Ket qua tim kiem cho '{keyword}':")
                    for i, song in enumerate(results, start=1):
                        print(f"   {i}. {song.title} - {song.artist}")
                else:
                    print(f" Khong tim thay bai hat hoac ca si phu hop voi '{keyword}'.")

        elif choice == 4:
            print("\n--- CHUYEN BAI KE TIEP (NEXT) ---")
            if manager.is_empty():
                print(" Danh sach rong!")
            elif manager.current and manager.current.next:
                manager.current = manager.current.next
                print(f" Dang phat: {manager.current.title} - {manager.current.artist}")
            else:
                print(" Da o bai hat cuoi cung trong danh sach.")

        elif choice == 5:
            print("\n--- QUAY LAI BAI TRUOC (PREVIOUS) ---")
            if manager.is_empty():
                print(" Danh sach rong!")
            elif manager.current and manager.current.prev:
                manager.current = manager.current.prev
                print(f" Dang phat: {manager.current.title} - {manager.current.artist}")
            else:
                print(" Da o bai hat dau tien trong danh sach.")

        elif choice == 6:
            print("\n--- TRON BAI NGAU NHIEN (SHUFFLE) ---")
            if manager.is_empty():
                print(" Danh sach rong, khong the shuffle!")
            else:
                manager.shuffle_playlist()
                print(" Da xao tron danh sach phat thanh cong!")

        elif choice == 7:
            print("\n--- TOAN BO DANH SACH PHAT ---")
            if manager.is_empty():
                print(" Danh sach hien tai dang rong!")
            else:
                curr = manager.head
                idx = 1
                while curr:
                    prefix = "-> " if curr == manager.current else "   "
                    print(f"{prefix}{idx}. {curr.title} - {curr.artist}")
                    curr = curr.next
                    idx += 1

        elif choice == 0:
            print("\n Cam on ban da su dung chuong trinh Music Playlist Manager. Tam biet!")
            break

if __name__ == "__main__":
    playlist = PlaylistManager()
    main_cli(playlist)