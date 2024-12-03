glob z = 20.1;
glob l = 1;

can print_hello {
        print("hello");
    }


can uses_glob(b: float) {
        print(z + b + l);
        print_hello();
    }

can edits_glob {
        :g: z ;
        z = 3.2;
    }

can do_nothing {
        a = 3.2;
    }

can edits_local_from_glob(b: float) -> float {
        b = 3.2;
        return b;
    }

with entry {
    b = 12.3;
    edits_local_from_glob(b);
    edits_glob();
    uses_glob(b);
    print(b);
    do_nothing();
}