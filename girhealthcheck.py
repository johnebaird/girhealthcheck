import os
import re
import json
import requests
from requests.auth import HTTPBasicAuth
import time

# comma seperate values of RWS/ES/WEBDAV/RPS/RCS/VP hosts to check pulled from environment variables
# *_HOSTS can support multiple hosts if seperated by commas, in case of RWS/ES the first host is also used to query for call totals
# *_URI can be overridden by environment vars if needed for some reason
# RWS_USER / WEBDAV_USER needs to be set for authentication for these services
#

RWS_HOSTS = os.getenv('RWS_HOSTS')
RWS_URI = os.getenv('RWS_URI', "/api/v2/diagnostics/version")
RWS_CALL_URI = os.getenv('RWS_CALL_URI', "/api/v2/recordings")
RWS_SCREEN_URI = os.getenv('RWS_SCREEN_URI', "/internal-api/screen-recordings")
RWS_USER = os.getenv('RWS_USER')
RWS_PASS = os.getenv('RWS_PASS')

ES_HOSTS = os.getenv('ES_HOSTS')
ES_URI = os.getenv('ES_URI', "/_cluster/health")

WEBDAV_HOSTS = os.getenv('WEBDAV_HOSTS')
WEBDAV_URI = os.getenv('WEBDAV_URI', "/recordings/")
WEBDAV_USER = os.getenv('WEBDAV_USER')
WEBDAV_PASS = os.getenv('WEBDAV_PASS')

RPS_HOSTS = os.getenv('RPS_HOSTS')
RPS_URI = os.getenv('RPS_URI', "/api/status/")

# RCS_URI needs to be /rcs/version which returns a 200 not /rcs/version/ which returns a 401
RCS_HOSTS = os.getenv('RCS_HOSTS')
RCS_URI = os.getenv('RCS_URI', "/rcs/version")

VP_HOSTS = os.getenv('VP_HOSTS')
VP_URI = os.getenv('VP_URI', "/api/status?verbose=1")

# what times to total for new calls coming in
CALL_TOTALS = [15, 30, 60, 180, 240]
SCREEN_TOTALS = [15, 30, 60, 180, 240]

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
        print (appname + " " + hostname + ": UP", end='')
    else:
        print(appname + " " + hostname + ": DOWN  -   ", end='') 
        print("HTTP Status: " +str(httpStatus) + " error: " + str(httpData[:400]) )
        
def printESClusterHealth(data):
    try: 
      health = json.loads(data)
    except:
        return
    else:
      print ("    Cluster Status: " + health['status'])

## add timestamp to start of all logged lines
def printTime():
    print(time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()) + " UTC " + time.strftime('%H:%M:%S - ',time.gmtime()), end='')

## print calls int he last x minutes defined by lastmin    
def printCallTotals(host, uri, lastmin, user, passw):
    now = round(time.time() * 1000)
    before = now - (lastmin * 60000)
    query = uri + "?startTime=" + str(before)
          
    rwsStatus, rwsData = checkURL(host, query, user, passw)
    
    try:
        if rwsStatus == 200:
            data = json.loads(rwsData)
            print(str(len(data["recordings"])) + " recordings in the last " + str(lastmin) + " minutes")
    except Exception as e:
        print("Error parsing json from " + query)
   

    
while (1):

    print("\n---- Host status ----")
    
    # check each RWS host
    if (RWS_HOSTS != None):
        rwsHosts = RWS_HOSTS.split(",")
        for host in rwsHosts:
            printTime()
            rwsStatus,rwsData = checkURL(host, RWS_URI, "", "")
            printHostStatus("RWS", host, rwsStatus, rwsData)
            print()
            
    ## check each ES host
    if (ES_HOSTS != None):
        esHosts = ES_HOSTS.split(",")
        for host in esHosts:
            printTime()
            esStatus, esData = checkURL(host, ES_URI, "", "")
            printHostStatus("ES", host, esStatus, esData)
            printESClusterHealth(esData)
                                    
    
    ## check each WebDAV host
    if (WEBDAV_HOSTS != None):
        webdavHosts = WEBDAV_HOSTS.split(",")
        for host in webdavHosts:
            printTime()
            webdavStatus, webdavData = checkURL(host, WEBDAV_URI, WEBDAV_USER, WEBDAV_PASS)
            printHostStatus("WebDAV", host, webdavStatus, webdavData)
            print()
                    
    
    ## check each RPS host
    if (RPS_HOSTS != None):
        rpsHosts = RPS_HOSTS.split(",")
        for host in rpsHosts:
            printTime()
            rpsStatus,rpsData = checkURL(host, RPS_URI, "", "")
            printHostStatus("RPS", host, rpsStatus, rpsData)
            print()
            
        
    ## check each RCS host
    if (RCS_HOSTS != None):
        rcsHosts = RCS_HOSTS.split(",")
        for host in rcsHosts:
            printTime()
            rcsStatus, rcsData = checkURL(host, RCS_URI, "", "")
            printHostStatus("RCS", host, rcsStatus, rcsData)
            print()
            
    ## Check each VP host
    if (VP_HOSTS != None):
        vpHosts = VP_HOSTS.split(",")
        for host in vpHosts:
            printTime()
            vpStatus, vpData = checkURL(host, VP_URI, "", "")
            printHostStatus("VP", host, vpStatus, vpData)
            print()
    
    
    print()
    
    if (RWS_HOSTS != None):
        print("---- Call status ----")
        
        printTime()
        print("RWS " + RWS_HOSTS.split(",")[0])
        print("Calls")
        for x in CALL_TOTALS: printCallTotals(RWS_HOSTS.split(",")[0], RWS_CALL_URI, x, RWS_USER, RWS_PASS)
        print("Screens")
        for x in SCREEN_TOTALS: printCallTotals(RWS_HOSTS.split(",")[0], RWS_SCREEN_URI, x, RWS_USER, RWS_PASS)
        print ("totals limited to 100")
        
    time.sleep(UPDATE)
    #break
     
     
