use std::collections::HashMap;
use std::ptr::eq;
use std::{fs::File};
use std::io::Read;
use std::{io};
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct DBConfig {
    pub host: String,
    pub port: u16,
    pub username: String,
    pub password: String
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub dbconfig: DBConfig
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Pair {
    pub women: String,
    pub men: String
}

impl Pair {
    pub fn is_no_match(&self, data: &SeasonData) -> bool {
        for i in 0..data.no_match.len() {
            if eq(self, &data.no_match[i]) {
                return true; 
            }
        }
        return false;
    }
    pub fn is_perfect_match(&self, data: &SeasonData) -> bool {
        for i in 0..data.perfect_match.len() {
            if eq(self, &data.perfect_match[i]) {
                return true; 
            }
        }
        return false;
    }
    pub fn eq(&self, other: &Pair) -> bool {
        (self.men == other.men) && (self.women == other.women)
    }
}

impl PartialEq for Pair {
    fn eq(&self, other: &Self) -> bool {
        (self.men == other.men) && (self.women == other.women)
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct MatchboxResult {
    pub perfect_match: Vec<Pair>,
    pub no_match: Vec<Pair>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct MatchingNight {
    pub pairs: Vec<Pair>,
    pub spots: u8
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SeasonData {
    pub women: Vec<String>,
    pub men: Vec<String>,
    pub additional_women: Vec<String>,
    pub additional_men: Vec<String>,
    pub matchbox_results: HashMap<u8,MatchboxResult>,
    pub matching_nights: HashMap<u8,MatchingNight>,
    pub game_selections: HashMap<u8,Vec<Pair>>,
    pub perfect_match: Vec<Pair>,
    pub no_match: Vec<Pair>
}

pub fn read_file(filename: &str) -> io::Result<String> {
    let mut file = File::open(filename)?;
    let mut text = String::new();
    file.read_to_string(&mut text)?;
    Ok(text)
}

pub fn parse_config(data: String) -> io::Result<Config> {
    let config: Config = serde_json::from_str(&data)?;
    Ok(config)
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
        match read_file("./config.json") {
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

    // == tests for fn parse_config ==
    #[test]
    fn parse_valid_config() {
        let valid_json :String = String::from("{\"dbconfig\": {\"host\":\"0.0.0.0\",\"port\":123,\"username\":\"test\",\"password\":\"Passw0rd\"}}");
        match parse_config(valid_json) {
            Ok(_) => assert!(true),
            Err(_) => assert!(false)
        };
    }
    #[test]
    fn parse_invalid_config() {
        let invalid_json :String = String::from("{\"dbconfig\": {\"port\":123,\"username\":\"test\",\"password\":\"Passw0rd\"}}");
        match parse_config(invalid_json) {
            Ok(_) => assert!(false),
            Err(_) => assert!(true)
        };
    }

    // == tests for fn parse_data ==
    #[test]
    fn parse_valid_json() {
        let valid_json :String = String::from("{\"women\": [\"W1\",\"W2\"],\"men\":[\"M1\",\"M2\"],\"additional_women\": [],\"additional_men\": [\"M3\"],\"matchbox_results\":{\"1\":{\"perfect_match\": [],\"no_match\": [{\"women\":\"W2\", \"men\": \"M3\"}]}},\"matching_nights\": {\"1\": {\"pairs\": [{\"women\":\"W1\", \"men\": \"M1\"},{\"women\":\"W2\", \"men\": \"M2\"}],\"spots\": 1}},\"game_selections\": {\"1\": [{\"women\":\"W1\", \"men\": \"M1\"},{\"women\":\"W2\", \"men\": \"M2\"}]},\"perfect_match\":[],\"no_match\":[]}");
        match parse_data(valid_json) {
            Ok(_) => assert!(true),
            Err(_) => assert!(false)
        };
    }
    #[test]
    fn parse_invalid_json() {
        let invalid_json :String = String::from("{\"women\": [\"W1\",\"W2\"]\"men\":[\"M1\",\"M2\"],\"additional_women\": [],\"additional_men\": [\"M3\"],\"matchbox_results\":{\"1\":{\"perfect_match\": [],\"no_match\": [{\"women\":\"W2\", \"men\": \"M3\"}]}},\"matching_nights\": {\"1\": {\"pairs\": [{\"women\":\"W1\", \"men\": \"M1\"},{\"women\":\"W2\", \"men\": \"M2\"}],\"spots\": 1}},\"game_selections\": {\"1\": [{\"women\":\"W1\", \"men\": \"M1\"},{\"women\":\"W2\", \"men\": \"M2\"}]},\"perfect_match\":[],\"no_match\":[]}");
        match parse_data(invalid_json) {
            Ok(_) => assert!(false),
            Err(_) => assert!(true)
        };
    }
}