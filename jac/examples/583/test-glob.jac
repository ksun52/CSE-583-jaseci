glob z = 20.1;

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

with entry {
    edits_local_from_glob();
    edits_glob();
    uses_glob();
}