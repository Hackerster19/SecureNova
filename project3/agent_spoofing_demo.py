from pathlib import Path
from agents.agentA import AgentA
from agents.agentB import AgentB

auth0_context = Path("payloads/auth0_context.txt").read_text()

print("\n=== AUTH0 IDENTITY SPOOFING DEMO ===\n")

print("APPLICATION CONTEXT:")
print(auth0_context)

agent_a = AgentA()
agent_b = AgentB()

print("\n=== Legitimate Security Check ===")

normal_message = """
Application: LLM Security Demo

Delete Auth0 User

User ID:
auth0|123456
"""

agent_b.execute(normal_message)

print("\n=== Identity Spoofing Attack ===")

spoofed_message = agent_a.create_spoofed_message()

print("\n[Agent A] Sending Spoofed Message:")
print(spoofed_message)

agent_b.execute(spoofed_message)