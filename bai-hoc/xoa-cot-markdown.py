import os
from pathlib import Path

# --- CẤU HÌNH ---
# Đặt đường dẫn đến thư mục chứa các tệp Markdown của bạn ở đây.
# Sử dụng '.' để chỉ định thư mục hiện tại (nơi bạn chạy script).
TARGET_DIRECTORY = '.' 

def process_markdown_line(line):
    """
    Xử lý một dòng văn bản. Nếu dòng này là một phần của bảng Markdown
    và có đủ cột, nó sẽ xóa cột thứ tư.
    """
    # Loại bỏ khoảng trắng ở đầu và cuối dòng để kiểm tra
    stripped_line = line.strip()

    # Một dòng được coi là hàng của bảng nếu nó bắt đầu và kết thúc bằng '|'
    if stripped_line.startswith('|') and stripped_line.endswith('|'):
        # Tách dòng thành các cột dựa trên dấu '|'
        columns = stripped_line.split('|')
        
        # Một bảng 4 cột khi tách ra sẽ có 6 phần tử
        # (phần tử đầu và cuối là chuỗi rỗng do có '|' ở hai đầu)
        # Ví dụ: '| A | B | C | D |' -> ['', ' A ', ' B ', ' C ', ' D ', '']
        if len(columns) >= 6:
            # Xóa cột thứ tư (có chỉ số là 4 trong danh sách)
            del columns[4]
            
            # Ghép các cột còn lại thành một dòng mới và thêm ký tự xuống dòng
            return '|'.join(columns) + '\n'
            
    # Nếu không phải là một hàng của bảng hoặc không đủ cột, trả về dòng gốc
    return line

def process_markdown_file(file_path):
    """
    Đọc một tệp Markdown, xử lý và ghi đè lại với các bảng đã được sửa đổi.
    """
    print(f"🔄 Đang xử lý tệp: {file_path}...")
    try:
        # Đọc tất cả các dòng từ tệp gốc với encoding utf-8
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Tạo một danh sách mới để lưu các dòng đã được xử lý
        new_lines = []
        for line in lines:
            new_lines.append(process_markdown_line(line))

        # Ghi đè tệp gốc với nội dung đã được sửa đổi
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
        print(f"✅ Xử lý thành công: {file_path}")

    except Exception as e:
        print(f"❌ Lỗi khi xử lý tệp {file_path}: {e}")

def main():
    """
    Hàm chính để tìm và xử lý tất cả các tệp Markdown.
    """
    # Chuyển đổi đường dẫn thư mục thành đối tượng Path để dễ xử lý
    path = Path(TARGET_DIRECTORY)

    # Tìm tất cả các tệp .md trong thư mục và các thư mục con của nó
    markdown_files = list(path.rglob('*.md'))

    if not markdown_files:
        print(f"⚠️ Không tìm thấy tệp Markdown nào trong thư mục '{TARGET_DIRECTORY}'.")
        return

    print(f"🔎 Tìm thấy {len(markdown_files)} tệp Markdown. Bắt đầu xử lý...")
    for file_path in markdown_files:
        process_markdown_file(file_path)
    
    print("\n🎉 Hoàn tất! Tất cả các tệp đã được xử lý.")

if __name__ == "__main__":
    main()