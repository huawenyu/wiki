mod math {
    pub fn add(x: i32, y: i32) -> i32 {
        x + y
    }
}

fn main() {
    let result = math::add(1, 2);
    println!("1 + 2 = {}", result);
}

