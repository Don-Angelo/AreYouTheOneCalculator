# AreYouTheOneCalculator

## How To Run 
### Dependencies
This program is written in rust, to build the executable you have to install the Rust language pack and the cargo packet manager. https://www.rust-lang.org/

### Run the program

    cargo run -- --help
    cargo run -- --season ./data/seasonY-XXXX/mnX.json

### Run with debug info
#### Windows

    $Env:RUST_log="info"; cargo run -- -s ./data/test/test1.json

### Run the tests

    cargo test