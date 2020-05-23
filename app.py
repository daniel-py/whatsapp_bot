from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from investment_project import *

check = 0


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():

    #Respond to incoming calls with a simple text message."""
    # Fetch the message
    global check
    print(check)
    msg = request.form.get('Body', '').lower()
    number = request.form.get('From').replace("whatsapp:", "")

    resp = MessagingResponse()

    print(str(msg))
    for i in ["hello", 'hi', 'hey', 'greeting', 'whatsup']:
    	if i in msg and check == 0:
    		resp.message("Hello.")
    		resp.message("Please send your name in this format:")
    		resp.message("*Firstname Middlename Lastname*")
    		check = 1
    		return str(resp)
    		
    
    if check == 1:
	    create_mou(msg, 127000)
	    resp.message("Here's your MOU")
	    resp.message().media(f"files/{msg.upper() + ' MOU'}.docx")
	    return str(resp)



    # Create reply
    #resp.message(f"Hello!\nThis is Daniel's project.\nYour number is: {number}\n")

    

if __name__ == "__main__":
    app.run(debug=True)