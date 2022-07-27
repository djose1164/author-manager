# importing libraries
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)  # instantiate the mail class

# configuration of mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "oscarelpollo00@gmail.com"
app.config["MAIL_PASSWORD"] = "fwenugpluonqngfh"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)

# message object mapped to a particular URL ‘/’
@app.route("/")
def index():
    if mail.app is None:
        raise ValueError("Something went wrong")
    msg = Message(
        "Hello", sender=app.config["MAIL_USERNAME"], recipients=["djose1164@gmail.com"]
    )
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"


if __name__ == "__main__":
    app.run(debug=True)
