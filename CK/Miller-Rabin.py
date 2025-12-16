import secrets

def is_probable_prime(n: int, k: int = 40) -> bool:
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def random_128bit_odd() -> int:
    n = secrets.randbits(128)
    n |= (1 << 127) 
    n |= 1           
    return n

def generate_prime_128bit():
    while True:
        candidate = random_128bit_odd()
        if is_probable_prime(candidate):
            return candidate

if __name__ == "__main__":
    prime = generate_prime_128bit()
    print("128-bit prime:", prime)

# Thuật toán chạy nhanh, kiểm tra và tìm kiếm được số nguyên tố 128 bít qua 30-50 lần sinh ngẫu nhiên chỉ trong 2-3s