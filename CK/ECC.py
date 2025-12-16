# ecc_ecdsa.py

import secrets
import hashlib

# --- Tham số SECP192R1 ---
P  = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF", 16)
A  = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC", 16)
B  = int("64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1", 16)
Gx = int("188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012", 16)
Gy = int("07192B95FFC8DA78631011ED6B24CDD573F977A11E794811", 16)
N  = int("FFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831", 16)
H  = 1

# --- Hàm các phép toán elliptic curve trên trường hữu hạn ---
def inverse_mod(k, p):
    """Tính nghịch đảo mod p (k^-1 mod p)."""
    if k == 0:
        raise ZeroDivisionError("Không thể tính nghịch đảo của 0")
    return pow(k, p - 2, p)

def point_add(P1, P2):
    """Cộng hai điểm P1, P2 trên đường cong"""
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2 and y1 != y2:
        return None
    if x1 == x2:
        # P1 == P2
        m = (3 * x1 * x1 + A) * inverse_mod(2 * y1, P) % P
    else:
        m = (y2 - y1) * inverse_mod(x2 - x1, P) % P
    x3 = (m * m - x1 - x2) % P
    y3 = (m * (x1 - x3) - y1) % P
    return (x3, y3)

def point_mul(k, P):
    """Nhân điểm P với k (double-and-add)"""
    R = None
    addend = P
    while k:
        if k & 1:
            R = point_add(R, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return R

# --- Hàm sinh khóa ---
def generate_keypair():
    """Sinh cặp khóa ECC (d, Q)"""
    d = secrets.randbelow(N - 1) + 1
    Q = point_mul(d, (Gx, Gy))
    return d, Q

# --- Ký ECDSA ---
def sign(message: bytes, d: int):
    """Ký thông điệp bằng khóa bí mật d"""
    e = int.from_bytes(hashlib.sha256(message).digest(), 'big')
    while True:
        k = secrets.randbelow(N - 1) + 1
        R = point_mul(k, (Gx, Gy))
        r = R[0] % N
        if r == 0:
            continue
        s = (inverse_mod(k, N) * (e + d * r)) % N
        if s != 0:
            break
    print("\n--- Ký ECDSA ---")
    print(f"k = {k}")
    print(f"R = ({R[0]}, {R[1]})")
    print(f"r = {r}")
    print(f"s = {s}")
    return r, s

# --- Xác minh ECDSA ---
def verify(message: bytes, r: int, s: int, Q):
    """Xác minh chữ ký (r, s) với khóa công khai Q"""
    if not (1 <= r < N) or not (1 <= s < N):
        return False
    e = int.from_bytes(hashlib.sha256(message).digest(), 'big')
    w = inverse_mod(s, N)
    u1 = (e * w) % N
    u2 = (r * w) % N
    X = point_add(point_mul(u1, (Gx, Gy)), point_mul(u2, Q))
    if X is None:
        return False
    x1, y1 = X
    print("\n--- Xác minh ECDSA ---")
    print(f"w = {w}")
    print(f"u1 = {u1}")
    print(f"u2 = {u2}")
    print(f"X = ({x1}, {y1})")
    print(f"x1 mod N = {x1 % N}")
    return (x1 % N) == r

# --- Hàm hiển thị tham số ---
def print_parameters(d=None, Q=None):
    print("\n=== Tham số đường cong SECP192R1 ===")
    print(f"P = {P}")
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"G = ({Gx}, {Gy})")
    print(f"N = {N}, H = {H}")
    if d and Q:
        print("\n=== Khóa ECC ===")
        print(f"d = {d}")
        print(f"Q = ({Q[0]}, {Q[1]})")
