import math
import secrets
from collections import defaultdict
import time
import sys
import multiprocessing as mp
import os


class ProgressLogger:
    def __init__(self, total, label="Progress"):
        self.total = total
        self.label = label
        self.start = time.time()
        self.last_print = 0

    def update(self, done):
        now = time.time()
        if now - self.last_print < 0.5 and done < self.total:
            return
        self.last_print = now

        percent = done * 100 // self.total
        elapsed = now - self.start
        eta = (elapsed / done * (self.total - done)) if done > 0 else 0

        sys.stdout.write(
            f"\r[{self.label}] {percent:3d}% "
            f"({done}/{self.total}) "
            f"elapsed={elapsed:6.1f}s "
            f"eta={eta:6.1f}s"
        )
        sys.stdout.flush()

    def finish(self):
        self.update(self.total)
        print()

def aks_congruence_check(args):
    a, n, r, x_n = args

    base = [a % n] + [0] * (r - 1)
    base[1 % r] = (base[1 % r] + 1) % n

    left = poly_pow(base, n, n, r)

    right = x_n[:]
    right[0] = (right[0] + a) % n

    return left == right


def is_perfect_power(n: int) -> bool:
    if n <= 1:
        return False
    max_b = int(math.log2(n)) + 1
    for b in range(2, max_b + 1):
        a = int(round(n ** (1.0 / b)))
        if a > 1 and pow(a, b) == n:
            return True
    return False

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def factorize(n: int) -> dict:
    factors = defaultdict(int)
    x = n
    while x % 2 == 0:
        factors[2] += 1
        x //= 2
    f = 3
    while f * f <= x:
        while x % f == 0:
            factors[f] += 1
            x //= f
        f += 2
    if x > 1:
        factors[x] += 1
    return dict(factors)

def euler_phi(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    fac = factorize(n)
    phi = n
    for p in fac.keys():
        phi = phi // p * (p - 1)
    return phi

def multiplicative_order(n: int, r: int) -> int:
    if gcd(n, r) != 1:
        return 0
    phi_r = euler_phi(r)
    divisors = []
    for d in range(1, int(math.isqrt(phi_r)) + 1):
        if phi_r % d == 0:
            divisors.append(d)
            if d * d != phi_r:
                divisors.append(phi_r // d)
    divisors.sort()
    for d in divisors:
        if pow(n % r, d, r) == 1:
            return d
    return phi_r

def poly_add(a, b, n_mod, r):
    m = max(len(a), len(b), r)
    out = [0] * m
    for i in range(m):
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0
        out[i % r] = (out[i % r] + ai + bi) % n_mod
    return out[:r]

def poly_mul(a, b, n_mod, r):
    out = [0] * r
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0:
                continue
            out[(i + j) % r] = (out[(i + j) % r] + ai * bj) % n_mod
    return out

def poly_pow(base, exp, n_mod, r):
    result = [0] * r
    result[0] = 1
    b = base[:]
    e = exp
    while e > 0:
        if e & 1:
            result = poly_mul(result, b, n_mod, r)
        b = poly_mul(b, b, n_mod, r)
        e >>= 1
    return result


def aks_is_prime(n: int, parallel=True) -> bool:
    if n < 2:
        return False
    if is_perfect_power(n):
        return False

    log2n = math.log2(n)
    bound = int(math.ceil(log2n * log2n))

    # Step 1–2: tìm r
    r = 2
    while True:
        if 1 < gcd(n, r) < n:
            return False
        if multiplicative_order(n, r) > bound:
            break
        r += 1

    # Step 3
    for a in range(2, r + 1):
        g = gcd(a, n)
        if 1 < g < n:
            return False

    if n <= r:
        return True

    # Step 5: đồng dư
    phi_r = euler_phi(r)
    A = int(math.floor(math.sqrt(phi_r) * math.log(n)))

    x_n = [0] * r
    x_n[n % r] = 1

    print(f"[AKS] r = {r}, φ(r) = {phi_r}, A = {A}")
    print(f"[AKS] Parallel = {parallel}, CPU = {os.cpu_count()}")

    progress = ProgressLogger(A, label="AKS congruence")

    if parallel:
        with mp.Pool(os.cpu_count()) as pool:
            done = 0
            print("[AKS] Starting congruence checks...")
            sys.stdout.flush()
            for ok in pool.imap_unordered(
                aks_congruence_check,
                ((a, n, r, x_n) for a in range(1, A + 1)),
                chunksize=1        # 🔥 RẤT QUAN TRỌNG
            ):
                done += 1
                progress.update(done)
                if not ok:
                    pool.terminate()
                    print("\n[AKS] Congruence failed")
                    return False
    else:
        for a in range(1, A + 1):
            if not aks_congruence_check((a, n, r, x_n)):
                return False
            progress.update(a)

    progress.finish()
    return True

def random_128bit_odd() -> int:
    n = secrets.randbits(128)
    n |= (1 << 127)  
    n |= 1           
    return n

def generate_prime_128bit_aks():
    attempt = 0
    while True:
        attempt += 1
        candidate = random_128bit_odd()

        for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
            if candidate % p == 0:
                candidate += 2

        print(f"\n[Attempt {attempt}] Testing candidate... {candidate}")
        if aks_is_prime(candidate, parallel=True):
            print(f"Found 128-bit prime after {attempt} attempts.")
            return candidate


if __name__ == "__main__":
    prime = generate_prime_128bit_aks()
    print("128-bit prime:", prime)
