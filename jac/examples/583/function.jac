can do_nothing() -> None {
    print("tester function");
}

@codon.jit
can sum(a: int, b: int) -> int {
    return a + b;
}
