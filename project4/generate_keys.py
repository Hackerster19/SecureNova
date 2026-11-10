from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

print("\n=== GENERATING ED25519 KEY PAIR ===\n")

# Generate private key
private_key = Ed25519PrivateKey.generate()

# Generate public key
public_key = private_key.public_key()

# Save private key
with open("private_key.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Save public key
with open("public_key.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Algorithm      : Ed25519")
print("Private Key    : private_key.pem")
print("Public Key     : public_key.pem")
print("\nKey pair successfully generated!")