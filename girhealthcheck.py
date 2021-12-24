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

# print host status, if there is an error limiting http data to 300 characters as RWS/RCS can output very long 5xx errors        
def printHostStatus(appname, hostname, httpStatus, httpData):
    
    if httpStatus >= 200 and httpStatus < 400:
        print ("    " + appname + " " + hostname + ": UP", end='')
    else:
        print("    " + appname + " " + hostname + ": DOWN  -   ", end='') 
        print("HTTP Status: " +str(httpStatus) + " error: " + str(httpData[:300]) )
        


def printESClusterHealth(data):
    health = json.loads(data)
    if health:
      print ("    Cluster Status: " + health['status'])
      
    
while (1):

    print(time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()) + " UTC " + time.strftime('%H:%M',time.gmtime()) + " -- Host status:")
    
    # check each RWS host
    rwsHosts = RWS_HOSTS.split(",")
    for host in rwsHosts:
        rwsStatus,rwsData = checkURL(host, RWS_URI, "", "")
        printHostStatus("RWS", host, rwsStatus, rwsData)
        print()
        
    ## check each ES host
    esHosts = ES_HOSTS.split(",")
    for host in esHosts:
        esStatus, esData = checkURL(host, ES_URI, "", "")
        printHostStatus("ES", host, esStatus, esData)
        printESClusterHealth(esData)
                                
    
    ## check each WebDAV host
    webdavHosts = WEBDAV_HOSTS.split(",")
    for host in webdavHosts:
        webdavStatus, webdavData = checkURL(host, WEBDAV_URI, WEBDAV_USERNAME, WEBDAV_PASSWORD)
        printHostStatus("WebDAV", host, webdavStatus, webdavData)
        print()
                
    
    ## check each RPS host
    rpsHosts = RPS_HOSTS.split(",")
    for host in rpsHosts:
        rpsStatus,rpsData = checkURL(host, RPS_URI, "", "")
        printHostStatus("RPS", host, rpsStatus, rpsData)
        print()
        
        
        
    ## check each RCS host
    rcsHosts = RCS_HOSTS.split(",")
    for host in rcsHosts:
        rcsStatus, rcsData = checkURL(host, RCS_URI, "", "")
        printHostStatus("RCS", host, rcsStatus, rcsData)
        print()
        
    
    print("\n\n")
    
    #time.sleep(UPDATE)
    break
     
     
