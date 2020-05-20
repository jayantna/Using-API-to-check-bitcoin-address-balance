import sys
sys.path.append("base58-2.0.0")
import base58
import sqlite3
import re
import binascii
import hashlib
import ssl
import urllib.request, urllib.parse, urllib.error
import json


fh=open("Bitcoin.csv", encoding="utf8").read()
x=re.findall('[13][a-km-zA-HJ-NP-Z1-9]{25,34}',fh)
validAdd=[]
for bitcoinAddress in x:
    #print("Bitcoin Address: ", bitcoinAddress)
    base58Decoder = base58.b58decode(bitcoinAddress).hex()
    prefixAndHash = base58Decoder[:len(base58Decoder)-8]
    checksum = base58Decoder[len(base58Decoder)-8:]
    hash = prefixAndHash
    for x in range(1,3):
        hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()        
    if(checksum == hash[:8]):
        #print("[TRUE] checksum is valid!")
        validAdd.append(bitcoinAddress)
    else:
        continue


for adds in validAdd:
    url='https://chain.api.btc.com/v3/address/'+adds
    data=urllib.request.urlopen(url).read().decode()
    js=json.loads(data)
    try:
        print(js['data']['address'], '{:.8f}'.format(js['data']['balance']/10**8,8))
    except:
        continue

    #print(json.dumps(js,indent=6))





        



    
    
    
