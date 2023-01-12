use log::{debug, info};
use itertools::{Itertools};
use crate::filehandler::SeasonData;



// fn add_repetition()

pub fn calculate_possibilities(data: &SeasonData){
    let mut m= Vec::<usize>::new(); // Vector of the greater number of people
    let mut n= Vec::<usize>::new(); // Vector of the smaller number of people
    let mut add_m = Vec::<usize>::new();
    let mut add_n = Vec::<usize>::new();

    debug!("Men: {:?}", data.men);
    debug!("Women: {:?}", data.women);

    if data.men.len() >= data.women.len() {
        for i in 0..data.men.len() {
            m.push(i);
        }
        for i in 0..data.women.len() {
            n.push(i);
        }
        for i in 0..data.additional_men.len() {
            add_m.push(i+m.len());
        }
        for i in 0..data.additional_women.len() {
            add_n.push(i+n.len());
        }
    } else {
        for i in 0..data.women.len() {
            m.push(i);
        }
        for i in 0..data.men.len() {
            n.push(i);
        }
        for i in 0..data.additional_women.len() {
            add_m.push(i+n.len());
        }
        for i in 0..data.additional_men.len() {
            add_n.push(i+m.len());
        }
    }
    let mut to_permut = Vec::<usize>::new();
    for i in 0..n.len() {
        to_permut.push(i);
    }
    
    if m.len() == n.len() {
        debug!("to_permut: {:?}", to_permut);
        create_permutations(&to_permut, &m, &add_m, &add_n);
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
            create_permutations(&extendet_to_permuts, &m, &add_m, &add_n);
        }   
    }
}

fn create_permutations(to_permut:&Vec<usize>, m:&Vec<usize>, add_m:&Vec<usize>, add_n:&Vec<usize>) {
    let len: usize = to_permut.len();
    let permuts = to_permut.into_iter().permutations(len);
    for perm in permuts {
        if (add_m.len() > 0) || (add_n.len() > 0){
            println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
            add_repetition(to_permut, m, add_m, add_n);
        } else {
            println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
        }
    }
}

fn add_repetition(to_permut:&Vec<usize>, m:&Vec<usize>, add_m:&Vec<usize>, add_n:&Vec<usize>) {
    let mut complete_m = Vec::<usize>::new();
    let mut complete_n = Vec::<usize>::new();
    for i in 0..m.len() {
        complete_m.push(m[i])
    }
    for i in 0..to_permut.len() {
        complete_n.push(to_permut[i])
    }
    if add_m.len() > 0 {
        info!("Adding {} repetitions of m", add_m.len());
    }
    if add_n.len() > 0 {
        info!("Adding {} repetitions of n", add_n.len());
    }
}

// fn calculate_affection()