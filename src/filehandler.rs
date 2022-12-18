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
    use super::*;
    // === Testing: read_file ===
    #[test]
    fn reading_file() {
        let text = read_file("./config.json");
    }

    #[test]
    fn read_missing_file() {
        fn reading_file() {
            let text = read_file("./missing-config.json");
        }
    }

    #[test]
    fn read_file_is_empty() {
        fn reading_file() {
            let text = read_file("./config.json");
        }
    }
}