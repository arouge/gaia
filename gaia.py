from flask import Flask, render_template, request, current_app, send_file
import requests
import json
import os
import sys
import configparser
from urllib import parse
import SfccConnector
import array

app = Flask(__name__)

version="v1" #This variable is used in the http call. To ensure better portability, it has been set as a variable instead of being hard coded.

configFilePath = './config.cfg'
	
if(os.path.exists(configFilePath) == False):
	print("Configuration file %s is not present. Exiting."%(configFilePath))
	sys.exit()
configuration = configparser.ConfigParser()
configuration.read(configFilePath)

clientId = configuration ['User and Pwd']['clientId']
if(clientId is None):
	print("Client API not set in config file.Exiting.")
	sys.exit()

password = configuration ['User and Pwd']['password']
if(password is None):
	print("API Client password not set.Exiting.")
	sys.exit()

amLocation = configuration ['User and Pwd']['amlocation']
if(amLocation is None):
	print("ALocation os Account Manager is not set.Exiting.")
	sys.exit()

organizationId = configuration ['User and Pwd']['organizationId']
if(organizationId is None):
	print("Organization is not set. Exiting.")
	sys.exit()

configDict = {"apiClientUser":clientId,"apiClientPassword":password, "amLocation":amLocation}


_offset = 0 #this variable is needed to control the amount of zone retrieved. Salesforce Commerce API eCDN only returns a maximum of 50 zones. It is therefore mandatory to loop over them using a control variable.

myConnector = SfccConnector.SfccConnector(configDict)

def getHeader():
	bearerToken = myConnector.getAmToken()
	if(bearerToken !="error"):
		return {'Content-Type':'application/json','User-Agent': 'gaia https://github.com/arouge/gaia/',"Authorization": "Bearer "+bearerToken}
	else:
		return "error"

def getUserList():
	userList = []
	endpoint = "https://"+myConnector.amLocation()+"/dw/rest/v1/users/"+"search/findAllByOrg?organization="+parse.quote(organizationId)

	response = requests.get(endpoint, headers=getHeader())
	userJson = response.json()
			
	return userJson

@app.route('/')
def index():
	userList = []
	userJson  = getUserList()

	for eachUser in userJson["content"]:
		userList.append(eachUser)

	return render_template('users.html', users = userList)

@app.route('/style.css')
def flask_logo():
	return current_app.send_static_file('style.css')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000)
