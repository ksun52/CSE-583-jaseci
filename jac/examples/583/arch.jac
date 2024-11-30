glob z = 20.1;

enum Color;
:enum:Color {
    RED = 1,
    GREEN = 2
}

obj Car {
    has make: str,
        model: str,
        year: int;
    static has wheels: int = 4;

    can obj_edits_a_static {
        Car.wheels = 5;
    }
    can obj_print_func {
        print(f"Car Info: {self.year} {self.make} {self.model}");
    }
    can obj_edits_itself {
        year = 2022;
    }
}

class Animal {
    has species: str;

    can class_print_func {
        print(f"Animal Info: {self.species}");
    }
}

node Pet :Animal: {
    can node_inherited_func {
        print("Pet function");
    }
}

can simple_func(a: float, b: float) -> float {
        return a * b;
    }

can uses_glob(b: float) {
        print(z + b);
    }

can edits_glob {
        :g: z ;
        z = 3.2;
    }

can edits_local_from_glob() -> float {
        z = 3.2;
        return z;
    }

can uses_enum {
    print(Color.RED.value);
}

with entry {
    car = Car("Toyota", "Camry", 2020);
    car.display_car_info();

    animal = Animal("Cat")
    animal.display_animal_info();
}