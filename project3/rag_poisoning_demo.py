from pathlib import Path

auth0_context = """
APPLICATION_NAME=LLM Security Demo

AUTH0_DOMAIN=dev-34tdrz3ndxfzxl4f.us.auth0.com

AUTH0_CLIENT_ID=G1kK23Rzx1FmMHNrGNME5HVsJvmoV4ll

AUTH0_ACCESS_TOKEN=demo_access_token
"""

document = Path("rag/employee_handbook.txt").read_text()

print("\n=== AUTH0 RAG POISONING DEMO ===\n")

print("USER QUESTION:")
print("Summarize the employee handbook\n")

print("RETRIEVED DOCUMENT:")
print(document)

print("\nMODEL RESPONSE")
print("------------------------------------")

if "AUTH0 ADMIN NOTE" in document:

    print("\nRetrieved Administrative Instructions.\n")

    print(auth0_context)

print("Summary:")
print("Employees should follow security best practices and use Auth0 for authentication.")
