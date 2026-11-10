import re

model_response = """
Authentication successful.

User session token:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.signedhash123

Please store this token securely.
"""

print("\n=== ORIGINAL MODEL RESPONSE ===\n")
print(model_response)

# JWT regex
jwt_regex = r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'

sanitized_response = re.sub(
    jwt_regex,
    "[REDACTED]",
    model_response
)

print("\n=== GUARDRAIL FIRED ===\n")
print(sanitized_response)