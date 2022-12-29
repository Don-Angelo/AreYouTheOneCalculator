# AreYouTheOneCalculator

## 1. How To Run 
### 1.1. Dependencies
The following dependencies are nessesary to build and run the program:

- The Rust language pack https://www.rust-lang.org/ (Tested with version 1.66.0) 
- Docker & Docker Compose https://docs.docker.com/get-docker/ (Testet with version 4.15.0)
- neo4j database docker container https://hub.docker.com/_/neo4j

### 1.1. Database
To run the program the database has to be started first:

    docker compose up -d

### 1.2 Run the program

    cargo run -- --help
    cargo run -- --season ./data/seasonY-XXXX/mnX.json

#### Run with debug info
##### Windows

    $Env:RUST_log="info"; cargo run -- -s ./data/test/test1.json

#### Run the tests

    cargo test