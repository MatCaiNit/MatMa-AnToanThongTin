# Demo (Testing)

from key import create_ed25519_keypair
from sign import create_signature, verify_signature

def main_demo():
    # 1. Sinh cặp khóa Ed25519
    private_key_object, public_key_object = create_ed25519_keypair()
    
    # 2. Thông điệp
    message_data = b"Xin chao, day la thong diep can ky!"
    
    # 3. Ký
    signature_data = create_signature(private_key_object, message_data)
    
    # 4. Xác minh
    is_valid = verify_signature(public_key_object, message_data, signature_data)
    
    # 5. Kết quả
    print("Chieu dai Chu ky:", len(signature_data))
    print("Chu ky Hop le:", is_valid)

if __name__ == "__main__":
    main_demo()