const crypto = require('crypto');
var reverse = require("buffer-reverse")
const got = require('got');

const BASE_URL = "https://api.blockcypher.com/v1/btc/main/blocks/"
const MAX_TXN = 500

// ------- CHANGE THIS VALUE TO THE BLOCK YOU WANT TO TEST ------- 
const SELECTED_BLOCK_HASH = "000000000000000018a9a6c39806292529a401918ec55e078306b35884814b7c"
// ------------------------------------------------------------- 

get_merkle_root = tx_list => {
    
    if (tx_list.length === 1) return tx_list[0]

    let branch = []

    for (let i = 0; i < tx_list.length-1; i=i+2) {
        branch.push(double_hash(tx_list[i], tx_list[i+1]))
    }

    if(tx_list.length % 2 === 1){
        branch.push(double_hash(tx_list[tx_list.length-1], tx_list[tx_list.length-1]))
    }

    return get_merkle_root(branch)
}

double_hash = (a,b) => {
    let a1 = Buffer.from(a, 'hex')
    let b1 = Buffer.from(b, 'hex')
    // convert to little endian notataion
    let res = Buffer.concat([reverse(a1), reverse(b1)])
    // double hashing as per bitcoin protocol
    const hash1 = crypto.createHash('sha256').update(res).digest();
    const hash2 = crypto.createHash('sha256').update(hash1).digest();
    return reverse(Buffer.from(hash2,'utf-8')).toString('hex')
}

get_tx_list = async (block_hash, tx_start = 0, tx_stop = 500) => {
    let transactions = [];
    while(true) {
        let url = BASE_URL + block_hash + "?txstart=" + String(tx_start) + "&limit=" + String(tx_stop);
        const response = await got(url);
        let current_txns = JSON.parse(response.body).txids;
        if(current_txns.length > 0){
            transactions = transactions.concat(current_txns);
            tx_start += MAX_TXN;
            tx_stop += MAX_TXN;
        }
        else {
            break;
        }
    }
    return transactions;
}

main = async() => {
    let tx_list = await get_tx_list(SELECTED_BLOCK_HASH);
    let merkle_root = get_merkle_root(tx_list);
    console.log(tx_list);
    console.log(merkle_root);
}

main();