# Doc

https://learnku.com/articles/31161

# Steps

Steps base on 02-cargo-hello

## add module directly in `main.rs`

0. Remove 03-cargo's Cargo.toml [dependencies]

1. Change code like:

```rust
mod math {
    pub fn add(x: i32, y: i32) -> i32 {
        x + y
    }
}

fn main() {
    let result = math::add(1, 2);
    println!("1 + 2 = {}", result);
}

```
1.1 So far we have crate modules:
    - `math`

2. build & run
```shell
   $ cargo run
   1 + 2 = 3
```

## add module by file

3. Move our new module `math` code from `src/main.rs` into a new file, `src/math.rs`:

   $ cargo new hello_split
   $ cd hello_split
   $ vi src/math.rs

```rust
pub fn add(x: i32, y: i32) -> i32 {
    x + y
}
```

4. keep `src/main.rs` like:

```rust
fn main() {
    let result = math::add(1, 2);
    println!("1 + 2 = {}", result);
}
```

5. cargo run
     error: use of undeclared type or module `math`

     虽然 src/main.rs 和 src/lib.rs（二进制和库项目）会被 cargo 自动识别为程序入口，其他文件则需要在文件中明确声明。
     我们的错误在于仅仅创建了 src/math.rs 文件，希望 cargo 会在构建时找到它，但事实上并不是这样的。cargo 甚至不会解析它。

6. Notify cargo from it's known entry src/main.rs:

```rust
/// insert into src/main.rs
mod math;
```

7. work fine:
   $ cargo run

7.1 tree:

```
   src/
       main.rs
       math.rs
```

7.2 So far the main module(we are here):
   - module `math`: `src/main.rs`
     + function `add`

## add sub-module by dir: if the sub-module is complex

```
src/
    main.rs
    math/
        mod.rs
        add.rs (new file)
        sub.rs (anoth new file)
```

### Using mod.rs to export module

$ cat `src/math/mod.rs`

``` rust
pub mod add;
pub mod sub;
```

So now our modules like:

   crate (we are here)
       module `math`
           module `add`
               function `add`
           module `sub`
               `sub`

   $ cargo run
   error: `add` not a function

### Cut-through the middle module

$ cat `src/math/mod.rs`

``` rust
// Make sub-module private
mod add;
mod sub;

// export functions
pub use add::add;
pub use sub::sub;
```

So now our modules like:

`math` 模块 (we are here)
    function: `add`
    function: `sub`
    module `add` (private)
        function: `add`
    module `sub` (private)
        function: `sub`

   $ work fine: cargo run

### candy `use`: import use to shorter the call path

$ cat `src/main.rs`:
```rust
mod math;
use math::{add, sub};

fn main() {
    let result = add(1, 2);
    println!("1 + 2 = {}", result);
}
```
