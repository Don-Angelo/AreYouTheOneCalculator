use threadpool::ThreadPool;
use std::thread;
use std::sync::mpsc::channel;
use std::{collections::HashMap};
use factorial::Factorial;
use log::{debug, info};
use itertools::{Itertools, Permutations};
use crate::filehandler::{SeasonData, Pair};

#[derive(Debug)]
pub struct PossibilityResult {
    pub general_possibilitys: u32,
    pub possible_pairs: HashMap<Pair, u32>
}

impl PossibilityResult {
    pub fn add_result(&mut self, res: PossibilityResult) {

    }
}

#[derive(Debug, Clone)]
pub struct AytoCalculator {
    data: SeasonData,
    men_primary: bool,
    m: Vec<usize>,
    n: Vec<usize>,
    add_m: Vec<usize>,
    add_n: Vec<usize>,
    m_names: Vec<String>,
    n_names: Vec<String>
}

impl AytoCalculator {

    pub fn new(data: &SeasonData) -> AytoCalculator{
        // Constructor
        let men_primary: bool;
        if data.men.len() >= data.women.len() {
            men_primary = true;
        } else {
            men_primary = false;
        }

        let (m, n, add_m, add_n):(Vec<usize>, Vec<usize>, Vec<usize>, Vec<usize>) = get_mn(&men_primary, data);
        
        let (m_names, n_names) = get_mn_names(&men_primary, data);

        let calculator: AytoCalculator = AytoCalculator { 
            data: data.clone(),
            men_primary,
            m, n, add_m, add_n,
            m_names, n_names
        };
        return calculator;
    }

    pub fn calculate_possibilities(&mut self){
        let mut to_permut:Vec<usize> = Vec::<usize>::new();
        for i in 0..self.n.len() {
            to_permut.push(i);
        }
    
        if self.m.len() == self.n.len() {
            debug!("to_permut: {:?}", to_permut);
            self.create_permutations(to_permut);
        } else {
            info!("Adding {:?} persons of vector n a second time", self.m.len()-self.n.len());
            let mut j;
            for i in 0..self.n.len() {
                let mut extendet_to_permuts = Vec::<usize>::new();
                for i in 0..to_permut.len() {
                    extendet_to_permuts.push(to_permut[i]);
                }
                j = i;
                debug!("j: {:?}", j);
                while extendet_to_permuts.len() < self.m.len() {
                    extendet_to_permuts.push(j);
                    j = j + 1;
                    if j >= self.m.len() {j = 0}
                }
                if j > self.n.len() {break;}
                debug!("to_permut: {:?}", extendet_to_permuts);
                self.create_permutations(extendet_to_permuts);
            }   
        }
    }

