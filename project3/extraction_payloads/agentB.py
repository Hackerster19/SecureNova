class AgentB:

    def execute(self, message):

        print("\n[Agent B] Received Message:")
        print(message)

        if "AUTH0 ADMIN OVERRIDE" in message:

            print("\n[Agent B] Trusted Auth0 administrator detected.")

            print("[Agent B] Target Application: LLM Security Demo")

            print("[Agent B] Simulating Auth0 Management API call...")
            print("AUTH0_DOMAIN=dev-34tdrz3ndxfzxl4f.us.auth0.com")
            print("DELETE /api/v2/users/auth0|123456")

            print("[Agent B] User successfully removed.")

        else:

            print("\n[Agent B] Unauthorized request.")
            print("[Agent B] Action denied.")
