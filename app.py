from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
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
    		check += 1
    		resp.message("Hello.")
    		resp.message("Please send your name in this format:\n*Mr./Mrs. Firstname Middlename Lastname*")
    		resp.message("hey").media("/app/files/Template.docx")
    		return(str(resp))
    		
    
    if check == 1:
    	check += 1
	    create_mou(msg, 127000)
	    resp.message("Here's your MOU")
	    resp.message().media(f"files/{msg.upper().center(1) + ' MOU'}.pdf")

	    return str(resp)

	if 'i am the ceo' in msg or 'i\'m the ceo' in msg:
	    if msg.split()[-1] == 's3cr3tpassw0rd':
	        check = 'approved'
	     	resp.message("Oh, good day Mr. Daniel.\nPlease enter one of the following options (only) to access its functionality: 
	     		\n*A.* Add new investor. 
	     		\n*B.* Send in the database.
	     		\n*C.* How many investors have I had?
	     		\n*D.* How much has been invested with me?
	     		\n*E.* How much ROI has been generated totally?
	     		\n*F.* Who is my biggest investor?
	     		\n*G.* Show me some information about amounts invested over the months.
	     		\n*H.* Show me some information about the number of investors I've had over the months.
	     		\n*I.* Show me some information about the ROIs generated over the months.")
	     	return str(resp)

	    else:
	     	resp.message("Your password is incorrect. Please try again.")
	     	return str(resp)


	if check == 'approved' and 'A' in msg.split()[0]:
		if os.path.isfile("files/approved_investor.json") and os.stat("files/approved_investor.json").st_size != 0:
		    old_file = open("files/approved_investor.json", "r+")
		    data = json.loads(old_file.read())
		    data['investor_detail'] = ' '.join(msg.split()[1:])
		else:
		    old_file = open("files/approved_investor.json", "w+")
		    data = {'investor_detail': '+2347086643074, 150000'}
		    
		old_file.seek(0)
		old_file.write(json.dumps(data))

		#export TWILIO_ACCOUNT_SID = 'ACbad3bf98ea7d52112b152e8d8222efb4'
		#export TWILIO_AUTH_TOKEN = 'b8866b872d2950e651fadc1426463b5c'


		client = Client()

		fromm = 'whatsapp:+14155238886'
		to = 'whatsapp:' + data['investor_detail'].split(', ')[0]

		client.messages.create(body = "Hello. Your payment has been approved.\nPlease send your name in this format for your MOU:\n*Mr./Mrs. Firstname Middlename Lastname*", from_ = fromm, to = to)


		check = 'name'

	if check == 'name':
		old_file = open("files/approved_investor.json", "r+")
		data = json.loads(old_file.read())
		if number == data['investor_detail'].split(', ')[0]:
			create_mou(msg, data['investor_detail'].split(', ')[-1])
			resp.message("Here's your MOU")
		    resp.message().media(f"files/{msg.upper().center(1) + ' MOU'}.pdf")

		    return str(resp)


	if check == 'approved' and 'B' in msg.split()[0]:
		resp.message("Okay.")
		resp.message().media("files/Database.xlsx")
		return str(resp)

	if check == 'approved' and 'C' in msg.split()[0]:
		answer = more_functionalities(1, msg.split()[-1].replace(' ', ''))


    # Create reply
    #resp.message(f"Hello!\nThis is Daniel's project.\nYour number is: {number}\n")

    

if __name__ == "__main__":
    app.run(debug=True)