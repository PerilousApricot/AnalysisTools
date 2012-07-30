#!/usr/bin/env python

import httplib
import urllib
import sys,os
import datetime

def makeRequest(url,params):

    encodedParams = urllib.urlencode(params)
    headers  =  {"Content-type": "application/x-www-form-urlencoded",
                 "Accept": "text/plain"}

    #conn  =  httplib.HTTPSConnection(url, cert_file = os.getenv('X509_USER_PROXY'), key_file = os.getenv('X509_USER_PROXY'))
    conn  =  httplib.HTTPConnection(url)
    

    conn.request("POST",  "/reqmgr/create/makeSchema", encodedParams, headers)
    response = conn.getresponse()
    data = response.read()
    if response.status != 303:
        print 'could not post request with following parameters:'
        for item in params.keys():
            print item + ": " + str(params[item])
        print 'Response from http call:'
        print 'Status:',response.status,'Reason:',response.reason
        print 'Explanation:'
        print data
        print "Exiting!"
        sys.exit(1)
    workflow=data.split("'")[1].split('/')[-1]
    print 'Injected workflow:',workflow,'into',url
    conn.close()
    return workflow
    
def approveRequest(url,workflow):
    params = {"requestName": workflow,
              "status": "assignment-approved"}

    encodedParams = urllib.urlencode(params)
    headers  =  {"Content-type": "application/x-www-form-urlencoded",
                 "Accept": "text/plain"}

    #conn  =  httplib.HTTPSConnection(url, cert_file = os.getenv('X509_USER_PROXY'), key_file = os.getenv('X509_USER_PROXY'))
    conn  =  httplib.HTTPConnection(url)


    conn.request("PUT",  "/reqmgr/reqMgr/request", encodedParams, headers)
    response = conn.getresponse()
    if response.status != 200:
        print 'could not approve request with following parameters:'
        for item in params.keys():
            print item + ": " + str(params[item])
        print 'Response from http call:'
        print 'Status:',response.status,'Reason:',response.reason
        print 'Explanation:'
        data = response.read()
        print data
        print "Exiting!"
        sys.exit(1)
    conn.close()
    print 'Approved workflow:',workflow
    return

def assignRequest(url,workflow,team,site,era,procversion,activity):
    params = {"action": "Assign",
              "Team"+team: "checked",
              "SiteWhitelist": site,
              "SiteBlacklist": [],
              "MergedLFNBase": "/store/user/meloam",
              "UnmergedLFNBase": "/store/user/meloam",
              "ForceUserOutput" : 1,
              "ForceUserStorage" : 1,
              "MinMergeSize": 2147483648,
              "MaxMergeSize": 4294967296,
              "SoftTimeout":  3600 * 24,
              "GracePeriod": 3600 * 24,
              "MaxMergeEvents": 50000,
              "AcquisitionEra": era,
              "ProcessingVersion": procversion,
              "maxRSS": 4294967296,
              "maxVSize": 4294967296,
              "dashboard": activity,
              "checkbox"+workflow: "checked"}

    encodedParams = urllib.urlencode(params, True)

    headers  =  {"Content-type": "application/x-www-form-urlencoded",
                 "Accept": "text/plain"}

    conn  =  httplib.HTTPConnection(url)
    conn.request("POST",  "/reqmgr/assign/handleAssignmentPage", encodedParams, headers)
    response = conn.getresponse()
    if response.status != 200:
        print 'could not assign request with following parameters:'
        for item in params.keys():
            print item + ": " + str(params[item])
        print 'Response from http call:'
        print 'Status:',response.status,'Reason:',response.reason
        print 'Explanation:'
        data = response.read()
        print data
        print "Exiting!"
        sys.exit(1)
    conn.close()
    print 'Assigned workflow:',workflow,'to site:',site,'with processing version',procversion
    return

# read configs.txt
config = {}
       
# ReqMgr url
url = "se2.accre.vanderbilt.edu:8685"
site = "T2_US_Vanderbilt"
# site = "T2_US_Vanderbilt"
# site = "T1_FR_CCIN2P3"
# site = "T3_US_Colorado"
team = "testingteam"
# team = "testbed-processing"
era = "MeloAcquistionEra2"
activity = "integration"
procversion = "IntegrationTest_" + datetime.datetime.now().strftime("%y%m%d")

# change RequestString before every usage
params =   {"CMSSWVersion": 'CMSSW_5_2_2',
            "GlobalTag": 'START52_V5::All',
            "MergedLFNBase" : "/store/user/meloam",
            "UnmergedLFNBase" : "/store/user/meloam",
              "ForceUserOutput" : 1,
              "ForceUserStorage" : 1,
            "SiteWhitelist" : "T2_US_Vanderbilt",
            "RequestString": 'T2stop_600_250_0_75v8',
            "RequestPriority": 300000,
            "TimePerEvent": 1000,
            "FilterEfficiency": 1,
            "ScramArch": 'slc5_amd64_gcc462',
            "RequestType" : "LHEStepZero",
            "RequestNumEvents": 100000,
            "inputMode": "couchDB",
            "CouchURL":"http://se2.accre.vanderbilt.edu:5985",
            "CouchDBName":"wmagent_configcache",
            # the full config
            #"ProcConfigCacheID": '1c73b6c3cbc6254dea3c3473be6cde49',
            # the fnal config bddd8738547bf9bab08d30c57b17ae59
            # the gpfs config c6e4c48118fee0605b67cb8abf557346
            "ProcConfigCacheID": '37916fe37672f725a17bf70a25e21a8a',
            "EventsPerLumi": 1,
            "PrimaryDataset": 'T2stop_600_250_0_75',
            "DataPileup": "",
            "filterEfficiency": 1,
            "MCPileup": "",
            "FirstEvent": 1,
            "DataTier": 'USER',
            "Memory": 2000000000,
            "SizePerEvent":1024*1024,
            "maxRSS": 4294967296,
            "maxVSize": 4294967296,
            "SoftTimeout": 3600 * 24,
            "FirstLumi": 1,
            "AcquisitionEra":era,
            "PrepID": 'MCTEST-GEN-0001',
            "ForceUserOutput" : 1,
            "Requestor": 'meloam',
            "RequestorDN": '/DC=org/DC=doegrids/OU=People/CN=Andrew Malone Melo 788499',
            'DbsUrl': 'https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet',
            "Group": 'testing',
            "TotalTime": 14400, #job length in sec.
            "userSandbox": "root://xrootd.unl.edu//store/user/meloam/sandboxes/gensandbox2.tgz",
            }        
                  
# make request

workflow = makeRequest(url,params)
approveRequest(url,workflow)
assignRequest(url,workflow,team,site,era,procversion,activity)
