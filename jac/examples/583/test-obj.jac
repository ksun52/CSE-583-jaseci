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

with entry {
    car = Car("Toyota", "Camry", 2020);
    car.display_car_info();
    car.obj_edits_a_static();
    car.obj_edits_itself();
    car.obj_print_func();
}