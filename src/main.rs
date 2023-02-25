use clap::Parser;
use std::io::ErrorKind;
use filehandler::{Config, SeasonData};
use filehandler::{read_file, parse_config, parse_data};

use crate::are_you_the_one_calculator::AytoCalculator;


pub mod filehandler;
pub mod are_you_the_one_calculator;

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
    println!("Are You The One Calculator started");
    let args = Args::parse();

    if args.season.is_none(){
        println!("Exiting program: The following arguments were not provided: -S <SEASON> or --season <SEASON> ");
        println!("Help with argument: -H or --Help");
        return;
    }

    let config_text = match read_file("./config.json") {
        Ok(text) => text,
        Err(err) => match err.kind() {
            ErrorKind::NotFound => {
                panic!("Error: File not found");
            },
            _ => panic!("Error reading the data: {:?}", err), // catch all other errors
        }
    };

    let config: Config = match parse_config(config_text) {
        Ok(season_data) => season_data,
        Err(err) => panic!("Error parsing the data: {:?}", err), // catch all errors
    };

    let text = match read_file(&args.season.unwrap()) {
        Ok(text) => text,
        Err(err) => match err.kind() {
            ErrorKind::NotFound => {
                panic!("Error: File not found");
            },
            _ => panic!("Error reading the data: {:?}", err), // catch all other errors
        }
    };

    let season_data: SeasonData = match parse_data(text) {
        Ok(season_data) => season_data,
        Err(err) => panic!("Error parsing the data: {:?}", err), // catch all errors
    };

    let mut calculator: AytoCalculator = AytoCalculator::new(&season_data);
    calculator.calculate_possibilities();   
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