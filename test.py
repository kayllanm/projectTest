# -*- coding: utf-8 -*-

import requests, json
import xml.etree.ElementTree as ET
import base64

url = "https://clients.voice.vodacom.com/cgc/PAServlet"

# get cookies
getResponse = requests.get("https://clients.voice.vodacom.com/cgc")
print(getResponse.headers)
cookie = getResponse.headers["Set-Cookie"].split(";")[0]

payload = "leaderBWUserId=27873100047%40vodacom.com&impFirstName=kayllan&impLastName=test&impMucHash=a3tca4&impMucSeed=cftvau"
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cookie': str(cookie),
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers).json()

print "////////////////////////// First response  ///////////////////////////////"
print(response)
print "////////////////////////// First response  ///////////////////////////////"

# ////////////////// Second Request ////////////////////////

bosh_url = response["boshUrl"]

second_payload = "<body rid='3100289102' xmlns='http://jabber.org/protocol/httpbind' to='kowabunga-guest.voice.vodacom.com' xml:lang='en' wait='60' hold='1' content='text/xml; charset=utf-8' ver='1.6' xmpp:version='1.0' xmlns:xmpp='urn:xmpp:xbosh'/>"

second_headers = {
    'content-type': "text/plain;charset=UTF-8"
    }
second_response = requests.request("POST", bosh_url, data=second_payload, headers=second_headers)

print "//////////////////////////  second_response  ///////////////////////////////"
print(second_response.text)
tree = ET.ElementTree(ET.fromstring(second_response.text))
root = tree.getroot()
print "//////////////////////////"
print(root.attrib["sid"])
print "//////////////////////////  second_response  ///////////////////////////////"

# ////////////////// 3rd Request ////////////////////////

third_payload = "<body rid='3100289103' xmlns='http://jabber.org/protocol/httpbind' sid='{0}'/>".format(root.attrib["sid"])

third_response = requests.request("POST", bosh_url, data=third_payload, headers=second_headers)

print "//////////////////////////  third_response  ///////////////////////////////"
print(third_response.text)
print "//////////////////////////  third_response  ///////////////////////////////"

# ////////////////// 4th Request actual login process ////////////////////////
auth = '{0}{1}{2}'.format(response["loginId"],  response["loginId"].split('@')[0],  response["password"])
encoded = base64.b64encode(auth)
print(encoded)

forth_payload = "<body rid='3100289105' xmlns='http://jabber.org/protocol/httpbind' sid='{0}'><auth xmlns='urn:ietf:params:xml:ns:xmpp-sasl' mechanism='PLAIN'>NTVlMmQ1YzItMTFiYy00YTA1LTkwNGYtYWM0YmVkYzViMGNkQGtvd2FidW5nYS1ndWVzdC52b2ljZS52b2RhY29tLmNvbQA1NWUyZDVjMi0xMWJjLTRhMDUtOTA0Zi1hYzRiZWRjNWIwY2QAMDQxMWY3OGMtNjJmMS00NTE5LWIxMGItYzI0MTc5MDRlZWI5</auth></body>".format(root.attrib["sid"], encoded)

forth_response = requests.request("POST", bosh_url, data=forth_payload, headers=second_headers)

print "//////////////////////////  forth_response  ///////////////////////////////"
print(forth_response.text)
print "//////////////////////////  forth_response  ///////////////////////////////"
