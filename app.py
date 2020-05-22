from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from investment_project import *

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

    check = 0

    for i in ["hello", 'hi', 'hey', 'greeting']:
    	if i.lower() in msg or i.upper() in msg or i.title() in msg:
    		resp.message("Hello.")
    		resp.message("Please send your name in this format:")
    		resp.message("*Firstname Middlename Lastname*")
    		check = 1

    		

    if check == 1:
	    create_mou(msg, 127000)
	    resp.message("Here's your MOU")
	    resp.message().media(f"files/{name + ' MOU'}.docx")





    # Create reply
    #resp.message(f"Hello!\nThis is Daniel's project.\nYour number is: {number}\n")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)