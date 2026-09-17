# LUVMUSIC – MUSIC PLAYLIST MANAGER

Đây là phiên bản YouTube-only xây dựng từ đề tài Python ban đầu. Thuật toán chính vẫn nằm trong Python; HTML/JavaScript không thay thế Doubly Linked List.

## 1. Chạy trên Windows

1. Cài Python 3.10 trở lên và đánh dấu **Add Python to PATH**.
2. Giải nén dự án.
3. Nhấp đúp `run.bat`.
4. Trình duyệt sẽ tự mở tại `http://localhost:5000`. Nếu chưa mở, hãy nhập địa chỉ này vào Chrome hoặc Edge.

Có thể chạy thủ công:

```bash
python -m pip install -r requirements.txt
python app.py
```

Lưu ý: không mở trực tiếp `templates/index.html`, vì giao diện cần Flask xử lý API và đường dẫn âm thanh.

## 2. Cấu trúc dự án

```text
LuvMusic-Doubly-Linked-List/
├── app.py                 # Flask API – cầu nối Python và HTML
├── core_struct.py         # Node và PlaylistManager (Doubly Linked List)
├── templates/index.html   # Giao diện trình phát nhạc
├── static/app.js          # Gọi Flask API và điều khiển YouTube Player
├── static/style.css       # Thiết kế giao diện
├── static/youtube.css     # Kiểu hiển thị trình phát YouTube
├── data/playlist.json     # Lưu thông tin playlist
├── original/              # Ba file Python gốc để đối chiếu
├── test_core.py           # Kiểm thử cấu trúc dữ liệu
├── test_api.py            # Kiểm thử kết nối Flask
├── run.bat                # Chạy nhanh trên Windows
└── run.sh                 # Chạy nhanh trên Linux/macOS
```

## 3. Luồng kết nối Python với HTML

```text
Người dùng bấm nút trên HTML
          ↓
JavaScript gửi HTTP request bằng fetch()
          ↓
Flask app.py nhận request
          ↓
PlaylistManager trong core_struct.py xử lý Node/prev/next
          ↓
Flask trả JSON → JavaScript cập nhật giao diện và YouTube Player
```

Ví dụ, khi nhấn **Bài tiếp theo**, JavaScript gửi `POST /api/next`. Flask gọi `playlist.next_song()`, con trỏ `current` chuyển sang `current.next`, sau đó bài mới được trả về giao diện.

## 4. Chức năng đã hoàn thành

- Thêm bài hát bằng title, artist và liên kết YouTube.
- Phát/tạm dừng, tua nhạc và điều chỉnh âm lượng.
- Next và Previous bằng con trỏ `current`.
- Xóa đúng Node và cập nhật bài đang phát.
- Tìm kiếm gần đúng theo tên bài hát hoặc ca sĩ.
- Shuffle nhưng giữ nguyên cặp title–artist.
- Repeat một bài hoặc toàn playlist.
- Đánh dấu yêu thích.
- Hỗ trợ URL `youtube.com/watch`, `youtu.be`, `shorts`, `embed`, `live` và video ID.
- Lưu playlist vào JSON sau khi tắt chương trình.
- Kiểm tra liên kết `head`, `tail`, `prev`, `next` sau các thao tác.

## 5. Ánh xạ chức năng

| Giao diện | Flask API | Hàm Python |
|---|---|---|
| Thêm bài hát | `POST /api/songs` | `add_song()` |
| Xóa bài hát | `DELETE /api/songs/<id>` | `delete_by_id()` → `delete_node()` |
| Tìm kiếm | `GET /api/songs?q=...` | `search_song()` |
| Bài tiếp theo | `POST /api/next` | `next_song()` |
| Bài trước | `POST /api/previous` | `prev_song()` |
| Trộn bài | `POST /api/shuffle` | `shuffle_playlist()` |
| Chọn bài đang phát | `POST /api/current/<id>` | `set_current()` |

## 6. Chạy kiểm thử

```bash
python -m unittest test_core.py test_api.py -v
```

Code gốc có hai phiên bản không đồng nhất. Bản web dùng quy tắc mới trong `Giao diện.py`: xóa theo đúng **title + artist**, tìm theo cả tên bài hát và ca sĩ. Các lớp và cơ chế Doubly Linked List ban đầu vẫn được giữ nguyên.

## 7. Đưa dự án lên GitHub

Tải toàn bộ **nội dung bên trong thư mục** `LuvMusic-Doubly-Linked-List` lên repository. Không tải thư mục `__pycache__` hoặc file `.pyc`. Sau khi tải dự án về, người chấm chỉ cần giải nén và nhấp đúp `run.bat` trên Windows.

Ứng dụng phát video bằng YouTube IFrame Player. Một số video có thể không phát trong trang web nếu chủ sở hữu video đã tắt tính năng nhúng; khi đó hãy thử một liên kết YouTube khác cho phép nhúng.
