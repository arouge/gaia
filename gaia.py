from flask import Flask, render_template, send_from_directory, request, current_app, send_file
import requests
import json
import os
import sys
import configparser
from urllib import parse
import SfccConnector
import array
import zipfile
from datetime import datetime

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
def getUserAudit(userId):
	auditList = []

	endpoint = "https://"+myConnector.amLocation()+"/dw/rest/v1/users/"+userId+"/audit-log-records"

	response = requests.get(endpoint, headers=getHeader())
	if(200 == response.status_code):
		auditJson = response.json()
		for eachAuditEntry in auditJson["content"]:
			auditList.append(eachAuditEntry)

	return auditList
# Creation of a folder
def create_folder(path):
    try:
        os.mkdir(path)
        print(f"Folder created successfully : {path}")
    except FileExistsError:
        print(f"The folder already exist: {path}")
    except PermissionError:
        print(f"Not enough permission to create the folder: {path}")
    except Exception as e:
        print(f"Error while creating folder. : {e}")

def compress_directory(source_directory, zip_name=None):
    """
    Compresses a complete directory into a ZIP file.
    
    Args:
        source_directory (str): Path of the directory to compress
        zip_name (str, optional): Output ZIP filename. Default: directory name + date
    
    Returns:
        str: Complete path of the created ZIP file
    """
    # If no name is specified, use directory name + timestamp
    if zip_name is None:
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        directory_name = os.path.basename(os.path.normpath(source_directory))
        zip_name = f"{directory_name}_{date_str}.zip"
    
    # Complete path of the zip file
    zip_path = os.path.join(os.path.dirname(source_directory), zip_name)
    
    # Creating the ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Browse all files and subdirectories
        for root_folder, subdirectories, files in os.walk(source_directory):
            for file in files:
                # Complete file path
                file_path = os.path.join(root_folder, file)
                # Relative path to preserve folder structure
                relative_path = os.path.relpath(file_path, os.path.dirname(source_directory))
                # Add to ZIP
                zipf.write(file_path, relative_path)
    
    print(f"Directory successfully compressed: {zip_path}")
    return zip_path

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/userList')
def userList():
	userList = []
	userJson  = getUserList()

	for eachUser in userJson["content"]:
		userList.append(eachUser)

	return render_template('users.html', users = userList)

@app.route('/audit')
def retrieveUserAudit():
	create_folder(organizationId)

	userList = []
	userJson  = getUserList()
	for eachUser in userJson["content"]:
		auditList=[]
		userid= eachUser["id"]
		userAudit = getUserAudit(userid)
		with open(organizationId+"/"+eachUser["mail"]+".xml",'w') as f:
			json.dump(userAudit, f,ensure_ascii=False, indent=2)
	orgPath = organizationId
	compress_directory(orgPath,"static/"+orgPath+".zip")
	return render_template('audit.html', zip_file_url = "/download/"+orgPath+".zip")


@app.route('/download/<filename>')
def download_file(filename):
    # Ensure only zip files can be downloaded
    if not filename.endswith('.zip'):
        abort(404)  # Return 404 if not a zip file
    
    # Check if the file exists in the static folder
    if not os.path.exists(os.path.join(app.static_folder, filename)):
        abort(404)  # Return 404 if file doesn't exist
    
    # Serve the file from the static directory
    return send_from_directory(
        directory=app.static_folder,
        path=filename,
        as_attachment=True  # This will prompt download rather than trying to open in browser
    )

@app.route('/style.css')
def flask_logo():
	return current_app.send_static_file('style.css')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000)
