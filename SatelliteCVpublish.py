#!/bin/python

import sys
import json
import requests
import time
import urllib3
import ConfigParser
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONFIG = ConfigParser.ConfigParser()
CONFIG.read("/tmp/encrypted.conf")
HEADERS = {"Content-Type":"application/json","Accept":"application/json"}
BASEURL = "https://Satserver.example.com"
USERNAME = "SatAdmin"
PASSWORD = CONFIG.get("configuration","password")
SSL_VERIFY = False   # Ignore SSL for now


def Publish_CV():
 COUNTER=0
 contentviews = ['RHEL7_Server', 'RHEL7_Software_Collections', 'RHEL8_Server']
 LEN = len(contentviews)
 while COUNTER < LEN:
  APIURL = "/katello/api/content_views/"
  URL = BASEURL + APIURL
  response = requests.get(URL, auth=(USERNAME, PASSWORD))
  data = response.json()
  for entry in data['results']:
   if (entry['name']) == (contentviews[COUNTER]) and (entry['latest_version']) != (entry['next_version']):
#    print contentviews[COUNTER]
    print "\nName: %s   Contentview ID: %s   LatestVersion: %s  NextVersion: %s" % (entry['name'], entry['id'], entry['latest_version'], entry['next_version'])
    ID = entry['id']
    URL = BASEURL + APIURL + str(ID) + '/publish'
    response = requests.post(URL, auth=(USERNAME, PASSWORD), headers=HEADERS)
    print ("Respective URL for each Content view ID")
    print response.url
  COUNTER = COUNTER + 1
  time.sleep(900)

Publish_CV()

def Publish_Composite_CV():
    COUNTER=0
    contentviews = ['CompositeCV1', 'CompositeCV2', 'CompositeCV3', 'CompositeCV4', 'CompositeCV5']
    LEN = len(contentviews)
    while COUNTER < LEN:
     APIURL = "/katello/api/content_views/"
     URL = BASEURL + APIURL
     response = requests.get(URL, auth=(USERNAME, PASSWORD))
     data = response.json()
     for entry in data['results']:
      if (entry['name']) == (contentviews[COUNTER]):
       print "\nName: %s   CompositeContentview ID: %s LatestVersion: %s  NextVersion: %s" % (entry['name'], entry['id'], entry['latest_version'], entry['next_version'])
       ID = entry['id']
       URL = BASEURL + APIURL + str(ID) + '/publish'
       response = requests.post(URL, auth=(USERNAME, PASSWORD), headers=HEADERS)
       print ("Respective URL for each Composite Content view ID")
       print response.url
     COUNTER = COUNTER + 1
     time.sleep(330)

Publish_Composite_CV()

###### Promoting of LifeCycle Environment ######

print ("\n*****Promote of LifeCycle Environments starts..*****\n")

def Promote_NONPRODLifecycle():
    APIURL = "/katello/api/content_views"
    URL = BASEURL + APIURL
    params={"name":"NonProd"}
    response = requests.get(URL, auth=(USERNAME, PASSWORD),params=params)
    data = response.json()
#    time.sleep(360)
    for entry in data["results"]:
        LATEST=(entry['latest_version'])
        print ("\nLatest CV Value Published" + " " + LATEST)
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as ID to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "NONPROD_ENV1":
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\nPrint URL and status while promoting NONPROD Lifecycle Environment")
    print input.url
    print input.status_code
    time.sleep(180)
    for entry in data["results"]:
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as id to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "NONPROD_ENV2":
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\nPrint URL and status while promoting NONPROD ENV2 Lifecycle Environment")
    print input.url
    print input.status_code
    time.sleep(160)

Promote_NONPRODLifecycle()

def Promote_ProdLifecycle():
    APIURL = "/katello/api/content_views"
    URL = BASEURL + APIURL
    params={"name":"Prod"}
    response = requests.get(URL, auth=(USERNAME, PASSWORD),params=params)
    data = response.json()
#    time.sleep(160)
    for entry in data["results"]:
        LATEST=(entry['latest_version'])
        print ( "\n Latest CV Value Published" + " " + LATEST)
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as id to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "Prod":
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\nPrint URL and status while promoting Prod Lifecycle Environment")
    print input.url
    print input.status_code
    time.sleep(160)

Promote_ProdLifecycle()

def Promote_QALifecycle():
    APIURL = "/katello/api/content_views"
    URL = BASEURL + APIURL
    params={"name":"QA"}
    response = requests.get(URL, auth=(USERNAME, PASSWORD),params=params)
    data = response.json()
#    time.sleep(160)
    for entry in data["results"]:
        LATEST=(entry['latest_version'])
        print ( "\n Latest CV Value Published" + " " + LATEST)
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as id to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "QA":
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\nPrint URL and status while promoting QA Lifecycle Environment")
    print input.url
    print input.status_code
    time.sleep(160)

Promote_QALifecycle()

def Promote_DevLifecycle():
    APIURL = "/katello/api/content_views"
    URL = BASEURL + APIURL
    params={"name":"Dev"}
    response = requests.get(URL, auth=(USERNAME, PASSWORD),params=params)
    data = response.json()
#    time.sleep(160)
    for entry in data["results"]:
        LATEST=(entry['latest_version'])
        print ( "\nLatest CV Value Published" + " " + LATEST)
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as id to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "DEV1":
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\n Print URL and status while promoting DEV1 Lifecycle Environment")
    print input.url
    print input.status_code
    time.sleep(180)
    for entry in data["results"]:
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as id to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "DEV2":
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\n Print URL and status while promoting DEV2 Lifecycle Environment")
    print input.url
    print input.status_code
    time.sleep(180)
    for entry in data["results"]:
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as id to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "DEV3":
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\nPrint URL and status while promoting DEV3 Lifecycle Environment")
    print input.url
    print input.status_code
    time.sleep(160)

Promote_DevLifecycle()

def Promote_TestLifecycle():
    APIURL = "/katello/api/content_views"
    URL = BASEURL + APIURL
    params={"name":"Test"}
    response = requests.get(URL, auth=(USERNAME, PASSWORD),params=params)
    data = response.json()
#    time.sleep(160)
    for entry in data["results"]:
        LATEST=(entry['latest_version'])
        print ( "\n Latest CV Value Published" + " " + LATEST)
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as id to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "Test1":
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\n Print URL and status while promoting Test1 Lifecycle Environment")
    print input.url
    print input.status_code
    time.sleep(180)

    for entry in data["results"]:
        for entry2 in (entry["versions"]):
            if (entry2["version"]) == LATEST:
               print "\nPrint version used as id to be promoted: %s" % (entry2["id"])
               ID=entry2["id"]
        for entry3 in (entry["environments"]):
            if (entry3["label"]) == "Test2"
               print "\nPrint id of each lifecycle environment: %s" % (entry3["id"])
               ENVID=(entry3["id"])
    URL = BASEURL + '/katello/api/content_view_versions/' + str(ID) +  '/promote'
    PAYLOAD = {
    "id": ID,
    "environment_id": ENVID
   }
    input = requests.post(URL, auth=(USERNAME, PASSWORD), data=json.dumps(PAYLOAD), headers=HEADERS)
    print ("\n Print URL and status while promoting Test2 Lifecycle Environment")
    print input.url
    print input.status_code

Promote_TestLifecycle()
