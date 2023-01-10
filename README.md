# AreYouTheOneCalculator

# 1. How To Run 
## 1.1. Dependencies
The following dependencies are nessesary to build and run the program:

- The Rust language pack https://www.rust-lang.org/ (Tested with version 1.66.0) 
- Docker & Docker Compose https://docs.docker.com/get-docker/ (Testet with version 4.15.0)

## 1.2. Database
To run the program the database has to be started first:

    docker compose up -d

You can now access the web interface of the database at http://localhost:7474/  
default user: neo4j  
temporary password: neo4j (you have to change it at the first login)

### 1.2.1 Database configuration
If you are starting the database the first time you have to configure the db.

## 1.3 Run the program

    cargo run -- --help
    cargo run -- --season ./data/seasonY-XXXX/mnX.json

### Run with debug info
#### Windows

    $Env:RUST_log="info"; cargo run -- -s ./data/test/test1.json

### Run the tests

    cargo test