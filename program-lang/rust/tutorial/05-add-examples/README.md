# Doc

http://xion.io/post/code/rust-examples.html

In Cargo's parlance, an example is nothing else but a Rust source code of a standalone executable1 that typically resides in a single .rs file. All such files should be places in the examples/ directory, at the same level as src/ and the Cargo.toml manifest itself2.

# Steps

1. add a hello.rs into dir examples:
   $ cat examples/hello.rs
```rust
// examples/hello.rs
fn main() {
    println!("Hello from an example!");
}
```

2. build & run

   $ cd tutorial/05-add-examples/hello
   $ cargo run --example hello

3. Another hello2

   $ cat examples/hello.rs
```rust
// examples/hello2.rs
use std::env;

fn main() {
    let name = env::args().skip(1).next();
    println!("Hello, {}!", name.unwrap_or("world".into()));
}
```

4. run hello2

   $ cargo run --example hello2 -- Alice
   Hello, Alice!

