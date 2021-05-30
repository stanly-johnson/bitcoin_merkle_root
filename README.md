### Bitcoin Merkle Root

Sample code in different languages to compute merkle root as per bitcoin implementation.

The bitcoin merkle tree differs from a standard merkle tree implementation in two ways
1. Bitcoin uses little endian notation
2. Double hashing against length extension attacks


| language   | status      |
|------------|-------------|
| Python     | Complete    |
| JS         | Complete    |
| Rust       | Pending     |
| Golang     | Pending     |



#### How to run

##### Python Example
1. Ensure you have python3 installed
2. Open `merkle.py` and change `SELECTED_BLOCK_HASH` to the block hash you want to test
3. Run `python3 merkle.py` and compare merkle root with block explorer

##### JS Example
1. Run `npm i`
2. Open `merkle.js` and change `SELECTED_BLOCK_HASH` to the block hash you want to test
3. Run `node merkle.js` and compare merkle root with block explorer
