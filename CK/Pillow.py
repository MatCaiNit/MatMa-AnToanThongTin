import os
from PIL import Image

# --- CÁC HÀM CÔNG CỤ HỖ TRỢ ---

def text_to_binary(text):
    """Chuyển chuỗi ký tự thành chuỗi bit (binary string)."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_string):
    """Chuyển chuỗi bit thành chuỗi ký tự."""
    if not binary_string:
        return ""
    # Đảm bảo chuỗi bit có độ dài là bội số của 8
    chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    
    # Chuyển từng byte (8 bit) thành ký tự
    return ''.join(chr(int(chunk, 2)) for chunk in chunks)

# --- CHỨC NĂNG LSB CỐT LÕI ---

def encode_image(image_path, message, output_path="encoded_image.png"):
    """
    Nhúng thông điệp vào LSB của các pixel ảnh.
    
    """
    try:
        img = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file ảnh tại {image_path}")
        return

    # Thêm ký tự kết thúc đặc biệt (ví dụ: '###') vào cuối thông điệp
    # để biết khi nào dừng giải mã.
    message_with_terminator = message + "###"
    binary_message = text_to_binary(message_with_terminator)
    message_length = len(binary_message)
    
    # Tổng số bit có thể chứa được: (chiều rộng * chiều cao * 3 kênh màu)
    max_capacity = img.width * img.height * 3
    
    if message_length > max_capacity:
        print(f"Lỗi: Thông điệp quá dài. Dung lượng tối đa: {max_capacity} bits.")
        return

    data_index = 0
    # Lặp qua từng pixel
    for x in range(img.width):
        for y in range(img.height):
            # Lấy giá trị R, G, B của pixel
            r, g, b = img.getpixel((x, y))

            # Chỉnh sửa LSB của từng kênh màu (R, G, B)
            
            # --- Kênh Đỏ (R) ---
            if data_index < message_length:
                # Xóa LSB cũ (AND với 11111110) và thêm bit mới (OR)
                r = (r & 0b11111110) | int(binary_message[data_index])
                data_index += 1
            
            # --- Kênh Xanh Lá (G) ---
            if data_index < message_length:
                g = (g & 0b11111110) | int(binary_message[data_index])
                data_index += 1

            # --- Kênh Xanh Dương (B) ---
            if data_index < message_length:
                b = (b & 0b11111110) | int(binary_message[data_index])
                data_index += 1

            # Cập nhật pixel với giá trị R, G, B đã chỉnh sửa
            img.putpixel((x, y), (r, g, b))
            
            if data_index >= message_length:
                break
        if data_index >= message_length:
            break
            
    img.save(output_path, "PNG")
    print(f"Mã hóa thành công. Ảnh đã mã hóa lưu tại: {output_path}")

def decode_image(image_path):
    """Trích xuất thông điệp từ LSB của các pixel ảnh đã mã hóa."""
    try:
        img = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file ảnh tại {image_path}")
        return

    binary_message = ""
    terminator = "###"
    
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            
            # Trích xuất LSB của từng kênh màu
            # Lấy LSB: (r & 0b00000001)
            
            # Kênh R
            binary_message += str(r & 1)
            if len(binary_message) % 8 == 0 and binary_to_text(binary_message).endswith(terminator):
                return binary_to_text(binary_message)[:-len(terminator)]
            
            # Kênh G
            binary_message += str(g & 1)
            if len(binary_message) % 8 == 0 and binary_to_text(binary_message).endswith(terminator):
                return binary_to_text(binary_message)[:-len(terminator)]

            # Kênh B
            binary_message += str(b & 1)
            if len(binary_message) % 8 == 0 and binary_to_text(binary_message).endswith(terminator):
                return binary_to_text(binary_message)[:-len(terminator)]
                
    return binary_to_text(binary_message) # Trả về phần còn lại (ít khả năng xảy ra nếu không tìm thấy terminator)

# --- CHẠY DEMO ---

if __name__ == "__main__":
    # Ghi chú: Hãy chuẩn bị một file ảnh có tên 'original.png' hoặc 'original.jpg' 
    # trong cùng thư mục để chạy thử nghiệm.
    # cd đến CK trước rồi mới python Pillow.py để chạy
    
    ORIGINAL_IMAGE = "original.png"
    ENCODED_IMAGE = "stego_image.png"
    SECRET_MESSAGE = "Thong diep bi mat: Ky thuat LSB da duoc su dung!"
    
    print(f"[*] Thong diep goc: {SECRET_MESSAGE}")
    
    # 1. Mã hóa thông điệp vào ảnh
    encode_image(ORIGINAL_IMAGE, SECRET_MESSAGE, ENCODED_IMAGE)
    
    # 2. Giải mã thông điệp từ ảnh đã ẩn
    recovered_message = decode_image(ENCODED_IMAGE)
    
    print(f"\n[+] Thong diep trich xuat: {recovered_message}")
    
    if recovered_message == SECRET_MESSAGE:
        print("[SUCCESS] Thong diep duoc trich xuat chinh xac!")
    else:
        print("[FAIL] Thong diep bi mat da bi mat!")