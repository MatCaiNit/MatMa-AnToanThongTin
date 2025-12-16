import math
import secrets
import time
import sys
import multiprocessing as mp
from collections import defaultdict
import os

# =====================================================
# Progress logger
# =====================================================

class ProgressLogger:
    def __init__(self, total, label="AKS"):
        self.total = total
        self.label = label
        self.start = time.time()
        self.last = 0

    def update(self, done):
        now = time.time()
        if now - self.last < 0.5 and done < self.total:
            return
        self.last = now

        percent = done * 100 // self.total
        elapsed = now - self.start
        eta = (elapsed / done * (self.total - done)) if done else 0

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

# =====================================================
# Number theory
# =====================================================

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def is_perfect_power(n):
    if n <= 1:
        return False
    max_b = int(math.log2(n)) + 1
    for b in range(2, max_b + 1):
        a = int(round(n ** (1.0 / b)))
        if a > 1 and pow(a, b) == n:
            return True
    return False

def factorize(n):
    fac = defaultdict(int)
    while n % 2 == 0:
        fac[2] += 1
        n //= 2
    f = 3
    while f * f <= n:
        while n % f == 0:
            fac[f] += 1
            n //= f
        f += 2
    if n > 1:
        fac[n] += 1
    return fac

def euler_phi(n):
    fac = factorize(n)
    res = n
    for p in fac:
        res = res // p * (p - 1)
    return res

def multiplicative_order(n, r):
    if gcd(n, r) != 1:
        return 0
    phi = euler_phi(r)
    for d in sorted(
        d for d in range(1, phi + 1) if phi % d == 0
    ):
        if pow(n % r, d, r) == 1:
            return d
    return phi

# =====================================================
# Polynomial arithmetic mod (x^r - 1, n)
# poly = list length r
# =====================================================

def poly_mul(a, b, n, r):
    out = [0] * r
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0:
                continue
            out[(i + j) % r] = (out[(i + j) % r] + ai * bj) % n
    return out

def poly_pow(base, exp, n, r):
    res = [0] * r
    res[0] = 1
    b = base[:]
    e = exp
    while e > 0:
        if e & 1:
            res = poly_mul(res, b, n, r)
        b = poly_mul(b, b, n, r)
        e >>= 1
    return res

# =====================================================
# GLOBAL for workers (giảm IPC)
# =====================================================

GLOBAL_XN = None
GLOBAL_N = None
GLOBAL_R = None

def init_worker(xn, n, r):
    global GLOBAL_XN, GLOBAL_N, GLOBAL_R
    GLOBAL_XN = xn
    GLOBAL_N = n
    GLOBAL_R = r

def aks_worker(a):
    n = GLOBAL_N
    r = GLOBAL_R
    x_n = GLOBAL_XN

    base = [0] * r
    base[0] = a % n
    base[1] = 1

    left = poly_pow(base, n, n, r)

    right = x_n[:]
    right[0] = (right[0] + a) % n

    return left == right

# =====================================================
# AKS main
# =====================================================

def aks_is_prime(n, parallel=True):
    if n < 2:
        return False

    if is_perfect_power(n):
        return False

    log2n = math.log2(n)
    bound = int(math.ceil(log2n * log2n))

    # Step 2: find r
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

    # Step 5
    phi_r = euler_phi(r)
    A = min(int(math.sqrt(phi_r) * math.log(n)), r - 1)

    x_n = [0] * r
    x_n[n % r] = 1

    print(f"[AKS] r = {r}, φ(r) = {phi_r}, A = {A}")
    print(f"[AKS] parallel = {parallel}, CPU = {os.cpu_count()}")

    progress = ProgressLogger(A, "AKS congruence")

    if not parallel:
        for a in range(1, A + 1):
            if not aks_worker(a):
                return False
            progress.update(a)
        progress.finish()
        return True

    # ---- PARALLEL BLOCKED EXECUTION ----
    ctx = mp.get_context("spawn")
    block = os.cpu_count()

    with ctx.Pool(
        processes=block,
        initializer=init_worker,
        initargs=(x_n, n, r)
    ) as pool:

        done = 0
        for start in range(1, A + 1, block):
            tasks = list(range(start, min(start + block, A + 1)))

            for ok in pool.imap_unordered(aks_worker, tasks, chunksize=1):
                done += 1
                progress.update(done)
                if not ok:
                    pool.terminate()
                    print("\n[AKS] Congruence failed")
                    return False

    progress.finish()
    return True

# =====================================================
# Prime generation (AKS – demo only)
# =====================================================

def random_128bit_odd():
    n = secrets.randbits(128)
    n |= (1 << 127)
    n |= 1
    return n

def generate_prime_aks():
    attempt = 0
    while True:
        attempt += 1
        n = random_128bit_odd()
        print(f"\n[Attempt {attempt}] Testing candidate")
        if aks_is_prime(n, parallel=True):
            print("Prime found")
            return n

# =====================================================
if __name__ == "__main__":
    mp.freeze_support()
    prime = generate_prime_aks()
    print("Prime:", prime)
