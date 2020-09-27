### Bitcoin Merkle Root

Sample code in different languages to compute merkle root as per bitcoin implementation.

The bitcoin merkle tree differs from a standard merkle tree implementation in two ways
1. Bitcoin uses little endian notation
2. Double hashing against length extension attacks

#### How to run
- Download block transactions from any bitcoin api ([ex](https://api.blockcypher.com/v1/btc/main/blocks/000000000000000018a9a6c39806292529a401918ec55e078306b35884814b7c?txstart=0&limit=400))
- Create a new json file with the list of transactions (Eg : 319957.json)
- Provide the new filename as input to `get_txn_list` function
- Verify result with `Merkle Root` in block header ([ex](https://www.blockchain.com/btc/block/000000000000000018a9a6c39806292529a401918ec55e078306b35884814b7c))

