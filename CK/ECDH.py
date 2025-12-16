from ECC import generate_ecc_keypair
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def demo_ecdh():
    alice_priv, alice_pub = generate_ecc_keypair()
    print("Alice: sinh cặp khóa ECC 192-bit")

    bob_priv, bob_pub = generate_ecc_keypair()
    print("Bob: sinh cặp khóa ECC 192-bit")

    alice_shared = alice_priv.exchange(ec.ECDH(), bob_pub)

    bob_shared = bob_priv.exchange(ec.ECDH(), alice_pub)

    alice_key = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=None,
        info=b"ecdh-demo"
    ).derive(alice_shared)

    bob_key = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=None,
        info=b"ecdh-demo"
    ).derive(bob_shared)

    print("Alice key:", alice_key)
    print("Bob key:  ", bob_key)
    print("Khóa giống nhau:", alice_key == bob_key)

if __name__ == "__main__":
    demo_ecdh()