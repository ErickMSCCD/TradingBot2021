import time
import hmac
import hashlib
import requests
import json
'''
For placing an order we need:
HTTP Request
POST https://api.bitso.com/v3/orders/
'''
my_key = '61c25b040d49dcecb188c61ea35aaf51'  # Secret Key
bts_key = 'OIyfMHuXxZ'
class PrivateApi:
    def __init__(self, my_key, bts_key, http_meth, req_path, param=None):
        self.my_key = my_key
        self.bts_key = bts_key
        self.http_meth = http_meth
        self.req_path = req_path
        self.param = param
    def createSignature(self):
        # Create signature
        nonce =  str(int(round(time.time() * 1000)))        
        message = nonce+self.http_meth+self.req_path
        if (self.http_meth == "POST"):
            message += json.dumps(self.param)
           

        signature = hmac.new(self.my_key.encode('utf-8'),
                                            message.encode('utf-8'),
                                            hashlib.sha256).hexdigest()
        # Build the auth header
        auth_header = 'Bitso %s:%s:%s' % (self.bts_key, nonce, signature)
        
        # Send request
        if (self.http_meth == "GET"):
            return requests.get("https://api.bitso.com" + self.req_path, headers={"Authorization": auth_header})
        elif (self.http_meth == "POST"):
            return requests.post("https://api.bitso.com" + self.req_path, json = self.param, headers={"Authorization": auth_header})

