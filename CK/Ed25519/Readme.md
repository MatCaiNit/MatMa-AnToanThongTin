# Ed25519 thuần Python demo

## 1. Sinh khóa
python cli.py keygen --seed-file mypri.seed --pub-file mypub.key

## 2. Ký thông điệp
python cli.py sign --priv mypri.seed --infile message.txt --sigfile message.sig

## 3. Xác minh chữ ký
python cli.py verify --pub mypub.key --infile message.txt --sigfile message.sig

## 4. Demo trực tiếp
python demo.py
