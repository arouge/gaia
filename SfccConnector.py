#!/usr/bin/python3
import time
import sys
import requests
from os import error
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

class SfccConnector:
        
    def tokenValidity(self):
        return self.__expiresAt

    def organizationID(self):
        return self.__organizationId

    def getAmToken(self):
        if(datetime.now()>=self.__expiresAt):
            tokenisValid = False
            _data={"grant_type":"client_credentials"}
            while (tokenisValid == False):
                token=requests.post(self.__sfccAuth, data=_data, auth=HTTPBasicAuth(self.__sfccUsername,self.__sfccPassword))
                if(200 == token.status_code):
                    tokenisValid = True
                elif (401 == token.status_code):
                    print("Authorization failed. Error 401 Exiting")
                    sys.exit()
                else:
                    print("Can not get the token. Retrying in 2 seconds")
                    time.sleep(2)

            endpointToken = token.json()
            self.__expiresAt=datetime.now()+timedelta(seconds=endpointToken["expires_in"]-10)
            self.__amToken = endpointToken["access_token"]
            self.__headers = {'User-Agent': 'sfcc-waf-ci (python 3.x)',"Authorization": "Bearer "+self.__amToken}
            print("Token refresh was needed.")
        else:
            print("Token refresh was NOT needed.")
                      
        return self.__amToken
    
    def amLocation(self):
        return self.__amLocation

    def __init__(self,config):
        self.__version='v1'
        self.__amLocation = config["amLocation"]
        self.__sfccAuth="https://"+self.__amLocation+"/dwsso/oauth2/access_token"
        #self.__sfccRealm = config["realmID"]
        #self.__sfccEnv = config["environment"]
        #self.__shortCode = config["shortCode"] 
        self.__sfccUsername = config["apiClientUser"] 
        self.__sfccPassword = config["apiClientPassword"]
        #self.__organizationId = 'f_ecom_'+self.__sfccRealm+'_'+self.__sfccEnv
        self.__expiresAt = datetime.now()
        self.__headers=''
        #self.__requiredScopes = config["requiredScopes"]
        self.__amToken=''
