from key import generate_keypair, export_private_seed, export_public_key
from sign import sign, verify

def main_demo():
    print("[*] Step 1: Generate keypair")
    seed, a, A = generate_keypair()
    priv_bytes = export_private_seed(seed)
    pub_bytes = export_public_key(A)

    print("\n[*] Step 2: Sign message")
    msg = b"Demo Ed25519 thuan Python"
    sig = sign(a, A, msg)

    print("\n[*] Step 3: Verify signature")
    valid = verify(A, msg, sig)
    print("Signature valid?", valid)

    print("\n[*] Step 4: Tamper test")
    tampered = b"Tampered message"
    valid_tampered = verify(A, tampered, sig)
    print("Signature valid for tampered message?", valid_tampered)

if __name__ == "__main__":
    main_demo()
