from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_ecc_keypair(curve: ec.EllipticCurve = ec.SECP192R1()): 
    """Sinh cặp khóa ECC sử dụng đường cong đã chỉ định (mặc định là SECP192R1)."""
    # Khóa bí mật (d)
    ecc_private_key = ec.generate_private_key(curve)
    # Khóa công khai (Q = d*G)
    ecc_public_key = ecc_private_key.public_key()
    return ecc_private_key, ecc_public_key

def serialize_keys_to_pem(private_key: ec.EllipticCurvePrivateKey, public_key: ec.EllipticCurvePublicKey):
    """Xuất khóa bí mật và khóa công khai sang định dạng PEM tiêu chuẩn."""
    
    # --- 1. Xuất Khóa Bí mật (Private Key) ---
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,            # Định dạng mã hóa ngoài (Base64 wrapper)
        format=serialization.PrivateFormat.PKCS8,       # Định dạng cấu trúc bên trong (PKCS#8)
        encryption_algorithm=serialization.NoEncryption() # Không mã hóa khóa bí mật
    )
    
    # --- 2. Xuất Khóa Công khai (Public Key) ---
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,            # Định dạng mã hóa ngoài (Base64 wrapper)
        format=serialization.PublicFormat.SubjectPublicKeyInfo # Định dạng cấu trúc bên trong (X.509 SubjectPublicKeyInfo)
    )
    
    return private_key_pem, public_key_pem

if __name__ == "__main__":
    # 1. Sinh khóa
    ecc_priv, ecc_pub = generate_ecc_keypair(curve=ec.SECP192R1())
    print("Tao cap khoa ECC tren duong cong SECP192R1 thanh cong.")
    
    # 2. Xuất sang PEM
    priv_pem_output, pub_pem_output = serialize_keys_to_pem(ecc_priv, ecc_pub)

    # 3. Hiển thị
    print("\n=======================================================")
    print("ECC Private Key (PKCS#8 / PEM):\n")
    print(priv_pem_output.decode())
    print("=======================================================")
    print("ECC Public Key (SubjectPublicKeyInfo / PEM):\n")
    print(pub_pem_output.decode())
    print("=======================================================")