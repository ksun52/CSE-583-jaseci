import:py codon;

can do_nothing() -> None {
    print("tester function");
}

@do_nothing
can sum(a: int, b: int) -> int {
    return a + b;
}
