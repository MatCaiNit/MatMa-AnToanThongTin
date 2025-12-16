import hashlib
from RSA import (
    generate_rsa_keypair as generate_keys,
    rsa_encrypt_integer as rsa_verify,
    rsa_decrypt_integer_crt as rsa_sign,
    bytes_to_integer as b2i,
    integer_to_bytes as i2b
)

def demo_rsa_digital_signature():
    """Minh họa quy trình ký và xác minh chữ ký số RSA."""
    
    # --- 1. ALICE (Người Ký): Chuẩn bị và Ký ---
    print("Alice: Dang tao cap khoa RSA 4096-bit...")
    # pub_key = (e, n), priv_key = (d, n)
    alice_pub_key, alice_priv_key = generate_keys()

    original_message = b"Day la thong diep can ky"
    print(f"Alice: Thong diep goc = {original_message}")

    # Buoc 1a: Hash thong diep
    message_hash_digest = hashlib.sha256(original_message).digest()
    hash_int = b2i(message_hash_digest)
    print(hash_int)
    
    # Buoc 1b: Ky bang khoa bi mat (private key)
    # Chu ky duoc tao ra bang cach tinh Hash^d mod n
    signature_int = rsa_sign(hash_int, alice_priv_key)
    print(f"Sign {signature_int}")
    digital_signature = i2b(signature_int)
    
    print("Alice: Tao chu ky so thanh cong.")
    print("Alice: Gui Thong diep va Chu ky cho Bob.")

    # --- 2. BOB (Nguoi Nhan): Xác minh ---
    bob_received_message = original_message
    bob_received_signature = digital_signature
    
    # Buoc 2a: Bob hash thong diep nhan duoc
    bob_message_hash_digest = hashlib.sha256(bob_received_message).digest()
    bob_hash_int = b2i(bob_message_hash_digest)
    
    # Buoc 2b: Bob su dung khoa cong khai (public key) cua Alice de giai ma chu ky
    # Ket qua nay chinh la Hash' = Signature^e mod n
    sig_int = b2i(bob_received_signature)
    hash_from_signature_int = rsa_verify(sig_int, alice_pub_key) 
    
    # Buoc 2c: So sanh Hash nhan duoc voi Hash giai ma tu chu ky
    is_valid = (hash_from_signature_int == bob_hash_int)

    print("\nBob: Ket qua Hash tu Thong diep nhan duoc =", bob_hash_int)
    print("Bob: Ket qua Hash giai ma tu Chu ky   =", hash_from_signature_int)
    print("Bob: CHU KY HOP LE (Xac thuc thanh cong) =", is_valid)

if __name__ == "__main__":
    demo_rsa_digital_signature()