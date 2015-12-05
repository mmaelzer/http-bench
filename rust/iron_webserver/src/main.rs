extern crate iron;

use iron::prelude::*;
use iron::status;


fn main() {
    println!("=== server listening on 127.0.0.1:8080 ===");
    println!("begin benchmark");

    Iron::new(|_: &mut Request| {
        Ok(Response::with((status::Ok, "Hello world")))
    }).http("127.0.0.1:8080").unwrap();
}
