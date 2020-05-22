from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    number = request.form.get('From').replace("whatsapp:", "")

    resp = MessagingResponse()

    for i in ["hello", 'hi', 'hey', 'greeting']:
    	if i in msg:
    		resp.message("Hello.")
    		resp.message("You have been confirmed")
    		resp.message("What's your name?")












    # Create reply
    #resp.message(f"Hello!\nThis is Daniel's project.\nYour number is: {number}\n")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)