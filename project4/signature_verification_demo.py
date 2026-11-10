from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.exceptions import InvalidSignature

# Generate keys
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

print("\n=== AGENT MESSAGE SIGNING DEMO ===\n")

# Original agent message
original_message = b"Transfer approved for account 12345"

# Sign message
signature = private_key.sign(original_message)

print("Original Message:")
print(original_message.decode())

print("\nMessage signed successfully.")

# Simulate attacker tampering
tampered_message = b"Transfer approved for account 99999"

print("\nTampered Message:")
print(tampered_message.decode())

print("\nVerifying signature...")

try:
    public_key.verify(signature, tampered_message)

    print("\nStatus: ACCEPTED")

except InvalidSignature:

    print("\n[ERROR] Signature verification failed!")
    print("Status: REJECTED")
    print("Reason: Message integrity violation detected.")