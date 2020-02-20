use log::{info};
use log4rs;

fn main() {
    // https://docs.rs/log4rs/0.10.0/log4rs/#encoders
    log4rs::init_file("./config/log4rs.yaml", Default::default()).unwrap();

    info!("booting up");
    info!("booting down");
}
