/*
https://hub.packtpub.com/shared-pointers-in-rust-challenges-solutions/

Let's start with the basic Cell structure.
A Cell will contain a mutable value, but it can be mutated without having a mutable Cell.

It has mainly three interesting methods: set(), swap(), and replace().
The first allows us to set the contained value, replacing it with a new value.
The previous structure will be dropped (the destructor will run).
That last bit is the only difference with the replace() method.
In the replace() method, instead of dropping the previous value, it will be returned.
The swap() method, on the other hand, will take another Cell and swap the values between the two.
All this without the Cell needing to be mutable.
 */
use std::cell::Cell;

#[derive(Copy, Clone)]
struct House {
    bedrooms: u8,
}

impl Default for House {
    fn default() -> Self {
        House { bedrooms: 1 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /* As you can see in the example, to use a Cell, the contained type must be Copy.
    If the contained type is not Copy, you will need to use a RefCell, which we will see next.
    */
    #[test]
    fn test_cell()
    {
        let house2 = House { bedrooms: 2 };
        let house5 = House { bedrooms: 5 };

        let cell2 = Cell::new(house2);
        println!("The cell2 has {} bedrooms.", cell2.get().bedrooms);

        cell2.set(house5);
        println!("cell.set(5): the cell2 has {} bedrooms", cell2.get().bedrooms);
        let old_house = cell2.replace(house2);
        println!(
            "cell.replace(2): cell2 has {} bedrooms, and the old_house has {} bedrooms",
            cell2.get().bedrooms,
            old_house.bedrooms
        );

        let cell5 = Cell::new(house5);
        cell2.swap(&cell5);
        println!(
            "cell.swap(cell5): cell2 has {} bedrooms, cell5 has {} bedrooms",
            cell2.get().bedrooms,
            cell5.get().bedrooms
        );

        /*
        the take() method, only available for types implementing the Default trait.
        This method will return the current value, replacing it with the default value.
        As you can see, you don't really mutate the value inside, but you replace it with another value.
        You can either retrieve the old value or lose it.
        That's why you can only use elements implementing Copy with a Cell.
        This also means that a Cell does not need to dynamically check borrows at runtime.
         */
        let cell2_take = cell2.take();
        println!(
            "cell2_take has {} bedrooms, the shared one {}",
            cell2_take.bedrooms,
            cell2.get().bedrooms
        );
    }
}