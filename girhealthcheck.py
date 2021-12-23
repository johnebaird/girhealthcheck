import re
import json
import requests
import time

# comma seperate values of RWS hosts to check
RWS_HOSTS = "http://192.168.45.81:8080"
RWS_URI = "/api/v2/diagnostics/version"

# comma seperated values of ES hosts to check
ES_HOSTS = "http://192.168.45.81:9200,http://192.168.45.83:9200"
ES_URI = "/_cluster/health"

#update interval in seconds between checks
UPDATE = 10


# Take a host and a URI and return appropriate HTTP status code and successful data from query or error response
def checkURL(host, uri):
    
    try:
        query = host + uri
        data = ""
        data = requests.get(query)
        
                        
    except:
        return 0, "timeout"
        
    else: 
        return data.status_code, data.text


# check invidual RWS and print status
def checkRWS(host, uri):
    
    rwsStatus,rwsData = checkURL(host, RWS_URI)
        
    if rwsStatus == 200:
        print ("    RWS " + host + ": UP")
    else:
        print ("    RWS " + host + ": DOWN  -   ", end='') 
        print ("HTTP Status: " +str(rwsStatus) + " data: " + str(rwsData) )
            

# check invididual ES and print status
def checkES(host, uri):

    esStatus, esData = checkURL(host, ES_URI)
    
    if esStatus == 200:
        print ("    ES " + host + ": UP")
    else:
        print ("    ES " + host + ": DOWN  -   ", end='') 
        print ("HTTP Status: " +str(esStatus) + " data: " + str(esData) )
        
        
            
while (1):

    print("Host status:")
    
    # check each RWS host
    rwshosts = RWS_HOSTS.split(",")
    
    for host in rwshosts:
        checkRWS(host, RWS_URI)
        
    
    ## check each ES host
    eshosts = ES_HOSTS.split(",")
    
    for host in eshosts:
       checkES(host, ES_URI)
                
      
      
    #time.sleep(UPDATE)
    break
     
     
