import json
import requests
import codecs
from hashlib import sha256 

decode_hex = codecs.getdecoder("hex_codec")
BASE_URL = "https://api.blockcypher.com/v1/btc/main/blocks/"
MAX_TXN = 500

## ------- CHANGE THIS VALUE TO THE BLOCK YOU WANT TO TEST ------- ##
SELECTED_BLOCK_HASH = "000000000000000018a9a6c39806292529a401918ec55e078306b35884814b7c"
## ------------------------------------------------------------- ##

# use https://api.blockcypher.com/v1/btc/main/blocks/<block_hash>?txstart=0&limit=0 for fetching txs of block
def get_txn_list(block_hash, tx_start = 0, tx_stop = 500):
    # loop through api calls to find the entire list of transactions,
    # this looping is necessary since the api has a max number of transactions that it returns
    transactions = []
    while True:
        url = BASE_URL + block_hash + "?txstart=" + str(tx_start) + "&limit=" + str(tx_stop)
        data = requests.get(url)
        tx = data.json()['txids']
        if not tx:
            break
        else:
            transactions.extend(tx)
            tx_start, tx_stop = tx_start + MAX_TXN, tx_stop + MAX_TXN
    return transactions

 
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
    txn_list = get_txn_list(SELECTED_BLOCK_HASH)
    print(txn_list)
    print(len(txn_list))
    print(get_merkle_root(txn_list))
    
   
if __name__ == "__main__":
    compute_merkle_root()
    