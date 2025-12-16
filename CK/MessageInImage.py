def text_to_bits(text):
    """Chuyển text thành chuỗi bit."""
    return ''.join(f'{ord(c):08b}' for c in text)

def bits_to_text(bits):
    """Chuyển bit thành text."""
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def hide_message_bmp(input_bmp, output_bmp, message):
    """Giấu tin vào LSB của pixel BMP."""
    with open(input_bmp, "rb") as f:
        bmp_data = bytearray(f.read())

    # BMP header = 54 byte, không thay đổi
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    # Thêm ký hiệu kết thúc
    message += "###"
    bits = text_to_bits(message)

    print(f"[DEBUG] Tin gốc: {message}")
    print(f"[DEBUG] Chuỗi bit: {bits[:64]}... (64 bit đầu tiên)")

    if len(bits) > len(pixel_data):
        raise ValueError("Ảnh không đủ dung lượng để giấu tin.")

    # Nhúng bit
    for i, bit in enumerate(bits):
        old_pixel = pixel_data[i]
        pixel_data[i] = (pixel_data[i] & 0b11111110) | int(bit)
        new_pixel = pixel_data[i]
        if i < 32:  # chỉ log 32 pixel đầu tiên
            print(f"[ENCODE] Pixel[{i}] cũ={old_pixel:08b}, bit nhúng={bit}, Pixel mới={new_pixel:08b}")

    # Ghi ảnh mới
    with open(output_bmp, "wb") as f:
        f.write(header + pixel_data)

    print(f"Đã giấu tin vào {output_bmp}")

def extract_message_bmp(stego_bmp):
    """Trích xuất tin từ LSB của BMP."""
    with open(stego_bmp, "rb") as f:
        bmp_data = bytearray(f.read())

    pixel_data = bmp_data[54:]
    bits = ""
    terminator = "###"

    for i, b in enumerate(pixel_data):
        lsb = b & 1
        bits += str(lsb)

        if i < 32:  # log 32 pixel đầu tiên
            print(f"[DECODE] Pixel[{i}]={b:08b}, LSB={lsb}")

        if len(bits) % 8 == 0:
            text = bits_to_text(bits)
            if text.endswith(terminator):
                print(f"[DECODE] Tin tạm thời: {text[:-len(terminator)]}")
                return text[:-len(terminator)]

    return bits_to_text(bits)

if __name__ == "__main__":
    INPUT_BMP = "correct.bmp"       # File BMP gốc (RGB, không nén)
    OUTPUT_BMP = "stego.bmp"        # Ảnh lưu kết quả
    SECRET_MESSAGE = "Hidden Message!"

    print("Tin gốc:", SECRET_MESSAGE)

    # Giấu tin
    hide_message_bmp(INPUT_BMP, OUTPUT_BMP, SECRET_MESSAGE)

    # Trích tin
    recovered = extract_message_bmp(OUTPUT_BMP)
    print("Tin trích xuất:", recovered)

    if recovered == SECRET_MESSAGE:
        print("[SUCCESS] Tin trích xuất chính xác!")
    else:
        print("[FAIL] Tin trích xuất không khớp!")
