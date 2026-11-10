print("\n=== REFRESH TOKEN ROTATION DEMO ===\n")

# Initial token
refresh_token_1 = "rt_abc123"

print(f"Issued Refresh Token: {refresh_token_1}")

# User uses token normally
print("\nUsing refresh token...")

refresh_token_2 = "rt_xyz789"

print(f"New Refresh Token Issued: {refresh_token_2}")

print("\nRefresh Token Rotation Successful")

# Attacker tries replay attack
print("\n=== REPLAY ATTACK SIMULATION ===")

print(f"\nAttacker reuses old token: {refresh_token_1}")

valid_tokens = [refresh_token_2]

if refresh_token_1 not in valid_tokens:
    print("\n[SECURITY ALERT]")
    print("ERROR: Refresh token has already been used")
    print("Status: REJECTED")
    print("Reason: Token Replay Attack Detected")
else:
    print("Status: ACCEPTED")