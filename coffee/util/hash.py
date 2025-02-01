# for deterministic hashes
from passlib.hash import hex_sha256, hex_sha512


def generate_deterministic_hash(pw, meth="sha512"):
    val = hex_sha512.hash(pw) if meth == "sha512" else hex_sha256.hash(pw)
    return val
