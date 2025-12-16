import hashlib, os
from RSA import (
    generate_rsa_keypair as generate_keys,
    rsa_encrypt_integer as rsa_verify,
    rsa_decrypt_integer_crt as rsa_sign,
    bytes_to_integer as b2i,
    integer_to_bytes as i2b
)

def demo_auth_challenge_response():
    """Minh họa sơ đồ Xưng danh Challenge–Response dùng Chữ ký số RSA."""
    
    # --- 1. ALICE (Người xưng danh) ---
    print("Alice: Dang tao cap khoa RSA 4096-bit...")
    alice_pub_key, alice_priv_key = generate_keys()

    # --- 2. BOB (Người xác minh): Tạo Challenge ---
    challenge_data = os.urandom(32) # Giá trị ngẫu nhiên 32 byte
    print(f"\nBob: Tao Challenge ngau nhien = {challenge_data.hex()}...")

    # --- 3. ALICE: Tạo Response (Chữ ký) ---
    # Buoc 3a: Hash Challenge
    challenge_hash_digest = hashlib.sha256(challenge_data).digest()
    hash_int = b2i(challenge_hash_digest)
    
    # Buoc 3b: Ky (Decrypt) Hash bang khoa BI MAT
    # Response = Hash(Challenge)^d mod n
    signature_int = rsa_sign(hash_int, alice_priv_key)
    digital_signature_response = i2b(signature_int)
    
    print("Alice: Ky Challenge (Response) va gui lai cho Bob.")

    # --- 4. BOB: Xác minh Response ---
    bob_received_signature = digital_signature_response

    # Buoc 4a: Bob Hash lai Challenge ban dau (de so sanh)
    bob_hash_int = b2i(hashlib.sha256(challenge_data).digest())
    
    # Buoc 4b: Bob Giai ma (Encrypt) chu ky bang khoa CONG KHAI
    # Verified Hash = Signature^e mod n
    sig_int = b2i(bob_received_signature)
    verified_hash_int = rsa_verify(sig_int, alice_pub_key) 

    # Buoc 4c: So sanh
    is_authenticated = (verified_hash_int == bob_hash_int)

    print("\nBob: Hash tu Challenge goc =", bob_hash_int)
    print("Bob: Hash giai ma tu Response =", verified_hash_int)
    
    if is_authenticated:
        print("\n Bob: Alice da xung danh HOP LE (Challenge–Response THANH CONG).")
    else:
        print("\n Bob: Xac thuc THAT BAI.")

if __name__ == "__main__":
    demo_auth_challenge_response()