# Doc

https://doc.rust-lang.org/cargo/getting-started/first-steps.html

# Steps

1. To start a new package with Cargo, use cargo new:
$ cargo new hello
Cargo defaults to --bin to make a binary program. To make a library, we'd pass --lib.

2. Let's check out what Cargo has generated for us:

```shell
   $ cd hello
   $ tree .
   .
   ├── Cargo.toml
   └── src
       └── main.rs
   1 directory, 2 files
```

3. let's check out `Cargo.toml`:

```ini
[package]
name = "hello_world"
version = "0.1.0"
authors = ["Your Name <you@example.com>"]
edition = "2018"

[dependencies]
This is called a manifest, and it contains all of the metadata that Cargo needs to compile your package.
```

4. code
Here's what's in src/main.rs:
```rust
fn main() {
    println!("Hello, world!");
}
```

5. build & run

   $ cargo build
   $ ./target/debug/hello
   Hello, world!

5.1 We can also use cargo run to compile and then run it, all in one step:

   $ cargo run
        Fresh hello_world v0.1.0 (file:///path/to/package/hello_world)
      Running `target/hello_world`

   Hello, world!

6. Clearn:
   $ cargo clean

