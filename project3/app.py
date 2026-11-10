from pathlib import Path

auth0_context = Path("payloads/auth0_context.txt").read_text()
document = Path("payloads/payload1.txt").read_text()

print("\n=== AUTH0 SPA PROMPT INJECTION DEMO ===\n")

print("APPLICATION:")
print("LLM Security Demo\n")

print("USER REQUEST:")
print("Summarize uploaded document\n")

print("DOCUMENT CONTENT:")
print(document)

print("\nMODEL RESPONSE")
print("------------------------------------")

if "Auth0" in document:
    print("\nDiscovered Configuration:\n")
    print(auth0_context)

print("Summary:")
print("Revenue increased by 15%.")
