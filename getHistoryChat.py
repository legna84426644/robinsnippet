'''
Created on Mar 4, 2017

@author: Robin
'''
import requests

token = ""
domain = ""
userid = ""

url = domain + "/v2/user/" + userid + "/history/latest"
h = {"Content-type":"application/json", "Authorization":"Bearer " + token}
query = "?max-results=1"
#d = {"max-results": 1}
res = requests.get(url+query, headers= h)
print res.text