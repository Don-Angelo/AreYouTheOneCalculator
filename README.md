# AreYouTheOneCalculator

## How To Run 
### Dependencies
The following dependencies are nessesary to build and run the program:

- The Rust language pack https://www.rust-lang.org/ (Tested with Rust v1.66.0) 
- Docker https://docs.docker.com/get-docker/
- Docker Compose https://docs.docker.com/compose/install/

### Run the program

    cargo run -- --help
    cargo run -- --season ./data/seasonY-XXXX/mnX.json

### Run with debug info
#### Windows

    $Env:RUST_log="info"; cargo run -- -s ./data/test/test1.json

### Run the tests

    cargo test