import os
from utils import sha512, clamp_scalar, scalar_mult, encode_point, B

SEED_LEN = 32

def log(msg, value):
    print(f"[LOG] {msg}: {value}")

def generate_seed():
    seed = os.urandom(SEED_LEN)
    log("Seed generated (hex)", seed.hex())
    return seed

def scalar_mult_base(a):
    return scalar_mult(B, a)

def generate_keypair(seed=None):
    if seed is None:
        seed = generate_seed()
    h = sha512(seed)
    log("SHA512(seed)", h.hex())
    a = clamp_scalar(h[:32])
    log("Clamped scalar a", a)
    A = scalar_mult_base(a)
    log("Public point A", A)
    return seed, a, A

def export_private_seed(seed):
    log("Export private seed", seed.hex())
    return seed

def export_public_key(A):
    encoded = encode_point(A)
    log("Encoded public key", encoded.hex())
    return encoded
