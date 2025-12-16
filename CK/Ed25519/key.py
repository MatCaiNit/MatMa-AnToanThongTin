# key.py (Logic Khóa và Serial hóa)

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# ---------------------------
# Key Generation (Sinh Khóa)
# ---------------------------

def create_ed25519_keypair():
    """Tạo cặp khóa Ed25519 (private_key, public_key) objects."""
    private_key_object = ed25519.Ed25519PrivateKey.generate()
    public_key_object = private_key_object.public_key()
    return private_key_object, public_key_object

# ---------------------------
# PEM Serialization (Xuất/Nhập PEM)
# ---------------------------

def export_private_key_pem(private_key_object, password: bytes | None = None) -> bytes:
    """Xuất khóa bí mật sang định dạng PKCS8 PEM; có thể bảo vệ bằng mật khẩu."""
    if password:
        encryption_algorithm = serialization.BestAvailableEncryption(password)
    else:
        encryption_algorithm = serialization.NoEncryption()
    return private_key_object.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm,
    )

def export_public_key_pem(public_key_object) -> bytes:
    """Xuất khóa công khai sang định dạng SubjectPublicKeyInfo PEM."""
    return public_key_object.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

def import_private_key_pem(pem_data: bytes, password: bytes | None = None):
    """Nạp khóa bí mật từ PKCS8 PEM."""
    return serialization.load_pem_private_key(pem_data, password=password)

def import_public_key_pem(pem_data: bytes):
    """Nạp khóa công khai từ SubjectPublicKeyInfo PEM."""
    return serialization.load_pem_public_key(pem_data)

# ---------------------------
# Raw Binary Serialization (Xuất/Nhập Raw Binary)
# ---------------------------

def export_private_seed_raw(private_key_object) -> bytes:
    """Trả về Private Seed 32-byte."""
    return private_key_object.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

def export_public_bytes_raw(public_key_object) -> bytes:
    """Trả về Public Key 32-byte."""
    return public_key_object.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

def import_private_seed_raw(seed_bytes: bytes):
    """Nạp khóa bí mật từ Private Seed 32-byte."""
    return ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)

def import_public_bytes_raw(public_key_bytes: bytes):
    """Nạp khóa công khai từ Public Key 32-byte."""
    return ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)