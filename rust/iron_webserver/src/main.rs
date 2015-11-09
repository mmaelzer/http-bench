extern crate iron;

use iron::prelude::*;
use iron::status;


fn main() {
    println!("=== server listening on 127.0.0.1:8080 ===");
    println!("begin benchmark");

    fn hello_world(_: &mut Request) -> IronResult<Response> {
        Ok(Response::with((status::Ok, "Hello World")))
    }

    Iron::new(hello_world).http("127.0.0.1:8080").unwrap();
}
