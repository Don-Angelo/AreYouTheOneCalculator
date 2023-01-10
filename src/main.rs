use clap::Parser;
use itertools::{Itertools};
use log::{info,debug};
use env_logger;
use std::io::ErrorKind;
use filehandler::{Config, SeasonData};
use filehandler::{read_file, parse_config, parse_data};

pub mod filehandler;

// ============================
// == Command line arguments ==
// ============================
#[derive(Parser)]
#[command(next_line_help = true)]
pub struct Args {
    #[arg(short, long)]
    /// Rel path to season data file
    season: Option<String> // if the parameter is optional: season: Option<String>
}

fn main(){
    env_logger::init();
    info!("Are You The One Calculator started");
    let args = Args::parse();

    if args.season.is_some(){

        info!("Reading config");
        let config_text = match read_file("./config.json") {
            Ok(text) => text,
            Err(err) => match err.kind() {
                ErrorKind::NotFound => {
                    panic!("Error: File not found");
                },
                _ => panic!("Error reading the data: {:?}", err), // catch all other errors
            }
        };
        debug!("Read config text: {}", config_text);
        let config: Config = match parse_config(config_text) {
            Ok(season_data) => season_data,
            Err(err) => panic!("Error parsing the data: {:?}", err), // catch all errors
        };
        debug!("Parsed config: {:?}", config);


        info!("Reading data: {:?}", args.season);        
        let text = match read_file(&args.season.unwrap()) {
            Ok(text) => text,
            Err(err) => match err.kind() {
                ErrorKind::NotFound => {
                    panic!("Error: File not found");
                },
                _ => panic!("Error reading the data: {:?}", err), // catch all other errors
            }
        };
        debug!("Read data: {}", text);
        let season_data: SeasonData = match parse_data(text) {
            Ok(season_data) => season_data,
            Err(err) => panic!("Error parsing the data: {:?}", err), // catch all errors
        };
        debug!("Parsed data: {:?}", season_data);
    } else {
        println!("Exiting program: The following arguments were not provided: -S <SEASON> or --season <SEASON> ");
        println!("Help with argument: -H or --Help");
    }

 

    let mut m = Vec::new();
    // let mut m = season_data["men"].as_array();
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

// ===========
// == Tests ==
// ===========
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let result = 2 + 2;
        assert_eq!(result, 4);
    }
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
    let len: usize = to_permut.len();
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
    println!("add_repetition, current permutation: {:?}, smaller len: {:?}, desired len: {:?}", perm, smaller_len, desired_len);
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