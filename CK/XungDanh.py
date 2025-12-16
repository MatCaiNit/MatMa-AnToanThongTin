# demo_rsa_challenge_response_verbose.py
import os
import hashlib
from RSA import (
    generate_rsa_keypair,
    rsa_encrypt_integer,
    rsa_decrypt_integer_crt,
    bytes_to_integer,
    integer_to_bytes
)

def demo_rsa_challenge_response():
    print("=== Bước 1: Alice tạo cặp khóa RSA 4096-bit ===")
    pub, priv = generate_rsa_keypair(prime_bits=2048)
    
    print("\nKhóa công khai (Alice):")
    print(f"  n (modulus, 64 ký tự đầu): {hex(pub['n'])[2:66]}...")
    print(f"  e = {pub['e']}")
    print("\nKhóa bí mật (Alice):")
    print(f"  d (int, 64 ký tự đầu): {hex(priv['d'])[2:66]}...")
    print(f"  p = {priv['p']}")
    print(f"  q = {priv['q']}")
    print(f"  dp = {priv['dp']}")
    print(f"  dq = {priv['dq']}")
    print(f"  qinv = {priv['qinv']}")

    # --- Bước 2: Bob tạo Challenge ---
    challenge = os.urandom(32)
    print(f"\n=== Bước 2: Bob tạo Challenge ===")
    print(f"Challenge (hex) = {challenge.hex()}")

    # --- Bước 3: Alice ký Challenge (tạo Response) ---
    print("\n=== Bước 3: Alice ký Challenge ===")
    # Hash challenge
    challenge_hash = hashlib.sha256(challenge).digest()
    hash_int = bytes_to_integer(challenge_hash)
    print(f"Hash của Challenge (int) = {hash_int}")

    # Ký bằng khóa bí mật (sử dụng CRT)
    signature_int = rsa_decrypt_integer_crt(hash_int, priv)
    signature_bytes = integer_to_bytes(signature_int)
    print(f"Signature (int) = {signature_int}")
    print(f"Signature (hex) = {signature_bytes.hex()}")

    # --- Bước 4: Bob nhận Response và xác minh ---
    print("\n=== Bước 4: Bob xác minh Response ===")
    # Hash lại challenge
    bob_hash_int = bytes_to_integer(hashlib.sha256(challenge).digest())
    print(f"Hash gốc Challenge (int) = {bob_hash_int}")

    # Giải mã signature bằng khóa công khai
    verified_hash_int = rsa_encrypt_integer(signature_int, pub)
    print(f"Hash giải mã từ Signature (int) = {verified_hash_int}")

    # So sánh
    if verified_hash_int == bob_hash_int:
        print("\nKết quả: Alice đã xưng danh HỢP LỆ (Challenge–Response thành công).")
    else:
        print("\nKết quả: Xác thực THẤT BẠI.")

if __name__ == "__main__":
    demo_rsa_challenge_response()
