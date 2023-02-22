use threadpool::ThreadPool;
use std::thread;
use std::sync::mpsc::channel;
use std::{collections::HashMap, sync::Mutex};

use log::{debug, info};
use itertools::{Itertools, Permutations};
use crate::filehandler::{SeasonData, Pair};

#[derive(Debug)]
pub struct PossibilityResult {
    pub general_possibilitys: u32,
    pub possible_pairs: HashMap<Pair, u32>
}

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

fn get_mn_names(data: &SeasonData) -> (Vec::<&String>, Vec::<&String>) {
    let mut m:Vec::<&String> = Vec::<&String>::new(); // Vector of the greater number of people
    let mut n:Vec::<&String> = Vec::<&String>::new(); // Vector of the smaller number of people

    if data.men.len() >= data.women.len() {
        for i in 0..data.men.len() {
            m.push(&data.men[i]);
        }
        for i in 0..data.women.len() {
            n.push(&data.women[i]);
        }
        for i in 0..data.additional_men.len() {
            m.push(&data.additional_men[i]);
        }
        for i in 0..data.additional_women.len() {
            n.push(&data.additional_women[i]);
        }
    } else {
        for i in 0..data.men.len() {
            m.push(&data.women[i]);
        }
        for i in 0..data.women.len() {
            n.push(&data.men[i]);
        }
        for i in 0..data.additional_men.len() {
            m.push(&data.additional_women[i]);
        }
        for i in 0..data.additional_women.len() {
            n.push(&data.additional_men[i]);
        }
    }
    return (m,n);
}

fn men_are_primary(data: &SeasonData) -> bool {
    if data.men.len() >= data.women.len() {
        return true;
    } else {
        return false;
    }
}

pub fn calculate_possibilities(data: &SeasonData){
    let (m, n, add_m, add_n):(Vec<usize>, Vec<usize>, Vec<usize>, Vec<usize>) = get_mn(data);
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
    process_in_threadpool(permuts, m, add_m, add_n, data);
    // for perm in permuts {
    //     if (add_m.len() > 0) || (add_n.len() > 0){
    //         // println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
    //         add_repetition(m, &perm, add_m, add_n, data);
    //     } else {
    //         // println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
    //         check_possible_combination(&m,  &perm, data);
    //     }
    // }
}

fn add_repetition(m:&Vec<usize>, perm:&Vec<&usize>, add_m:&Vec<usize>, add_n:&Vec<usize>, data: &SeasonData) {
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
    }
    if add_n.len() > 0 {
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

fn create_pairs_from_permutations(m:&Vec<usize>, n:&Vec<&usize>, data: &SeasonData) -> Result<Vec<Pair>, &'static str> {
    let (m_names, n_names) = get_mn_names(data);
    // let mut pairs: Result<Vec<Pair>, Err>;
    let mut pairs: Vec<Pair> = Vec::<Pair>::new();
    for i in 0..m.len() {
        if men_are_primary(data) {
            let p = Pair{ 
                women: n_names[*n[i]].to_string(), 
                men: m_names[m[i]].to_string()
            };
            if p.is_no_match(data) {
                return Err("Pair is no match!");
            }
            pairs.push(p);
        } else {
            let p = Pair{ 
                women: m_names[m[i]].to_string(), 
                men: n_names[*n[i]].to_string()
            };
            if p.is_no_match(data) {
                return Err("Pair is no match!");
            }
            pairs.push(p);
        }
        
    }
    return Ok(pairs);
}

fn check_possible_combination(m:&Vec<usize>, n:&Vec<&usize>, data: &SeasonData) -> bool {
    println!("m:{:?} n:{:?}", m, n);
    let pairs = match create_pairs_from_permutations(m, n, data) {
        Ok(p) => p,
        Err(err) => {
            debug!("Err creating pairs: {}", err);
            drop(err);
            println!("NOT Possible");
            return false;
        }
    };
    for mnk in data.matching_nights.keys() {
        let mut matches: u8 = 0;
        for i in 0..pairs.len() {
            if data.matching_nights[mnk].pairs.contains(&pairs[i]) {
                matches += 1;
            }
        }
        if matches > data.matching_nights[mnk].spots {
            println!("NOT Possible");
            return false;
        }
    }
    println!("Possible");
    return true;
}


fn process_in_threadpool(permuts: Permutations<core::slice::Iter<usize>>, m:&Vec<usize>, add_m:&Vec<usize>, add_n:&Vec<usize>, data: &SeasonData) {
    
    // #TODO: calculate num of permutations
    let mut calculations = 0;
    let result_data = PossibilityResult{general_possibilitys: 0, possible_pairs:HashMap::new()};
    let max_threads = thread::available_parallelism().unwrap(); // returns the number of recomended threads used as number of worker threads
    info!("Using {:?} threads to calculate.", max_threads);

    
    let mut num_of_threds:u32 = 0;


    let n_jobs = 8;
    let pool = ThreadPool::new(usize::from(max_threads));

    let (tx, rx) = channel();
    for perm in permuts {
        calculations += 1;
        let tx = tx.clone();
        let m_clone = m.clone();
        let add_m_clone = add_m.clone();
        let add_n_clone = add_n.clone();
        let data_clone = data.clone();
        pool.execute(move|| {
            
                //  if (add_m.len() > 0) || (add_n.len() > 0){
                //         // println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
                //         add_repetition(m, &perm, add_m, add_n, data);
                //     } else {
                //         // println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", m, perm, add_m, add_n);
                //         check_possible_combination(&m,  &perm, data);
                //     }
            
            tx.send("test").expect("channel will be there waiting for the pool");
        });
    }

    //blocks until all work is done   
    for _ in 0..calculations {
        debug!("Result from thread: {:?}", rx.recv().unwrap());
    }
    info!("All threads finished their work.");
    // return result_data;


}


// fn calculate_affection()