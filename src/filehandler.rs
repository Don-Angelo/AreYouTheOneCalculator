use std::{fs::File};
use std::io::Read;
use std::io;

pub fn read_file(filename: &str) -> io::Result<String> {
    let mut file = File::open(filename)?;
    let mut text = String::new();
    file.read_to_string(&mut text)?;
    Ok(text)
}

// ===========
// == Tests ==
// ===========
#[cfg(test)]
mod tests {
    use std::io::ErrorKind;
    use super::*;

    #[test]
    fn reading_file() {
        match read_file("./config.json") {
            Ok(_) => assert!(true),
            Err(_) => assert!(false),
        };
    }

    #[test]
    fn read_missing_file() {
        match read_file("./missing-config.json") {
            Ok(_) => assert!(false),
            Err(err) => match err.kind() {
                ErrorKind::NotFound => assert!(true),
                _ => assert!(false), // catch all other errors
            },
        };
    }
}