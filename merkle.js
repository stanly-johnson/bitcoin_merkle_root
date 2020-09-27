const crypto = require('crypto');
var reverse = require("buffer-reverse")
const tx_list = require('./319957.json')

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

console.log(get_merkle_root(tx_list['txs']))