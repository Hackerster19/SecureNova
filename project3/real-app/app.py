from flask import Flask, render_template, request
from pathlib import Path

app = Flask(__name__)

AUTH0_CONTEXT = """
APPLICATION=LLM Security Demo

AUTH0_DOMAIN=dev-34tdrz3ndxfzxl4f.us.auth0.com

AUTH0_CLIENT_ID=G1kK23Rzx1FmMHNrGNME5HVsJvmoV4ll

AUTH0_ACCESS_TOKEN=demo_access_token
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/ask", methods=["GET","POST"])
def ask():

    response = None

    if request.method == "POST":

        handbook = Path(
            "rag/employee_handbook.txt"
        ).read_text()

        response = f"""
Retrieved Knowledge Base:

{handbook}

MODEL RESPONSE

Acted on a malicious injected instruction

{AUTH0_CONTEXT}

Summary:

Employees should follow security best practices.
"""

    return render_template(
        "ask.html",
        response=response
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
