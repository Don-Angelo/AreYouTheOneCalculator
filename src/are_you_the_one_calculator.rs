use log::{debug, info};
use itertools::{Itertools};
use crate::filehandler::SeasonData;



// fn add_repetition()

fn get_mn(data: &SeasonData) -> (Vec::<usize>, Vec::<usize>, Vec::<usize>, Vec::<usize>){
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
    return (m,n,add_m,add_n);
}

fn get_mn_names(data: &SeasonData) {

}

fn get_matching_night_mn(data: &SeasonData) {
    for k in data.matching_nights.keys() {
        
    }
}


pub fn calculate_possibilities(data: &SeasonData){
    let (m, n, add_m, add_n):(Vec<usize>, Vec<usize>, Vec<usize>, Vec<usize>) = get_mn(data);

    debug!("Men: {:?}", data.men);
    debug!("Women: {:?}", data.women);

    
    let mut to_permut:Vec<usize> = Vec::<usize>::new();
    for i in 0..n.len() {
        to_permut.push(i);
    }
    
    if m.len() == n.len() {
        debug!("to_permut: {:?}", to_permut);
        create_permutations(&to_permut, &m, &add_m, &add_n, data);
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
            create_permutations(&extendet_to_permuts, &m, &add_m, &add_n, data);
        }   
    }
}

fn create_permutations(to_permut:&Vec<usize>, m:&Vec<usize>, add_m:&Vec<usize>, add_n:&Vec<usize>, data: &SeasonData) {
    let len: usize = to_permut.len();
    let permuts = to_permut.into_iter().permutations(len);
    for perm in permuts {
        if (add_m.len() > 0) || (add_n.len() > 0){
            // println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
            add_repetition(m, &perm, add_m, add_n, data);
        } else {
            // println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
            check_possible_combination(&m,  &perm, data);
        }
    }
}

fn add_repetition(m:&Vec<usize>, perm:&Vec<&usize>, add_m:&Vec<usize>, add_n:&Vec<usize>, data: &SeasonData) {
    // println!("add_repetition m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
    let mut complete_m = Vec::<usize>::new();
    let mut complete_n = Vec::<&usize>::new();
    for i in 0..m.len() {
        complete_m.push(m[i])
    }
    
    for i in 0..perm.len() {
        complete_n.push(perm[i])
    }
    if add_m.len() > 0 {
        for i in 0..add_m.len() {
            complete_m.push(add_m[i])
        }
        for i in 0..perm.len() {
            complete_n.push(perm[i]);
            check_possible_combination(&complete_m, &complete_n, data);
            complete_n.pop();
        }
        // info!("Adding {} repetitions of m", add_m.len());
    }
    if add_n.len() > 0 {
        // info!("Adding {} repetitions of n", add_n.len());
        for i in 0..add_n.len() {
            complete_n.push(&add_n[i])
        }
        for i in 0..m.len() {
            complete_m.push(m[i]);
            check_possible_combination(&complete_m, &complete_n, data);
            complete_m.pop();
        }
    }
}

fn check_possible_combination(m:&Vec<usize>, n:&Vec<&usize>, data: &SeasonData) {
    println!("m:{:?} n:{:?}", m, n);
}

// fn calculate_affection()