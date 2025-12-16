from Elgamal import (
    generate_elgamal_keypair as generate_keys,
    elgamal_encrypt_message as elgamal_encrypt_message,
    elgamal_decrypt_cipher as elgamal_decrypt_cipher,
    bytes_to_integer as b2i,
    integer_to_bytes as i2b
)

def demo_elgamal_encryption_exchange():
    """Minh họa quy trình Mã hóa và Giải mã ElGamal 2048-bit."""
    
    # --- 1. ALICE (Người Nhận): Sinh Khóa ---
    print("Alice: Dang tao cap khoa ElGamal 2048-bit...")
    # alice_pub = (p, g, y), alice_priv = (p, g, x)
    alice_public_key, alice_private_key = generate_keys(2048)

    # Bob nhan khoa cong khai cua Alice
    bob_encryption_key = alice_public_key

    # --- 2. BOB (Người Gửi): Mã hóa ---
    original_message = b"Xin chao Alice, day la Bob!"
    print(f"Bob: Thong diep goc = {original_message}")
    
    message_int = b2i(original_message)
    
    # Kiểm tra kích thước thông điệp (p là phần tử đầu tiên của tuple khóa công khai)
    if message_int >= bob_encryption_key[0]:
        raise RuntimeError("Thong diep qua lon cho modulus ElGamal (p)")

    # Mã hóa bằng khóa CÔNG KHAI của Alice. Bản mã là một tuple (c1, c2).
    cipher_pair = elgamal_encrypt_message(message_int, bob_encryption_key)
    print("Bob: Ma hoa thanh cong va gui ban ma cho Alice.")

    # --- 3. ALICE (Người Nhận): Giải mã ---
    # Alice nhan ban ma và giải mã bằng khóa BÍ MẬT của mình
    recovered_int = elgamal_decrypt_cipher(cipher_pair, alice_private_key)
    recovered_message = i2b(recovered_int)

    # --- 4. Kết quả ---
    print(f"\nAlice: Thong diep giai ma duoc = {recovered_message}")
    
    is_match = (recovered_message == original_message)
    print("Alice: Khop voi thong diep ban dau =", is_match)

if __name__ == "__main__":
    demo_elgamal_encryption_exchange()