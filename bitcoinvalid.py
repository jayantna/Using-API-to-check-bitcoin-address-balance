import sys
import hashlib
import binascii
sys.path.append("base58-2.0.0")

import base58
bitcoinAddress='313671323933723173377371387373343'
print("Bitcoin Address: ", bitcoinAddress)

base58Decoder = base58.b58decode(bitcoinAddress).hex()
print("Base58 Decoder: ", base58Decoder)

prefixAndHash = base58Decoder[:len(base58Decoder)-8]
checksum = base58Decoder[len(base58Decoder)-8:]
print("\t|___> Prefix & Hash: ", prefixAndHash)
print("\t|___> Checksum: ", checksum)
print("--------------------------------------")

hash = prefixAndHash
for x in range(1,3):
    hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
    print("Hash#", x, " : ", hash)
print("--------------------------------------")

if(checksum == hash[:8]):
    print("[TRUE] checksum is valid!")
else:
    print("[FALSE] checksum is not valid!")
