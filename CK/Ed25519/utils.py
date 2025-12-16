import hashlib

# ----------------------
# Curve Ed25519 Constants
# ----------------------
p  = 2**255 - 19
d  = 37095705934669439343138083508754565189542113879843219016388785533085940283555
l  = 2**252 + 27742317777372353535851937790883648493
B  = (
    15112221349535400772501151409588531511454012693041857206046113283949847762202,
    46316835694926478169428394003475163141307993866256225615783033603165251855960
)

# ----------------------
# SHA512
# ----------------------
def sha512(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()

# ----------------------
# Clamping scalar
# ----------------------
def clamp_scalar(scalar_bytes: bytes) -> int:
    s = bytearray(scalar_bytes)
    s[0] &= 248
    s[31] &= 127
    s[31] |= 64
    return int.from_bytes(s, "little")

# ----------------------
# Modular inverse
# ----------------------
def inv(x, m):
    return pow(x, m-2, m)

# ----------------------
# Point operations (Twisted Edwards)
# ----------------------
def ed_add(P, Q):
    # P + Q on Ed25519
    x1, y1 = P
    x2, y2 = Q
    x3 = ((x1*y2 + x2*y1) * inv(1 + d*x1*x2*y1*y2, p)) % p
    y3 = ((y1*y2 + x1*x2) * inv(1 - d*x1*x2*y1*y2, p)) % p
    return (x3, y3)

def ed_double(P):
    return ed_add(P, P)

def scalar_mult(P, e: int):
    # Montgomery ladder
    Q = (0, 1)  # neutral element
    for i in reversed(range(e.bit_length())):
        Q = ed_double(Q)
        if (e >> i) & 1:
            Q = ed_add(Q, P)
    return Q

# ----------------------
# Encode/Decode points
# ----------------------
def recover_x(y, sign_bit):
    y2 = y*y % p
    u = (y2 - 1) % p
    v = (d*y2 + 1) % p
    inv_v = pow(v, p-2, p)
    x2 = (u*inv_v) % p
    x = pow(x2, (p+3)//8, p)
    if (x*x - x2) % p != 0:
        x = (x * pow(2,(p-1)//4,p)) % p
    if x & 1 != sign_bit:
        x = p - x
    return x

def encode_point(P):
    x, y = P
    b = y.to_bytes(32, "little")
    if x & 1:
        b = bytearray(b)
        b[31] |= 0x80
    return bytes(b)

def decode_point(b):
    y = int.from_bytes(b[:32], "little") & ((1<<255)-1)
    sign_x = (b[31] >> 7) & 1
    x = recover_x(y, sign_x)
    return (x, y)
