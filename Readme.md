We are using data provided by someone who has scraped the top 2.5 million Reddit posts and then placed them on GitHub. Now we can figure out (with data!) just how much Redditors love BITCOIN. Or how about a data backed equivalent of r/bitcoin?

Steps:

We are using data of bitcoin.csv provided in the github link
Using the data we are going to extract all the possible bitcoin addresses posted by Redditors, extracting using regex '[13][a-km-zA-HJ-NP-Z1-9]{25,34}'
Now we have all the btc addresses from the data including the invalid one
To exclude invalid btc address we are going to perform SHA256 checksum in all addresses
Now we have only valid bitcoin addresses from which we can extract account details like transactions, hashes, block details, balance etc.
Here we are only extracting Account's Bitcoin holding balance
import sys
sys.path.append("base58-2.0.0") #base58 module library

import re
import binascii, base58, hashlib
import ssl
import urllib.request, urllib.parse, urllib.error
import json


fh=open("Bitcoin.csv", encoding="utf8").read()
x=re.findall('[13][a-km-zA-HJ-NP-Z1-9]{25,34}',fh)
validAdd=[]

#performing SHA256 checksum
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

#obtaining bitcoin account details using btc.com api
for adds in validAdd:
    url='https://chain.api.btc.com/v3/address/'+adds
    data=urllib.request.urlopen(url).read().decode()
    js=json.loads(data)
    #print(json.dumps(js,indent=6))
    try:
        print(js['data']['address'], '{:.8f}'.format(js['data']['balance']/10**8,8))
    except:
        continue
