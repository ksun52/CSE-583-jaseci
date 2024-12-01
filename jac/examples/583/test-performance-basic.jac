import from time { time }

can is_prime(n: int) {
    if n <= 1 {
        return False;
    }
    for i in range(2, n) {
        if n % i == 0 {
            return False;
        }
    }
    return True;
}

with entry {
    t0 = time();
    ans = 0;
    for i in range(100000, 200000) {
        if is_prime(i) {
            ans = ans + 1;
        }
    }
    t1 = time();
    print(f'[python] {ans} | took {t1 - t0} seconds');
}