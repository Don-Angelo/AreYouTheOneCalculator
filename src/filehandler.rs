use std::collections::HashMap;
use std::{fs::File};
use std::io::Read;
use std::io;
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Pair {
    women: String,
    men: String
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MatchboxResult {
    perfect_match: Vec<Pair>,
    no_match: Vec<Pair>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MatchingNight {
    pairs: Vec<Pair>,
    spots: u8
}

#[derive(Debug, Serialize, Deserialize)]
pub struct GamePairs {
    pairs: Vec<Pair>
}


#[derive(Debug, Serialize, Deserialize)]
pub struct SeasonData {
    women: Vec<String>,
    men: Vec<String>,
    additional_women: Vec<String>,
    additional_men: Vec<String>,
    matchbox_results: HashMap<u8,MatchboxResult>,
    matching_nights: HashMap<u8,MatchingNight>,
    game_selections: HashMap<u8,Vec<Pair>>
}

pub fn read_file(filename: &str) -> io::Result<String> {
    let mut file = File::open(filename)?;
    let mut text = String::new();
    file.read_to_string(&mut text)?;
    Ok(text)
}

pub fn parse_data(data: String) -> io::Result<SeasonData> {
    let season_data: SeasonData = serde_json::from_str(&data)?;
    
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
        match read_file("./data/test/test1.json") {
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
        let valid_json :String = String::from("{\"women\": [\"W1\",\"W2\"],\"men\":[\"M1\",\"M2\"],\"additional_women\": [],\"additional_men\": [\"M3\"],\"matchbox_results\":{\"1\":{\"perfect_match\": [],\"no_match\": [{\"women\":\"W2\", \"men\": \"M3\"}]}},\"matching_nights\": {\"1\": {\"pairs\": [{\"women\":\"W1\", \"men\": \"M1\"},{\"women\":\"W2\", \"men\": \"M2\"}],\"spots\": 1}},\"game_selections\": {\"1\": [{\"women\":\"W1\", \"men\": \"M1\"},{\"women\":\"W2\", \"men\": \"M2\"}]}}");
        match parse_data(valid_json) {
            Ok(_) => assert!(true),
            Err(_) => assert!(false)
        };
    }
    #[test]
    fn parse_invalid_json() {
        let invalid_json :String = String::from("{\"women\": [\"W1\",\"W2\"]\"men\":[\"M1\",\"M2\"],\"additional_women\": [],\"additional_men\": [\"M3\"],\"matchbox_results\":{\"1\":{\"perfect_match\": [],\"no_match\": [{\"women\":\"W2\", \"men\": \"M3\"}]}},\"matching_nights\": {\"1\": {\"pairs\": [{\"women\":\"W1\", \"men\": \"M1\"},{\"women\":\"W2\", \"men\": \"M2\"}],\"spots\": 1}},\"game_selections\": {\"1\": [{\"women\":\"W1\", \"men\": \"M1\"},{\"women\":\"W2\", \"men\": \"M2\"}]}}");
        match parse_data(invalid_json) {
            Ok(_) => assert!(false),
            Err(_) => assert!(true)
        };
    }
}