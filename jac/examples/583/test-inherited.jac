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



with entry {
    animal = Animal("Cat");
    animal.display_animal_info();
    pet = Pet();
    pet.node_inherited_func();
}