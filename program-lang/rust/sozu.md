# Doc
https://github.com/sozu-proxy/sozu

# Build

    /// at least version >= 1.40
    $ cargo update
    $ rustc update

    $ git clone https://github.com/sozu-proxy/sozu.git
    $ cd sozu
    $ cd ctl && cargo build; cd ../bin && cargo build

# QuickStart

    $ cd sozu
    $ RUST_BACKTRACE=full ./target/debug/sozu start --config ./bin/config.toml

    /// Open a new terminal:
    $ curl http://localhost:808