    fn create_permutations(&mut self, to_permut: Vec<usize>) {
        let len: usize = to_permut.len();
        let permuts = to_permut.iter().permutations(len);
        
        self.process_in_threadpool(permuts);
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

    fn process_in_threadpool(&mut self, permuts: Permutations<core::slice::Iter<usize>>) {
        let perm_len = Factorial::factorial(&self.m.len());
    
        let result_data = PossibilityResult{general_possibilitys: 0, possible_pairs:HashMap::new()};
        let max_threads = thread::available_parallelism().unwrap(); // returns the number of recomended threads used as number of worker threads
        info!("Using {:?} threads to calculate.", max_threads);
        info!("Processing {:?} permutations.", perm_len);
        
    
        let pool = ThreadPool::new(usize::from(max_threads));
    
        let (tx, rx) = channel();
        for perm in permuts {
            let tx = tx.clone();
            let mut perm_clone  = Vec::<usize>::new();
            for i in 0..perm.len(){
                perm_clone.push(*perm[i]);
            }
            let calculator_clone = self.clone();
                
            // let perm_clone: Vec<&usize> = perm.cloned();
            pool.execute(move || {
                let mut calculator = calculator_clone;
                let m_clone = calculator.m.clone();
                if (calculator.add_m.len() > 0) || (calculator.add_n.len() > 0){
                    println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", calculator.m, perm_clone, calculator.add_m, calculator.add_n);
                            // add_repetition(&m_clone, &perm_clone, &add_m, &add_n, &data_clone);
                } else {
                    println!("m:{:?} n:{:?} add_m:{:?} add_n:{:?}", calculator.m, perm_clone, calculator.add_m, calculator.add_n);
                    
                    calculator.check_possible_combination(&m_clone,  &perm_clone);
                }
                   
                tx.send(perm_clone).expect("channel will be there waiting for the pool");
            });
        }
    
        //blocks until all work is done   
        for _ in 0..perm_len {
            debug!("Result from thread: {:?}", rx.recv().unwrap());
        }
    
        info!("All threads finished their work.");
        // return result_data;
         
    
    }

    fn add_repetition(&mut self, m:&Vec<usize>, perm:&Vec<usize>) {
        let mut complete_m = Vec::<usize>::new();
        let mut complete_n = Vec::<usize>::new();
        for i in 0..m.len() {
            complete_m.push(m[i])
        }
        
        for i in 0..perm.len() {
            complete_n.push(perm[i])
        }
        if self.add_m.len() > 0 {
            for i in 0..self.add_m.len() {
                complete_m.push(self.add_m[i])
            }
            for i in 0..perm.len() {
                complete_n.push(perm[i]);
                self.check_possible_combination(&complete_m, &complete_n);
                complete_n.pop();
            }
        }
        if self.add_n.len() > 0 {
            for i in 0..self.add_n.len() {
                complete_n.push(self.add_n[i])
            }
            for i in 0..m.len() {
                complete_m.push(m[i]);
                self.check_possible_combination(&complete_m, &complete_n);
                complete_m.pop();
            }
        }
    }



    fn check_possible_combination(&mut self, perm_m:&Vec<usize>, perm_n:&Vec<usize>) -> bool {
        println!("m:{:?} n:{:?}", perm_m, perm_n);
        let pairs = match self.create_pairs_from_permutations(perm_m, perm_n) {
            Ok(p) => p,
            Err(err) => {
                debug!("Err creating pairs: {}", err);
                drop(err);
                println!("NOT Possible");
                return false;
            }
        };
        for mnk in self.data.matching_nights.keys() {
            let mut matches: u8 = 0;
            for i in 0..pairs.len() {
                if self.data.matching_nights[mnk].pairs.contains(&pairs[i]) {
                    matches += 1;
                }
            }
            if matches > self.data.matching_nights[mnk].spots {
                println!("NOT Possible");
                return false;
            }
        }
        println!("Possible");
        return true;
    }
 
    fn create_pairs_from_permutations(&mut self, perm_m:&Vec<usize>, perm_n:&Vec<usize>) -> Result<Vec<Pair>, &'static str> {
        
        // let mut pairs: Result<Vec<Pair>, Err>;
        let mut pairs: Vec<Pair> = Vec::<Pair>::new();
        for i in 0..perm_m.len() {
            if self.men_primary {
                let p: Pair = Pair{
                    women: self.n_names[perm_n[i]].clone(), 
                    men: self.m_names[perm_m[i]].clone()
                };
                if p.is_no_match(&self.data) {
                    return Err("Pair is no match!");
                }
                pairs.push(p);
            } else {
                let p = Pair{ 
                    women: self.m_names[perm_m[i]].clone(), 
                    men: self.n_names[perm_n[i]].clone()
                };
                if p.is_no_match(&self.data) {
                    return Err("Pair is no match!");
                }
                pairs.push(p);
            }
            
        }
        return Ok(pairs);
    }

    







}

fn get_mn(men_primary:&bool ,data:&SeasonData) -> (Vec::<usize>, Vec::<usize>, Vec::<usize>, Vec::<usize>){
    let mut m= Vec::<usize>::new(); // Vector of the greater number of people
    let mut n= Vec::<usize>::new(); // Vector of the smaller number of people
    let mut add_m = Vec::<usize>::new();
    let mut add_n = Vec::<usize>::new();

    debug!("Men: {:?}", data.men);
    debug!("Women: {:?}", data.women);

    if *men_primary {
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

fn get_mn_names(men_primary:&bool, data: &SeasonData) -> (Vec::<String>, Vec::<String>) {
    /*
        Returns the names of m and n depending of the rules of m and n (m>=m)
     */
    let mut m:Vec<String> = Vec::<String>::new(); // Vector of the greater number of people
    let mut n:Vec::<String> = Vec::<String>::new(); // Vector of the smaller number of people

    if *men_primary {
        for i in 0..data.men.len() {
            m.push(data.men[i].clone());
        }
        for i in 0..data.women.len() {
            n.push(data.women[i].clone());
        }
        for i in 0..data.additional_men.len() {
            m.push(data.additional_men[i].clone());
        }
        for i in 0..data.additional_women.len() {
            n.push(data.additional_women[i].clone());
        }
    } else {
        for i in 0..data.men.len() {
            m.push(data.women[i].clone());
        }
        for i in 0..data.women.len() {
            n.push(data.men[i].clone());
        }
        for i in 0..data.additional_men.len() {
            m.push(data.additional_women[i].clone());
        }
        for i in 0..data.additional_women.len() {
            n.push(data.additional_men[i].clone());
        }
    }
    return (m,n);
}














// fn calculate_affection()