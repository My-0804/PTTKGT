from core_struct import PlaylistManager

def run_tests():
    pl = PlaylistManager()
    
    # 1. Test rỗng
    print("Test 1 - Xoa khi rong:", pl.delete_song_by_title("A"))
    print("Test 1 - Validate links:", pl.validate_links())
    
    # 2. Test 1 bài
    pl.add_song("Song 1", "Artist 1")
    pl.current = pl.head
    print("Test 2 - Xoa 1 bai:", pl.delete_song_by_title("song 1"))
    print("Test 2 - Validate links:", pl.validate_links())
    print("Test 2 - current after delete:", pl.current)
    
    # 3. Test xóa đầu, cuối, giữa
    pl.add_song("Song A", "Artist A")
    pl.add_song("Song B", "Artist B")
    pl.add_song("Song C", "Artist C")
    pl.add_song("Song D", "Artist D")
    pl.add_song("Song E", "Artist E")
    
    pl.current = pl.head # Dang nghe Song A
    print("Test 3a - Xoa bai dau (Song A):", pl.delete_song_by_title("song a"))
    print("Test 3a - Validate links:", pl.validate_links())
    print("Test 3a - current sau khi xoa bai dang phat o dau:", pl.current.title if pl.current else None) # Should be Song B
    
    pl.current = pl.tail # Dang nghe Song E
    print("Test 3b - Xoa bai cuoi (Song E):", pl.delete_song_by_title("song e"))
    print("Test 3b - Validate links:", pl.validate_links())
    print("Test 3b - current sau khi xoa bai dang phat o cuoi:", pl.current.title if pl.current else None) # Should be Song D
    
    pl.current = pl.head.next # Dang nghe Song C (B -> C -> D)
    print("Test 3c - Xoa bai o giua (Song C):", pl.delete_song_by_title("song c"))
    print("Test 3c - Validate links:", pl.validate_links())
    print("Test 3c - current sau khi xoa bai dang phat o giua:", pl.current.title if pl.current else None) # Should be Song D
    
    # 4. Test Search
    node, idx = pl.search_song("song d")
    print("Test 4 - Tim kiem 'song d':", f"Found {node.title} at index {idx}" if node else "Not found")
    
    # 5. Test Shuffle
    pl.add_song("Song X", "Artist X")
    pl.add_song("Song Y", "Artist Y")
    pl.add_song("Song Z", "Artist Z")
    print("Before Shuffle:")
    curr = pl.head
    while curr:
        print(f"  {curr.title}")
        curr = curr.next
        
    pl.shuffle_playlist()
    print("After Shuffle:")
    curr = pl.head
    while curr:
        print(f"  {curr.title}")
        curr = curr.next
    print("Test 5 - Validate links after shuffle:", pl.validate_links())

if __name__ == "__main__":
    run_tests()