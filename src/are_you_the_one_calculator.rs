use log::{debug, info};
use itertools::{Itertools};
use crate::filehandler::SeasonData;



// fn add_repetition()

pub fn calculate_possibilities(data: SeasonData){
    let m: &Vec<String>; // Vector of the greater number of people
    let n: &Vec<String>; // Vector of the smaller number of people
    let add_m: &Vec<String>; 
    let add_n: &Vec<String>;
    debug!("Men: {:?}", &data.men);
    debug!("Women: {:?}", &data.women);

    if data.men.len() >= data.women.len() {
        m = &data.men;
        n = &data.women;
        add_m = &data.additional_men;
        add_n = &data.additional_women;
    } else {
        m = &data.women;
        n = &data.men;
        add_m = &data.additional_women;
        add_n = &data.additional_men;
    }
    let mut to_permut = Vec::<usize>::new();
    for i in 0..n.len() {
        to_permut.push(i);
    }
    
    if m.len() == n.len() {
        debug!("to_permut: {:?}", to_permut);
        create_permutations(&to_permut);
    } else {
        info!("Adding {:?} persons of vector n a second time", m.len()-n.len());
        let mut j;
        for i in 0..n.len() {
            let mut extendet_to_permuts = Vec::<usize>::new();
            for i in 0..to_permut.len() {
                extendet_to_permuts.push(to_permut[i]);
            }
            j = i;
            debug!("j: {:?}", j);
            while extendet_to_permuts.len() < m.len() {
                extendet_to_permuts.push(j);
                j = j + 1;
                if j >= m.len() {j = 0}
            }
            if j > n.len() {break;}
            debug!("to_permut: {:?}", extendet_to_permuts);
            create_permutations(&extendet_to_permuts);
        }
        
    }
    
}

fn create_permutations(to_permut:&Vec<usize>) {
    let len: usize = to_permut.len();
    let permuts = to_permut.into_iter().permutations(len);
    for perm in permuts {
        println!("{:?}", perm);
    }
}

// fn calculate_affection()