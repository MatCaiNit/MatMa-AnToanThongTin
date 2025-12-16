import hashlib
from ECC import generate_ecc_keypair as generate_ecc_keys 

# Import các lớp từ thư viện cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

def demo_ecc_digital_signature():
    """Minh họa quy trình ký và xác minh chữ ký số ECDSA."""
    
    # --- 1. ALICE (Người Ký): Chuẩn bị và Ký ---
    print("Alice: Dang tao cap khoa ECC 192-bit...")
    # alice_priv là ec.EllipticCurvePrivateKey, alice_pub là ec.EllipticCurvePublicKey
    alice_private_key, alice_public_key = generate_ecc_keys()

    original_message = b"Day la thong diep can ky"
    print(f"Alice: Thong diep goc = {original_message}")

    # Buoc 1: Alice ky thong diep bang khoa BI MAT
    # Sử dụng hàm băm SHA256 và sơ đồ ECDSA
    digital_signature = alice_private_key.sign(
        original_message,
        ec.ECDSA(hashes.SHA256())
    )
    print("Alice: Tao chu ky so thanh cong va gui cho Bob")

    # --- 2. BOB (Người Xác minh): Xác minh ---
    bob_received_message = original_message
    bob_received_signature = digital_signature

    print("\nBob: Tien hanh xac minh chu ky bang khoa CONG KHAI...")
    try:
        # Bob su dung khoa CONG KHAI de xac minh chu ky
        alice_public_key.verify(
            bob_received_signature,
            bob_received_message,
            ec.ECDSA(hashes.SHA256())
        )
        print("Bob: Chu ky hop le = True (Xac minh THANH CONG).")
    except Exception as e:
        # Neu xac minh that bai (vi du: thong diep bi thay doi, chu ky bi sai)
        print(f"Bob: Chu ky hop le = False (Xac minh THAT BAI). Chi tiet loi: {e}")

if __name__ == "__main__":
    demo_ecc_digital_signature()