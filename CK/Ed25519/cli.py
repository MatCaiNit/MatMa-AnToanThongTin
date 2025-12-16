import argparse, sys, os
from key import (
    create_ed25519_keypair,
    export_private_key_pem, export_public_key_pem,
    import_private_key_pem, import_public_key_pem,
)
from sign import create_signature, verify_signature

# ---------------------------------------------------------------------
# CHỨC NĂNG LỆNH (COMMAND EXECUTION FUNCTIONS)
# ---------------------------------------------------------------------

def execute_keygen(arguments):
    """Thực hiện lệnh 'keygen' (Sinh cặp khóa Ed25519)."""
    private_key_object, public_key_object = create_ed25519_keypair()
    
    output_directory = arguments.output_dir
    if output_directory and not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    password_bytes = arguments.password.encode() if arguments.password else None
    
    private_pem_data = export_private_key_pem(private_key_object, password=password_bytes)
    public_pem_data = export_public_key_pem(public_key_object)

    # Xác định đường dẫn file
    output_dir_resolved = output_directory or "."
    private_file_path = os.path.join(output_dir_resolved, arguments.private_filename or "ed25519_private.pem")
    public_file_path = os.path.join(output_dir_resolved, arguments.public_filename or "ed25519_public.pem")
    
    # Ghi file
    with open(private_file_path, "wb") as f:
        f.write(private_pem_data)
    with open(public_file_path, "wb") as f:
        f.write(public_pem_data)

    print(f"Tao file thanh cong:\n  {private_file_path}\n  {public_file_path}")

def execute_sign(arguments):
    """Thực hiện lệnh 'sign' (Ký dữ liệu)."""
    
    # Nạp khóa bí mật
    with open(arguments.private_key_file, "rb") as f:
        private_pem_data = f.read()
        
    password_bytes = arguments.password.encode() if arguments.password else None
    private_key_object = import_private_key_pem(private_pem_data, password=password_bytes)
    
    # Đọc dữ liệu đầu vào
    if arguments.input_data_source == "-":
        input_data = sys.stdin.buffer.read()
    else:
        with open(arguments.input_data_source, "rb") as f:
            input_data = f.read()
            
    # Ký dữ liệu
    signature_data = create_signature(private_key_object, input_data)
    
    # Xuất chữ ký
    output_location = arguments.output_signature_file or "-"
    if output_location == "-":
        sys.stdout.buffer.write(signature_data)
    else:
        with open(output_location, "wb") as f:
            f.write(signature_data)
        print(f"Chu ky da duoc ghi vao {output_location}")

def execute_verify(arguments):
    """Thực hiện lệnh 'verify' (Xác minh chữ ký)."""
    
    # Nạp khóa công khai
    with open(arguments.public_key_file, "rb") as f:
        public_pem_data = f.read()
    public_key_object = import_public_key_pem(public_pem_data)
    
    # Đọc dữ liệu đầu vào và chữ ký
    input_data = sys.stdin.buffer.read() if arguments.input_data_source == "-" else open(arguments.input_data_source, "rb").read()
    signature_data = sys.stdin.buffer.read() if arguments.signature_data_source == "-" else open(arguments.signature_data_source, "rb").read()
    
    # Xác minh
    is_valid = verify_signature(public_key_object, input_data, signature_data)
    
    # Kết quả và mã thoát
    print("VALID" if is_valid else "INVALID")
    sys.exit(0 if is_valid else 1)

def main_cli():
    parser = argparse.ArgumentParser(description="Cong cu dong lenh cho Chu ky so Ed25519")
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    # ------------------ Lệnh: keygen ------------------
    parser_keygen = subparsers.add_parser("keygen", help="Sinh cap khoa Ed25519")
    parser_keygen.add_argument("--out-dir", default=".", dest="output_dir", help="Thu muc xuat file khoa")
    parser_keygen.add_argument("--private", default="ed25519_private.pem", dest="private_filename", help="Ten file khoa bi mat")
    parser_keygen.add_argument("--public", default="ed25519_public.pem", dest="public_filename", help="Ten file khoa cong khai")
    parser_keygen.add_argument("--password", help="Mat khau de ma hoa file PEM khoa bi mat")
    parser_keygen.set_defaults(func=execute_keygen)

    # ------------------ Lệnh: sign --------------------
    parser_sign = subparsers.add_parser("sign", help="Tao chu ky cho du lieu dau vao")
    parser_sign.add_argument("--private", required=True, dest="private_key_file", help="File PEM khoa bi mat de ky")
    parser_sign.add_argument("--password", help="Mat khau giai ma PEM (neu co)")
    parser_sign.add_argument("--input", default="-", dest="input_data_source", help="Du lieu dau vao (file hoac '-' cho stdin)")
    parser_sign.add_argument("--output", default="-", dest="output_signature_file", help="File xuat chu ky hoac '-' cho stdout")
    parser_sign.set_defaults(func=execute_sign)

    # ------------------ Lệnh: verify ------------------
    parser_verify = subparsers.add_parser("verify", help="Xac minh chu ky so")
    parser_verify.add_argument("--public", required=True, dest="public_key_file", help="File PEM khoa cong khai de xac minh")
    parser_verify.add_argument("--input", default="-", dest="input_data_source", help="Du lieu goc dau vao (file hoac '-' cho stdin)")
    parser_verify.add_argument("--signature", default="-", dest="signature_data_source", help="File chu ky hoac '-' cho stdin")
    parser_verify.set_defaults(func=execute_verify)

    arguments = parser.parse_args()
    arguments.func(arguments)

if __name__ == "__main__":
    main_cli()