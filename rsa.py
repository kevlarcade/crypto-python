import random
import gmpy2

def genKeys(size):
    keylen = size
    plen = random.randint(keylen // 2 - 20, keylen // 2 - 1)
    qlen = keylen - plen
    p = random.getrandbits(plen)
    q = random.getrandbits(qlen)
    p = gmpy2.next_prime(p)
    q = gmpy2.next_prime(q)
    e = 65537
    d = gmpy2.invert(e, (p - 1) * (q - 1))
    N = p * q
    pub = (e, N)
    priv = (d, N)
    return (pub, priv)

def encrypt(key, msg):
    pass

def decrypt(key, msg):
    pass

def sign(key, msg):
    pass

def check(key, msg):
    pass
