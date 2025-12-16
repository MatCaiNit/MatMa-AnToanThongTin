# demo_ecdsa.py

from ECC import generate_keypair, sign, verify, print_parameters

def demo_ecc_digital_signature():
    """Minh họa quy trình ký và xác minh chữ ký số ECDSA (Alice -> Bob)."""
    
    # --- 1. ALICE (Người Ký) ---
    print("Alice: Dang tao cap khoa ECC 192-bit...")
    d, Q = generate_keypair()
    print_parameters(d, Q)

    original_message = b"Day la thong diep can ky"
    print(f"\nAlice: Thong diep goc = {original_message}")

    # Alice ký thông điệp
    r, s = sign(original_message, d)
    print(f"Alice: Tao chu ky so (r, s) = ({r}, {s})")
    print("Alice: Gui chu ky va thong diep cho Bob")

    # --- 2. BOB (Người Xác minh) ---
    bob_received_message = original_message
    bob_received_signature = (r, s)

    print("\nBob: Tien hanh xac minh chu ky bang khoa CONG KHAI...")
    valid = verify(bob_received_message, bob_received_signature[0], bob_received_signature[1], Q)

    if valid:
        print("Bob: Chu ky hop le = True (Xac minh THANH CONG).")
    else:
        print("Bob: Chu ky hop le = False (Xac minh THAT BAI).")

if __name__ == "__main__":
    demo_ecc_digital_signature()
