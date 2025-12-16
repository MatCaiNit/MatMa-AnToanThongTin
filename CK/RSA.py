import secrets
import math
import sys
import time

def is_probable_prime_miller_rabin(n: int, rounds: int = 64) -> bool:
    """
    Kiểm tra tính nguyên tố xác suất bằng thuật toán Miller-Rabin.
    """
    if n < 2:
        return False
    # Sàng lọc nhanh với các số nguyên tố nhỏ
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False

    # Phân tích n - 1 = 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Thực hiện kiểm tra Miller-Rabin (rounds lần)
    for _ in range(rounds):
        # Chọn cơ số ngẫu nhiên 'a'
        a = secrets.randbelow(n - 3) + 2  
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
            
        # Kiểm tra điều kiện x^(2^j * d) = -1 mod n
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # Nếu vòng lặp không bị 'break', n là hợp số
            return False
    return True

def extended_gcd(a: int, b: int) -> tuple:
    """
    Giải thuật Euclid mở rộng: Tìm g = gcd(a, b) và x, y sao cho ax + by = g.
    """
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def modular_inverse(a: int, m: int) -> int:
    """
    Tính nghịch đảo modulo của a mod m (a^-1 mod m).
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Nghich dao modulo khong ton tai (khong phai la so nguyen to cung nhau)")
    return x % m


def random_odd_with_msb(bits: int) -> int:
    """Sinh số ngẫu nhiên lẻ có bit cao nhất được đặt (đảm bảo độ dài)."""
    n = secrets.randbits(bits)
    n |= (1 << (bits - 1))  # Đặt bit cao nhất (Most Significant Bit)
    n |= 1                  # Đặt bit thấp nhất (Least Significant Bit)
    return n

def generate_strong_prime(bits: int) -> int:
    """Tìm số nguyên tố xác suất có độ dài bits."""
    print(f"\r  Dang tim prime {bits}-bit...", end='')
    sys.stdout.flush()
    while True:
        candidate = random_odd_with_msb(bits)
        if is_probable_prime_miller_rabin(candidate):
            return candidate

def bytes_to_integer(b: bytes) -> int:
    """Chuyển đổi bytes sang integer (Big Endian)."""
    return int.from_bytes(b, byteorder="big")

def integer_to_bytes(x: int, length: int = None) -> bytes:
    """Chuyển đổi integer sang bytes (Big Endian), có thể thêm zero padding."""
    blen = (x.bit_length() + 7) // 8
    b = x.to_bytes(blen, byteorder="big")
    if length is not None and blen < length:
        b = b"\x00" * (length - blen) + b
    return b

def generate_rsa_keypair(prime_bits: int = 2048):
    """
    Sinh cặp khóa RSA: n = p*q (4096-bit) với p, q là nguyên tố 2048-bit.
    """
    start_time = time.time()
    # Khóa công khai mặc định
    e = 65537 
    
    # 1. Sinh hai số nguyên tố lớn p và q
    print(f"\nDang sinh p ({prime_bits}-bit)...")
    p = generate_strong_prime(prime_bits)
    print(f"\r p da duoc sinh. ({prime_bits}-bit).")
    print(f"\r p = {p}.")
    print(f"Dang sinh q ({prime_bits}-bit)...")
    while True:
        q = generate_strong_prime(prime_bits)
        if q != p:
            break
    print(f"\r q da duoc sinh. ({prime_bits}-bit).")
    print(f"\r q = {q}.")
    
    # 2. Tính n và phi(n)
    n = p * q
    print(f"\n n = {n}")
    phi = (p - 1) * (q - 1)
    print(f"\n phi = {phi}")

    # 3. Tính khóa bí mật d
    if math.gcd(e, phi) != 1:
         # Điều này hiếm khi xảy ra khi e=65537, nhưng là kiểm tra an toàn
         print("WARNING: gcd(e, phi) != 1. Tai tao khoa...")
         return generate_rsa_keypair(prime_bits)

    d = modular_inverse(e, phi)
    print(f"\n d = {d}")
    # 4. Tính các tham số CRT để tăng tốc giải mã
    # dp = d mod (p-1)
    # dq = d mod (q-1)
    # qinv = q^-1 mod p (sử dụng p thay vì n)
    dp = d % (p - 1)
    print(f"\n dp = {dp}")
    dq = d % (q - 1)
    print(f"\n dq = {dq}")
    qinv = modular_inverse(q, p)
    print(f"\n qinv = {qinv}")

    public_key = {"n": n, "e": e}
    private_key = {
        "n": n, "d": d, 
        "p": p, "q": q, 
        "dp": dp, "dq": dq, "qinv": qinv
    }
    
    elapsed = time.time() - start_time
    print(f"Hoan tat sinh khoa 4096-bit. Thoi gian: {elapsed:.2f}s.")
    return public_key, private_key

def rsa_encrypt_integer(message_int: int, public_key: dict) -> int:
    """Mã hóa số nguyên c = m^e mod n."""
    n, e = public_key["n"], public_key["e"]
    if not (0 <= message_int < n):
        raise ValueError("So nguyen thong diep vuot qua gioi han modulus (n)")
    c = pow(message_int, e, n)
    print(f"\n c = {c}")
    return c

def rsa_decrypt_integer_crt(cipher_int: int, private_key: dict) -> int:
    """
    Giải mã số nguyên c -> m = c^d mod n sử dụng Định lý Số dư Trung Hoa (CRT).
    CRT làm tăng tốc giải mã lên ~4 lần. 
    """
    n = private_key["n"]
    if not (0 <= cipher_int < n):
        raise ValueError("So nguyen ban ma vuot qua gioi han modulus (n)")
        
    p, q, dp, dq, qinv = private_key["p"], private_key["q"], private_key["dp"], private_key["dq"], private_key["qinv"]
    
    # 1. Tính toán modulo p và q
    # m1 = c^dp mod p
    m1 = pow(cipher_int, dp, p)
    print(f"\n m1 = {m1}")
    # m2 = c^dq mod q
    m2 = pow(cipher_int, dq, q)
    print(f"\n m2 = {m2}")
    # 2. Áp dụng CRT
    # h = qinv * (m1 - m2) mod p
    h = (qinv * (m1 - m2)) % p
    print(f"\n h = {h}")
    # m = m2 + h * q
    m = m2 + h * q
    print(f"\n m = {m}")
    return m

if __name__ == "__main__":
    print("--- DEMO THUẬT TOÁN RSA 4096-BIT ---")
    
    # Sinh khóa (phần tốn thời gian nhất)
    pub, priv = generate_rsa_keypair(prime_bits=2048)
    
    print("\nTHÔNG SỐ KHÓA:")
    print(f"  Do dai khóa (n): {pub['n'].bit_length()} bits")
    print(f"  Modulus n (hex, 64 ký tự đầu): {hex(pub['n'])[2:66]}...")
    print(f"  Khoa cong khai e: {pub['e']}")
    
    # Chuẩn bị thông điệp
    raw_message = b"Day la thong diep bi mat cua he thong RSA 4096-bit."
    m_int = bytes_to_integer(raw_message)
    
    if m_int >= pub["n"]:
        print("\n[CANH BAO] Thong diep qua lon cho RSA. Can phai su dung Padding/Segmenting.")
        sys.exit(1)

    print("\nQUÁ TRÌNH MÃ HÓA/GIẢI MÃ:")
    
    # 1. MÃ HÓA
    c_int = rsa_encrypt_integer(m_int, pub)
    print(f"  [Encrypt] Ban ma (integer, 20 ký tự đầu): {str(c_int)[:20]}...")
    
    # 2. GIẢI MÃ (sử dụng CRT)
    m_out_int = rsa_decrypt_integer_crt(c_int, priv)
    
    # 3. Chuyển đổi kết quả về dạng bytes
    recovered_message = integer_to_bytes(m_out_int)

    print(f"\nKet qua:")
    print(f"  Thong diep goc: {raw_message.decode()}")
    print(f"  Thong diep giai ma: {recovered_message.decode()}")
    
    is_match = (raw_message == recovered_message)
    print(f"  Kiem tra khop: {is_match}")