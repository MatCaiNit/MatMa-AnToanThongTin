import secrets
import math
import sys

def is_probable_prime(n: int, rounds: int = 64) -> bool:
    """
    Kiểm tra tính nguyên tố xác suất bằng thuật toán Miller-Rabin.
    """
    if n < 2: return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    if n in small_primes: return True
    for p in small_primes:
        if n % p == 0: return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2  
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def random_odd_with_msb(bits: int) -> int:
    """Sinh số ngẫu nhiên lẻ có độ dài chính xác là 'bits'."""
    n = secrets.randbits(bits)
    n |= (1 << (bits - 1)) # Đặt bit cao nhất
    n |= 1                  # Đặt bit thấp nhất (số lẻ)
    return n

def generate_strong_prime(bits: int) -> int:
    """Tìm số nguyên tố xác suất có độ dài bits."""
    sys.stdout.write(f"\rDang tim prime {bits}-bit...")
    sys.stdout.flush()
    while True:
        candidate = random_odd_with_msb(bits)
        if is_probable_prime(candidate):
            sys.stdout.write(f"\r Prime {bits}-bit da duoc sinh.")
            sys.stdout.flush()
            return candidate

def bytes_to_integer(b: bytes) -> int:
    """Chuyển đổi bytes sang integer (Big Endian)."""
    return int.from_bytes(b, byteorder="big")

def integer_to_bytes(x: int) -> bytes:
    """Chuyển đổi integer sang bytes (Big Endian)."""
    blen = (x.bit_length() + 7) // 8
    return x.to_bytes(blen, byteorder="big")

def generate_elgamal_keypair(bits: int = 2048):
    """
    Sinh cặp khóa ElGamal. Khóa công khai (p, g, y), Khóa bí mật (p, g, x).
    """
    # 1. Sinh số nguyên tố p
    p = generate_strong_prime(bits)
    
    # 2. Chọn generator g và khóa bí mật x
    g = 2 # g thường là một giá trị nhỏ, hoặc một generator ngẫu nhiên trong Zp*
    x = secrets.randbelow(p - 2) + 1  # 1 < x < p-1 
    
    # 3. Tính khóa công khai y
    y = pow(g, x, p)
    
    public_key = (p, g, y)
    private_key = (p, g, x)
    return public_key, private_key

def elgamal_encrypt_message(message_int: int, public_key: tuple) -> tuple:
    """Mã hóa số nguyên thông điệp m thành bản mã (c1, c2)."""
    p, g, y = public_key
    if not (0 < message_int < p):
        raise ValueError("So nguyen thong diep vuot qua gioi han modulus (p)")
        
    # Chọn k ngẫu nhiên (ephemeral key)
    k = secrets.randbelow(p - 2) + 1
    
    # c1 = g^k mod p
    c1 = pow(g, k, p)
    
    # s = y^k mod p (Shared secret)
    s = pow(y, k, p)
    
    # c2 = m * s mod p
    c2 = (message_int * s) % p
    
    return (c1, c2)

def elgamal_decrypt_cipher(cipher_pair: tuple, private_key: tuple) -> int:
    """Giải mã bản mã (c1, c2) thành số nguyên thông điệp m."""
    p, g, x = private_key
    c1, c2 = cipher_pair
    
    # 1. Tinh lai Shared secret: s = c1^x mod p
    s = pow(c1, x, p)
    
    # 2. Tinh nghich dao cua s: s_inv = s^(-1) mod p
    s_inv = pow(s, -1, p) 
    
    # 3. Giai ma: m = c2 * s_inv mod p
    # Vi c2 = m * s mod p, suy ra m = c2 * s^(-1) mod p
    m = (c2 * s_inv) % p
    
    return m

if __name__ == "__main__":
    print("--- DEMO THUẬT TOÁN MÃ HÓA ELGAMAL 2048-BIT ---")
    
    # Sinh khóa
    pub, priv = generate_elgamal_keypair(bits=2048)
    
    print("\nTHÔNG SỐ KHÓA:")
    print(f"  Modulus p (bits): {pub[0].bit_length()}")
    print(f"  Generator g: {pub[1]}")
    
    # Chuẩn bị thông điệp
    raw_message = b"Day la thong diep bi mat duoc ma hoa bang ElGamal."
    m_int = bytes_to_integer(raw_message)
    
    if m_int >= pub[0]:
        print("\n[CANH BAO] Thong diep qua lon cho modulus ElGamal. Can su dung Padding truoc.")
        sys.exit(1)

    print("\nQUÁ TRÌNH MÃ HÓA/GIẢI MÃ:")
    
    # 1. MÃ HÓA
    cipher_pair = elgamal_encrypt_message(m_int, pub)
    print(f"  [Encrypt] Ban ma (c1, c2) duoc tao.")
    
    # 2. GIẢI MÃ
    recovered_int = elgamal_decrypt_cipher(cipher_pair, priv)
    
    # 3. Chuyển đổi kết quả về dạng bytes
    recovered_message = integer_to_bytes(recovered_int)

    print(f"\nKet qua:")
    print(f"  Thong diep goc: {raw_message.decode()}")
    print(f"  Thong diep giai ma: {recovered_message.decode()}")
    
    is_match = (raw_message == recovered_message)
    print(f"  Kiem tra khop: {is_match}")