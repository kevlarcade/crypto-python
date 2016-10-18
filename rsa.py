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

def encryptblock(key, block):
    e, n = key
    m = gmpy2.mpz(0)
    cblock = []

    for b in block:
        m *= 256
        m += b

    cm = pow(m, e, n)

    while cm != 0:
        b = cm % 256
        cm //= 256
        cblock.append(bytes(b))

    cblock.reverse()
    return b''.join(cblock)

def encrypt(key, msg):
    e, n = key
    e = gmpy2.mpz(e)
    n = gmpy2.mpz(n)
    blksize = n.bit_length() - 1
    blksize //= 8
    cmsg = b''
    for s in range(0, len(msg), blksize):
        cmsg += encryptblock(key, msg[s:s+blksize])
    return cmsg

def decrypt(key, msg):
    pass

def sign(key, msg):
    pass

def check(key, msg):
    pass
