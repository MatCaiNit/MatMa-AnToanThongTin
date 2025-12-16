# Generate keypair

Command: python cli.py keygen --out-dir keys --password yourpass

# Sign a file

Command: python cli.py sign --private keys/ed25519_private.pem --password yourpass --input message.txt --output message.sig

# Verify signature

Command: python cli.py verify --public keys/ed25519_public.pem --input message.txt --signature message.sig

# Stream via pipes

Command: cat message.txt | python cli.py sign --private keys/ed25519_private.pem --password yourpass > message.sig