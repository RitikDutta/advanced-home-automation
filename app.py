from flask import Flask, request, make_response, jsonify
import requests
from flask import jsonify
from flask import make_response
import json

# import dialogflow_handler
# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
	url = "https://io.adafruit.com/api/v2/nisam/feeds/relay1/data"
	headers = {"X-AIO-Key": "aio_tZwT41kNnCUq2MfgUmQfrbgsz0TW"}
	r = requests.post(url, data={"value":"OFF"}, headers=headers)
	data = r.json()
	return 'Hello World!'


# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
	# quotations = json.load(open("quotations.json",encoding="utf-8_sig"))
	headers = {"X-AIO-Key": "aio_tZwT41kNnCUq2MfgUmQfrbgsz0TW"}
	url1 = "https://io.adafruit.com/api/v2/nisam/feeds/relay1/data"
	url2 = "https://io.adafruit.com/api/v2/nisam/feeds/relay2/data"
	resget1 = requests.get('https://io.adafruit.com/api/v2/nisam/feeds/relay1?x-aio-key=aio_tZwT41kNnCUq2MfgUmQfrbgsz0TW')
	r1 = resget1.json()
	relay1_value = r1['last_value']
	resget2 = requests.get('https://io.adafruit.com/api/v2/nisam/feeds/relay2?x-aio-key=aio_tZwT41kNnCUq2MfgUmQfrbgsz0TW')
	r2 = resget2.json()
	relay2_value = r2['last_value']
	crypto = requests.get('https://api.wazirx.com/api/v2/tickers')
	r_crypto = crypto.json()

	
	req = request.get_json()
	a = req['handler']['name']
	b = req['intent']['params']['currency1']['resolved']
	speech = ""
	if a=='relay1on':
		if relay1_value == "ON":
			speech = "Relay 1 already on"
		else:
			r = requests.post(url1, data={"value":"ON"}, headers=headers)
			data = r.json()
			speech = "Relay 1 Turned on"
	elif a == 'relay1off':
		if relay1_value == "OFF":
			speech = "Relay 1 already off"
		else:
			r = requests.post(url1, data={"value":"OFF"}, headers=headers)
			data = r.json()
			speech = "Relay 1 Turned off"
	elif a == 'relay2on':
		if relay2_value == "ON":
			speech = "Relay 2 already on"
		else:
			r = requests.post(url2, data={"value":"ON"}, headers=headers)
			data = r.json()
			speech = "Relay 2 Turned on"
	elif a == 'relay2off':
		if relay2_value == "OFF":
			speech = "Relay 2 already off"
		else:
			r = requests.post(url2, data={"value":"OFF"}, headers=headers)
			data = r.json()
			speech = "Relay 2 Turned off"
	elif a=='crypto':
		speech = "value of {0} is {1}".format(b, r_crypto[b]['last'])

	reply = {"candidates": [{"first_simple": {"variants": [{"speech": "Enter "}]}}]}
	# print(b)
	return {
  "session": {
    "id": "example_session_id",
    "params": {}
  },
  "prompt": {
    "override": 'false',
    "firstSimple": {
      "speech": speech,
      "text": ""
    }
  }
}


	

# # run the app
if __name__ == '__main__':
   app.run()
