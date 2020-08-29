# Docs

https://rustcc.gitbooks.io/rustprimer/content/macro/macro.html
https://kaisery.github.io/trpl-zh-cn/ch15-05-interior-mutability.html

## QuickStart

### Setup env for R&D

https://hoverbear.org/blog/setting-up-a-rust-devenv/

## Best Rust IDE

IntelliJ IDEA (Comunity Version) + Rust plugin + Vim plugin

## vim plugs

### tags
https://github.com/dan-t/rusty-tags

Base on ctags:

    $ cargo install rusty-tags
    /// generate tags for vi
    $ rusty-tags vi
    $ rustup component add rust-src

    ///tags names: Put this into your ~/.vimrc file:
      autocmd BufRead *.rs :setlocal tags=./rusty-tags.vi;/
    /// <or> reuse the old name
    rusty-tags vi --output=".tags".

### work-with coc.vim

https://github.com/neoclide/coc-rls

Execute vim command like this:
:CocInstall coc-rls

# Language

## file struct
https://doc.rust-lang.org/stable/rust-by-example/mod/split.html
https://riptutorial.com/rust/example/29562/basic-code-organization

## modules

https://journal.infinitenegativeutility.com/the-basic-principles-of-rust-modules

## Macro

match type: ident, expr, block, stmt, ...
https://riptutorial.com/rust/example/5646/fragment-specifiers---kind-of-patterns

## lifetime

Q: [What is &'a in Rust Language](https://stackoverflow.com/questions/47640550/what-is-a-in-rust-language)
Understood & is for shared reference but did not understand what is the difference between type and 'a in Rust language

In another location I read this code:

#[derive(Debug)]
struct Person<'a> {
    name: &'a str,
    age: u8
}

fn main() {
    let name = "Peter";
    let age = 27;
    let peter = Person { name, age };

    // Pretty print
    println!("{:#?}", peter);
}
What does 'a in the struct Person<'a> { } means? and can I build the same struct using struct Person<'type> { } or struct Person<T> { }?

And what is the meaning of name: &'a str?

And how can I re-code it, if want to avoid using the <'a>


A:

I found [this][1] and [this][2] and [this][3] and [this][4] that explains my question.

The `'a` reads ‘the lifetime a’. Technically, every reference has some lifetime associated with it, but the compiler lets you elide (i.e. omit, see "[Lifetime Elision][5]") them in common cases.

    fn bar<'a>(...)

A function can have ‘generic parameters’ between the `<>`s, of which lifetimes are one kind. The `<>` is used to declare lifetimes. This says that bar has one lifetime, 'a.

Rust has two main types of strings: `&str` and `String`. The `&str` are called `‘string slices’`. A string slice has a fixed size, and cannot be mutated. It is a reference to a sequence of UTF-8 bytes.

    let greeting = "Hello there."; // greeting: &'static str

"Hello there." is a `string literal` and its type is `&'static str`. A string literal is a string slice that is statically allocated, meaning that it’s saved inside our compiled program, and exists for the entire duration it runs. The greeting binding is a reference to this statically allocated string. Any function expecting a string slice will also accept a string literal.

In the above example

    struct Person<'a> {  }

requires to contain `<'a>` as the `name` is defined using:

    name: &'a str,

which is called by:

    let name = "Peter";

If interested to avoid the usage of `'a` then the above code can be re-written as:

    #[derive(Debug)]
    struct Person {    // instead of: struct Person<'a> {
        name: String,  // instead of: name: &'a str
        age: u8
    }

    fn main() {
        let name = String::from("Peter");  // instead of: let name = "Peter"; which is &'static str
        let age = 27;
        let peter = Person { name, age };

        // Pretty print
        println!("{:#?}", peter);
    }


  [1]: https://doc.rust-lang.org/book/second-edition/ch10-03-lifetime-syntax.html#lifetime-annotation-syntax
  [2]: https://doc.rust-lang.org/book/second-edition/ch19-02-advanced-lifetimes.html
  [3]: https://doc.rust-lang.org/1.6.0/book/lifetimes.html
  [4]: https://doc.rust-lang.org/1.6.0/book/strings.html
  [5]: https://doc.rust-lang.org/1.6.0/book/lifetimes.html#lifetime-elision

# Samples

