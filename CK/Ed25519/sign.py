from utils import sha512, scalar_mult, encode_point, decode_point, ed_add, B, l

def log(msg, value):
    print(f"[LOG] {msg}: {value}")

def sign(a, A, message_bytes):
    log("Message bytes", message_bytes.hex())
    r = int.from_bytes(sha512(a.to_bytes(32,"little") + message_bytes), "little") % l
    log("Nonce r", r)
    R = scalar_mult(B, r)
    log("Point R", R)
    R_enc = encode_point(R)
    log("Encoded R", R_enc.hex())

    k = int.from_bytes(sha512(R_enc + encode_point(A) + message_bytes), "little") % l
    log("Challenge k", k)
    S = (r + k*a) % l
    log("Scalar S", S)
    signature = R_enc + S.to_bytes(32,"little")
    log("Final signature", signature.hex())
    return signature

def verify(A, message_bytes, signature):
    R_enc = signature[:32]
    S = int.from_bytes(signature[32:], "little")
    R = decode_point(R_enc)
    log("Decoded R", R)
    log("Scalar S from signature", S)
    k = int.from_bytes(sha512(R_enc + encode_point(A) + message_bytes), "little") % l
    log("Challenge k", k)
    SB = scalar_mult(B, S)
    kA = scalar_mult(A, k)
    log("Point SB", SB)
    log("Point k*A", kA)
    R_plus_kA = ed_add(R, kA)
    log("Point R + k*A", R_plus_kA)
    valid = SB == R_plus_kA
    log("Signature valid?", valid)
    return valid
