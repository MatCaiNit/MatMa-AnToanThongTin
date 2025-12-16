import argparse
from key import generate_keypair, export_private_seed, export_public_key
from sign import sign, verify
from utils import decode_point

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="cmd", required=True)

# keygen
k = sub.add_parser("keygen")
k.add_argument("--seed-file")
k.add_argument("--pub-file")

# sign
s = sub.add_parser("sign")
s.add_argument("--priv")
s.add_argument("--infile")
s.add_argument("--sigfile")

# verify
v = sub.add_parser("verify")
v.add_argument("--pub")
v.add_argument("--infile")
v.add_argument("--sigfile")

args = parser.parse_args()

if args.cmd == "keygen":
    seed, a, A = generate_keypair()
    if args.seed_file:
        with open(args.seed_file,"wb") as f:
            f.write(export_private_seed(seed))
        print("Private seed saved to:", args.seed_file)
    if args.pub_file:
        with open(args.pub_file,"wb") as f:
            f.write(export_public_key(A))
        print("Public key saved to:", args.pub_file)
    else:
        print("Public key (hex):", export_public_key(A).hex())

elif args.cmd == "sign":
    with open(args.priv,"rb") as f:
        seed = f.read()
    _, a, A = generate_keypair(seed)
    with open(args.infile,"rb") as f:
        msg = f.read()
    sig = sign(a, A, msg)
    with open(args.sigfile,"wb") as f:
        f.write(sig)
    print("File signed:", args.sigfile)

elif args.cmd == "verify":
    with open(args.pub,"rb") as f:
        A_enc = f.read()
    A = decode_point(A_enc)
    with open(args.infile,"rb") as f:
        msg = f.read()
    with open(args.sigfile,"rb") as f:
        sig = f.read()
    if verify(A, msg, sig):
        print("VALID")
    else:
        print("INVALID")
