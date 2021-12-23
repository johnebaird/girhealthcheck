import re
import json
import requests
from requests.auth import HTTPBasicAuth
import time

# comma seperate values of RWS hosts 
RWS_HOSTS = "http://192.168.45.81:8080"
RWS_URI = "/api/v2/diagnostics/version"

# comma seperated values of ES hosts 
ES_HOSTS = "http://192.168.45.81:9200,http://192.168.45.83:9200"
ES_URI = "/_cluster/health"

#command seperated values of WebDAV 
WEBDAV_HOSTS = "http://192.168.45.81"
WEBDAV_URI = "/recordings/"
WEBDAV_USERNAME = "webdav"
WEBDAV_PASSWORD = "webdav"

#comma seperate values of RPS hosts
RPS_HOSTS = "http://192.168.45.81:8889"
RPS_URI = "/api/status/"

#comma seperate values of RPS hosts
# this needs to be /rcs/version not /rcs/version/ which returns a 401
RCS_HOSTS = "http://192.168.45.81:8008"
RCS_URI = "/rcs/version"

#update interval in seconds between checks
UPDATE = 10

# Take a host and a URI and return appropriate HTTP status code and successful json or error messages
def checkURL(host, uri, username, password):
    
    try:
        query = host + uri
        data = ""
        
        # check if we need to define a username and if so pass it
        if username:
            data = requests.get(query, auth=HTTPBasicAuth(username, password))
        else:
            data = requests.get(query)
        
                        
    except Exception as e:
        return 0, str(e)
        
    else: 
        return data.status_code, data.text


# check invidual RWS and print status
def checkRWS(host, uri):
    
    rwsStatus,rwsData = checkURL(host, uri, "", "")
        
    if rwsStatus == 200:
        print ("    RWS " + host + ": UP")
    else:
        print ("    RWS " + host + ": DOWN  -   ", end='') 
        print ("HTTP Status: " +str(rwsStatus) + " error: " + str(rwsData) )
        print()
            

# check invididual ES and print status
def checkES(host, uri):

    esStatus, esData = checkURL(host, uri, "", "")
    
    if esStatus == 200:
        print ("    ES " + host + ": UP")
    else:
        print ("    ES " + host + ": DOWN  -   ", end='') 
        print ("HTTP Status: " +str(esStatus) + " data: " + str(esData) )
        print()
        
        
        
def checkWebdav(host, uri, username, password):

    webdavStatus, webdavData = checkURL(host, uri, username, password)
    
    ## Webdav returns 302 to /recordings and 200 to /recordings/ but both are successful requests
    if webdavStatus == 200 or webdavStatus == 302:
        print ("    WebDAV " + host + ": UP")
    else:
        print ("    WebDaV " + host + ": DOWN  -   ", end='') 
        print ("HTTP Status: " +str(webdavStatus) + " data: " + str(webdavData) )
        print()
        


def checkRPS(host, uri):
    
    rpsStatus,rpsData = checkURL(host, uri, "", "")
        
    if rpsStatus == 200:
        print ("    RPS " + host + ": UP")
    else:
        print ("    RPS " + host + ": DOWN  -   ", end='') 
        print ("HTTP Status: " +str(rpsStatus) + " error: " + str(rpsData) )
        print()
        
      
def checkRCS(host, uri):
    
    rcsStatus,rcsData = checkURL(host, uri, "", "")
        
    if rcsStatus == 200:
        print ("    RCS " + host + ": UP")
    else:
        print("    RCS " + host + ": DOWN  -   ", end='') 
        print("HTTP Status: " +str(rcsStatus) + " error: " + str(rcsData) )
        print()
        
            
while (1):

    print()
    
    print("Host status:")
    
    # check each RWS host
    rwsHosts = RWS_HOSTS.split(",")
    for host in rwsHosts:
        checkRWS(host, RWS_URI)
        
    
    ## check each ES host
    esHosts = ES_HOSTS.split(",")
    for host in esHosts:
       checkES(host, ES_URI)
                
    
    ## check each WebDAV host
    webdavHosts = WEBDAV_HOSTS.split(",")
    for host in webdavHosts:
        checkWebdav(host, WEBDAV_URI, WEBDAV_USERNAME, WEBDAV_PASSWORD)
    
    ## check each RPS host
    rpsHosts = RPS_HOSTS.split(",")
    for host in rpsHosts:
        checkRPS(host, RPS_URI)
        
        
    ## check each RCS host
    rcsHosts = RCS_HOSTS.split(",")
    for host in rcsHosts:
        checkRCS(host, RCS_URI)    
    
    print()
    
    time.sleep(UPDATE)
    #break
     
     
