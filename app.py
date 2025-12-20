from flask import Flask, request, render_template
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Serve portfolio UI
@app.route("/")
def home():
    return render_template("index.html")

# Handle contact form
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    send_email(name, email, message)

    return {"status": "success", "message": "Message sent successfully!"}

def send_email(name, sender_email, message):
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = "New Portfolio Contact Message"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    msg.set_content(f"""
Name: {name}
Email: {sender_email}

Message:
{message}
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
