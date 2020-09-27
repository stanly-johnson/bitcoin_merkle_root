import json
import codecs
from hashlib import sha256 

decode_hex = codecs.getdecoder("hex_codec")

# use https://api.blockcypher.com/v1/btc/main/blocks/<block_hash>?txstart=0&limit=0 for fetching txs of block
# read txns from file
def get_txn_list(filename = "tx_list.json"):
    with open(filename) as f:
        data = json.load(f)
    return data['txs']

 
# calculate merkle root as per bitcoin protocol
def get_merkle_root(txn_list):
    
    if len(txn_list) == 1:
        return txn_list[0]
        
    branch = []
    
    for i in range(0, len(txn_list)-1, 2):
        branch.append(double_hash(txn_list[i], txn_list[i+1])) 
        
    # in case of odd number of transactions, duplicate last txn and hash 
    if len(txn_list) % 2 == 1:
        branch.append(double_hash(txn_list[-1],txn_list[-1]))
        
    return get_merkle_root(branch)


def double_hash(a, b):
    # convert to little endian notation used by bitcoin
    a1 = decode_hex(a)[0][::-1]
    b1 = decode_hex(b)[0][::-1]
    # bitcoin uses double hashing, prevents length extension attacks
    h = sha256(sha256(a1+b1).digest()).digest()
    return h[::-1].hex()

    
def compute_merkle_root():
    #https://www.blockchain.com/btc/block/000000000000000018a9a6c39806292529a401918ec55e078306b35884814b7c
    txn_list = get_txn_list("319957.json")
    print(get_merkle_root(txn_list))
    
   
if __name__ == "__main__":
    compute_merkle_root()
    