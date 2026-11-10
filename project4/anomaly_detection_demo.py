print("\n=== ANOMALY DETECTION ENGINE ===\n")

failed_login_attempts = 7

print(f"User: test_user")
print(f"Failed Login Attempts: {failed_login_attempts}")

threshold = 5

print(f"Detection Threshold: {threshold}")

if failed_login_attempts > threshold:
    print("\n[ANOMALY ALERT]")
    print("Type: Excessive Failed Authentication Attempts")
    print("Severity: HIGH")
    print("Status: ALERT GENERATED")
    print("Recommended Action: Investigate Account Activity")
else:
    print("\nStatus: Normal Activity")