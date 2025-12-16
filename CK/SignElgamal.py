import math
import hashlib
import secrets
from Elgamal import generate_elgamal_keypair as generate_keys, bytes_to_integer as b2i

def elgamal_sign_message(message: bytes, private_key: tuple) -> tuple:
    """Thực hiện ký thông điệp bằng khóa bí mật ElGamal."""
    p, g, x = private_key
    
    # 1. Băm thông điệp
    message_digest = hashlib.sha256(message).digest()
    m = b2i(message_digest)

    # 2. Chọn giá trị ngẫu nhiên k (Ephemeral key)
    # k phải thỏa mãn gcd(k, p - 1) = 1
    while True:
        k = secrets.randbelow(p - 2) + 1
        if math.gcd(k, p - 1) == 1:
            break
            
    # 3. Tính r (Thành phần đầu tiên của chữ ký)
    # r = g^k mod p
    r = pow(g, k, p)
    
    # 4. Tính k_inv (Nghịch đảo modulo của k)
    k_inv = pow(k, -1, p - 1)
    
    # 5. Tính s (Thành phần thứ hai của chữ ký)
    # s = k_inv * (m - x*r) mod (p - 1)
    s = (k_inv * (m - x * r)) % (p - 1)
    
    return (r, s)

def elgamal_verify_signature(message: bytes, signature: tuple, public_key: tuple) -> bool:
    """Xác minh chữ ký bằng khóa công khai ElGamal."""
    p, g, y = public_key
    r, s = signature
    
    # 1. Kiểm tra r
    if not (0 < r < p):
        return False

    # 2. Băm thông điệp
    message_digest = hashlib.sha256(message).digest()
    m = b2i(message_digest)

    # 3. Tính vế trái (Verification Equation)
    # Left = g^m mod p
    left_side = pow(g, m, p)
    
    # 4. Tính vế phải
    # Right = (y^r * r^s) mod p
    y_r = pow(y, r, p)
    r_s = pow(r, s, p)
    right_side = (y_r * r_s) % p
    
    # 5. So sánh
    return left_side == right_side

def demo_elgamal_digital_signature():
    print("Alice: Dang tao cap khoa ElGamal 2048-bit...")
    # Khóa công khai (p, g, y), Khóa bí mật (p, g, x)
    alice_pub_key, alice_priv_key = generate_keys(2048)

    message_to_sign = b"Day la thong diep can ky"
    print(f"Alice: Thong diep goc = {message_to_sign}")

    # --- ALICE: Ký thông điệp ---
    digital_signature = elgamal_sign_message(message_to_sign, alice_priv_key)
    print("Alice: Tao chu ky so thanh cong (r, s) va gui cho Bob")

    # --- BOB: Xác minh chữ ký ---
    bob_received_message = message_to_sign
    bob_received_signature = digital_signature

    is_valid = elgamal_verify_signature(bob_received_message, bob_received_signature, alice_pub_key)
    print("Bob: Chu ky hop le =", is_valid)

if __name__ == "__main__":
    demo_elgamal_digital_signature()