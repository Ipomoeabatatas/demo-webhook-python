    # /index.py

from flask import Flask, request, jsonify, render_template
import os
#import dialogflow
import requests
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

### PLEASE MODIFY THE NEXT TWO LINES TO CUSTOMIZE TO YOUR OWN GOOGLESHEET ###

KEY_FILE = "PythonToSheet-46f0bfa4bace.json"        
GOOGLE_SHEET = "OneChatBotCourse"                   

##

SCOPE = ['https://spreadsheets.google.com/feeds',  'https://www.googleapis.com/auth/drive']

app = Flask(__name__)

## The default route shows a web page . It use for testing only
@app.route('/')
def index():
    return ('Flask Application Is Deployed successful. It is not free from bug yet')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    action = data['queryResult']['action']
    
    if action == "test_connection" :
        return test_connection(data)
    elif action == "register_participants" :
        return register_participants(data)
    elif action == "request_callback" :
        return request_callback(data)
    elif action == "dummy_action" :
        return funct_dummy(data)
    else:
        return handle_unknown_action(data)

########################################################################
def test_connection(data):
   replytext = "Hi there. You have made a successful connection to the webhook. The webhook has received your utterance <" + data['queryResult']['queryText'] + ">"
   response = {
#        "fulfillmentText": " " ,
        "fulfillmentMessages" : [{"text" : {"text" : [ replytext ]}}]}    
   return jsonify(response)  


########################################################################
def handle_unknown_action(data):
   response = {}
   replytext = "Oh dear! Your intent <" + data['queryResult']['intent']['displayName'] + "> for action <" + data['queryResult']['action']  + "> is not implemented in the webhook yet. Please disable fulfillment for the intent."
   response["fulfillmentText"] = replytext
   return jsonify(response)            
   

   
########################################################################
def register_participants(data):
   shirtsize = data['queryResult']['parameters']['shirtsize']
   name =  data['queryResult']['parameters']['person']['name']
   department = data['queryResult']['parameters']['department']
##   querytext = data['queryResult']['queryText']

   creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, SCOPE)
   client = gspread.authorize(creds)
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
   sheet = client.open(GOOGLE_SHEET).worksheet('eventregisteration')
# Extract of the values
   values = [name, department, shirtsize]
   sheet.append_row(values, value_input_option='RAW')
# Prepare a response
   response = {}
   replytext = "Hi "  + name + ", Thanks for registrating for the event. We will reserve shirt size " + shirtsize + " for you. We've got your information in the spreadsheet. Please collect at HR Department. "
   response["fulfillmentText"] = replytext
   return jsonify(response)  




#######################################################################

def request_callback(data):
   phone = data['queryResult']['parameters']['phone-number']
   name =  data['queryResult']['parameters']['person']['name']
   querytext = data['queryResult']['queryText']

   creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, SCOPE)
   client = gspread.authorize(creds)
   # Find a workbook by name and open the first sheet
   # Make sure you use the right name here.
   sheet = client.open(GOOGLE_SHEET).worksheet('callback')
   # Extract and print all of the values
   values = [name, phone, querytext]
   sheet.append_row(values, value_input_option='RAW')
   # Prepare a response
   response = {}
   replytext = "Hi "  + name + ", sorry I can't help you now. But, someone will call you back at " + phone + ". Talk to you soon. We've got your information in the spreadsheet."
   response["fulfillmentText"] = replytext
   return jsonify(response)  



########################################################################

def funct_dummy(data):
   response["fulfillmentText"] = "placeholder"
   return jsonify(response) 
   
   
########################################################################
   
# run Flask app
if __name__ == "__main__":
        app.run()