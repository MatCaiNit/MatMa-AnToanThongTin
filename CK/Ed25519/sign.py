# sign.py (Logic Ký & Xác minh)

from cryptography.hazmat.primitives.asymmetric import ed25519
import hashlib
import typing

def create_signature(private_key_object: ed25519.Ed25519PrivateKey, message_data: bytes) -> bytes:
    """Trả về chữ ký 64-byte cho dữ liệu thông điệp."""
    return private_key_object.sign(message_data)

def verify_signature(public_key_object: ed25519.Ed25519PublicKey, message_data: bytes, signature_data: bytes) -> bool:
    """Trả về True nếu chữ ký hợp lệ, False nếu không."""
    try:
        public_key_object.verify(signature_data, message_data)
        return True
    except Exception:
        return False

# Ký/Xác minh cho dữ liệu lớn (Stream/File)

def create_stream_signature(private_key_object: ed25519.Ed25519PrivateKey, stream_iterator: typing.Iterable[bytes], hash_algorithm="sha512") -> bytes:
    """Ký dữ liệu lớn bằng cách hash nội dung và ký lên bản tóm tắt (digest)."""
    hasher = hashlib.new(hash_algorithm)
    for chunk in stream_iterator:
        hasher.update(chunk)
    data_digest = hasher.digest()
    # Ký lên digest, không phải toàn bộ stream
    return private_key_object.sign(data_digest)

def verify_stream_signature(public_key_object: ed25519.Ed25519PublicKey, stream_iterator: typing.Iterable[bytes], signature_data: bytes, hash_algorithm="sha512") -> bool:
    """Xác minh chữ ký trên bản tóm tắt (digest) của dữ liệu stream."""
    hasher = hashlib.new(hash_algorithm)
    for chunk in stream_iterator:
        hasher.update(chunk)
    data_digest = hasher.digest()
    
    try:
        public_key_object.verify(signature_data, data_digest)
        return True
    except Exception:
        return False