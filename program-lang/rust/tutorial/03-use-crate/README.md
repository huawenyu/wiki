# Doc

https://learnku.com/articles/31161

# Steps base on 02-cargo-hello

1. Change code like:

```rust
fn main() {
    let random_boolean = rand::random();
    println!("You {}!", if random_boolean { "win" } else { "lose" });
}
```

2. build & run
```shell
   $ cargo run
      Compiling hello v0.1.0 (/home/hyu/wiki/program-lang/rust/tutorial/03-use-crate/hello)
   error[E0433]: failed to resolve: use of undeclared type or module `rand`
    --> src/main.rs:2:26
     |
   2 |     let random_boolean = rand::random();
     |                          ^^^^ use of undeclared type or module `rand`

   error: aborting due to previous error

   For more information about this error, try `rustc --explain E0433`.
   error: could not compile `hello`.

   To learn more, run the command again with --verbose.
```

3. fix "use of undeclared type or module `rand`":

3.1 declare in Cargo.toml, by append the following into it:
```ini
   [dependencies]
   rand = "0.7.0"
```
   /// works fine
   $ cargo run

3.1.1 So far we have two entries:
   - our hello: `src/main.rs`
   - the entry of crate `rand`: itself's `src/lib.rs`


