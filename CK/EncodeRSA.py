from RSA import (
    generate_rsa_keypair as generate_keys,
    rsa_encrypt_integer as rsa_encrypt,
    rsa_decrypt_integer_crt as rsa_decrypt,
    bytes_to_integer as b2i,
    integer_to_bytes as i2b
)

def demo_rsa_encryption_exchange():
    """Minh họa quy trình Mã hóa và Giải mã RSA 4096-bit."""
    
    # --- 1. ALICE (Người Nhận): Sinh Khóa ---
    print("Alice: Dang tao cap khoa RSA 4096-bit...")
    alice_public_key, alice_private_key = generate_keys()

    # Bob nhan khoa cong khai cua Alice
    bob_encryption_key = alice_public_key

    # --- 2. BOB (Người Gửi): Mã hóa ---
    original_message = b"Xin chao Alice, day la Bob!"
    print(f"Bob: Thong diep goc = {original_message}")
    
    message_int = b2i(original_message)
    
    # Kiem tra kich thuoc thong diep
    if message_int >= bob_encryption_key["n"]:
        raise RuntimeError("Thong diep qua lon cho modulus RSA (Can su dung Padding truoc)")

    # Ma hoa bang khoa CONG KHAI cua Alice
    cipher_int = rsa_encrypt(message_int, bob_encryption_key)
    print("Bob: Ma hoa thanh cong va gui ban ma cho Alice.")

    # --- 3. ALICE (Người Nhận): Giải mã ---
    # Alice nhan ban ma va giai ma bang khoa BI MAT cua minh
    recovered_int = rsa_decrypt(cipher_int, alice_private_key)
    recovered_message = i2b(recovered_int)

    # --- 4. Kết quả ---
    print(f"\nAlice: Thong diep giai ma duoc = {recovered_message}")
    
    is_match = (recovered_message == original_message)
    print("Alice: Khop voi thong diep ban dau =", is_match)

if __name__ == "__main__":
    demo_rsa_encryption_exchange()