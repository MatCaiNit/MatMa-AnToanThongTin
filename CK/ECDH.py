# demo_ecdh_verbose.py
from ECC import generate_keypair, point_mul
import hashlib

def ecdh_shared_secret(priv, pub):
    """Tính khóa chung ECDH: K = d * Q"""
    return point_mul(priv, pub)

def hkdf_sha256(key_material, length=16, info=b"ecdh-demo"):
    """Hàm HKDF đơn giản dùng SHA-256"""
    # Bước 1: extract
    prk = hashlib.sha256(key_material.to_bytes(48, 'big')).digest()
    # Bước 2: expand
    okm = hashlib.sha256(prk + info + b'\x01').digest()
    return okm[:length]

def demo_ecdh():
    # Sinh cặp khóa Alice
    alice_priv, alice_pub = generate_keypair()
    print("Alice:")
    print(f"  Khóa riêng d = {alice_priv}")
    print(f"  Khóa công khai Q = ({alice_pub[0]}, {alice_pub[1]})\n")

    # Sinh cặp khóa Bob
    bob_priv, bob_pub = generate_keypair()
    print("Bob:")
    print(f"  Khóa riêng d = {bob_priv}")
    print(f"  Khóa công khai Q = ({bob_pub[0]}, {bob_pub[1]})\n")

    # Tính khóa chung
    alice_shared_point = ecdh_shared_secret(alice_priv, bob_pub)
    bob_shared_point   = ecdh_shared_secret(bob_priv, alice_pub)

    print("Khóa chung Alice tính được:")
    print(f"  X = {alice_shared_point[0]}")
    print(f"  Y = {alice_shared_point[1]}\n")

    print("Khóa chung Bob tính được:")
    print(f"  X = {bob_shared_point[0]}")
    print(f"  Y = {bob_shared_point[1]}\n")

    # Lấy x-coordinate làm shared secret
    alice_shared_int = alice_shared_point[0]
    bob_shared_int   = bob_shared_point[0]

    # Derive key từ shared secret
    alice_key = hkdf_sha256(alice_shared_int)
    bob_key   = hkdf_sha256(bob_shared_int)

    print("Khóa cuối sau HKDF:")
    print(f"  Alice key = {alice_key.hex()}")
    print(f"  Bob key   = {bob_key.hex()}")
    print("Khóa giống nhau:", alice_key == bob_key)

if __name__ == "__main__":
    demo_ecdh()
