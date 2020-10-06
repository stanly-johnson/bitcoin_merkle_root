extern crate crypto;
use self::crypto::digest::Digest;
use self::crypto::sha2::Sha256;
use std::str;

fn gen_merkle_root(arr: Vec<String>) -> String {
    
    if arr.len() == 1 {
        return arr[arr.len() - 1].to_string();
    }

    let mut branch : Vec<String> = Vec::new();

    for i in (0..arr.len()-1).step_by(2){
        let result = sha256_digest(&arr[i], &arr[i+1]);
        branch.push(result);
    }

    if arr.len()%2 == 1 {
        let result = sha256_digest(&arr[arr.len() - 1], &arr[arr.len() - 1]);
        branch.push(result);
    }

    return gen_merkle_root(branch);

}

fn sha256_digest(x1 : &str, x2 : &str) -> String {
    let mut hasher = Sha256::new();

    let s1 = x1.as_bytes();
    let m1: Vec<u8> = s1.iter().copied().rev().collect();

    let s2 = x2.as_bytes();
    let m2: Vec<u8> = s2.iter().copied().rev().collect();

    hasher.input(&concat_u8(&m1, &m2));
    
    let hex = hasher.result_str();

    hasher.reset();
    hasher.input_str(&hex);

    let hex2 = hasher.result_str();
    let h = hex2.as_bytes();
    let h1: Vec<u8> = h.iter().copied().rev().collect();

    //println!("{:?}", h1);

    return str::from_utf8(&h1).unwrap().to_string();
 
}

fn concat_u8(first: &[u8], second: &[u8]) -> Vec<u8> {
    [first, second].concat()
}


fn main(){

    let mut wtf : Vec<String> = Vec::new();

    for x in 0..TXNS.len(){
        wtf.push(TXNS[x].to_string());
    }

    println!("{:?}", wtf);

    let y = gen_merkle_root(wtf);
    println!("Merkle Root : {}", y);
     
}
