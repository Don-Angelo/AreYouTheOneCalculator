use itertools::Itertools;
// use std::ops::Range;
use std::fs::File;
use std::io::Read;
use std::io;

fn main(){
    println!("are you the one calculator main");
    let mut text = read_file("./data/vipSeason2-2022.json");
    println!("file: {:?}", text);


    let mut m = Vec::new();
    let mut n = Vec::new();
    m.push("Men0".to_string());
    m.push("Men1".to_string());
    m.push("Men2".to_string());
    m.push("Men3".to_string());
    // m.push("Men4".to_string());
    
    n.push("Women0".to_string());
    n.push("Women1".to_string());
    n.push("Women2".to_string());
    // n.push("Women3".to_string());

    if m.len() >= n.len() {
        process(&n.len(), &m.len());
    } else {
        process(&m.len(), &n.len());
    }
}

fn read_file(filename: &str) -> io::Result<String> {
    let mut file = File::open(filename)?;
    let mut text = String::new();
    file.read_to_string(&mut text)?;
    Ok(text)
}

fn process(smaller_len:&usize, desired_len:&usize) {
    println!("{:?} {:?}", smaller_len, desired_len);
    let mut to_permut = Vec::<usize>::new();
    for i in 0..*smaller_len {
        to_permut.push(i);
    }
    create_permutations(&to_permut, &smaller_len, &desired_len);
}

fn create_permutations(to_permut:&Vec<usize>, smaller_len:&usize, desired_len:&usize) {
    println!("create_permutations {:?}",to_permut);
    let len = to_permut.len();
    let permuts = to_permut.into_iter().permutations(len);
    for perm in permuts {
        if perm.len() < *desired_len {
            add_repetition(&perm, smaller_len, desired_len);
        } else {
            println!("{:?}", perm);
        }
    }
}

fn add_repetition(perm:&Vec<&usize>, smaller_len:&usize, desired_len:&usize) {
    println!("add_repetition {:?} {:?} {:?}", perm, smaller_len, desired_len);
    for i in 0..*smaller_len {
        let mut extended_perm = perm.clone();
        extended_perm.push(&i);
        if extended_perm.len() < *desired_len {
            add_repetition(&extended_perm, &smaller_len, &desired_len);
        } else {
            println!("{:?}", extended_perm);
        }
    }
}