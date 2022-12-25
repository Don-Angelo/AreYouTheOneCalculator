use std::{fs::File};
use std::io::Read;
use std::io;

pub struct Person {
    name: String
}

pub struct Pair {
    person1: Person,
    person2: Person
}
// impl is possible

pub struct MatchboxResult {
    number: u8,
    perfect_match: Vec<Pair>,
    no_match: Vec<Pair>,
}

pub struct MatchingNight {
    number: u8,
    pairs: Vec<Pair>,
    lights: u8
}

pub struct SeasonData {
    women: Vec<Person>,
    men: Vec<Person>,
    additional_women: Vec<Person>,
    additional_men: Vec<Person>,
    matchbox_results: Vec<MatchboxResult>,
    matching_nights: Vec<MatchingNight>
}

pub fn read_file(filename: &str) -> io::Result<String> {
    let mut file = File::open(filename)?;
    let mut text = String::new();
    file.read_to_string(&mut text)?;
    Ok(text)
}

pub fn parse_data(data: String) -> io::Result<SeasonData> {
    let season_data: SeasonData;
    Ok(season_data)
}

// ===========
// == Tests ==
// ===========
#[cfg(test)]
mod tests {
    use std::io::ErrorKind;
    use super::*;

    // == tests for fn read_file ==
    #[test]
    fn reading_file() {
        match read_file("./test/test1.json") {
            Ok(_) => assert!(true),
            Err(_) => assert!(false),
        };
    }
    #[test]
    fn read_missing_file() {
        match read_file("./missing-file.json") {
            Ok(_) => assert!(false),
            Err(err) => match err.kind() {
                ErrorKind::NotFound => assert!(true),
                _ => assert!(false), // catch all other errors
            },
        };
    }

    // == tests for fn parse_data ==
    #[test]
    fn parse_valid_json() {
    }
    #[test]
    fn parse_invalid_json() {
    }
}