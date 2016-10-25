import random
import gmpy2
import binascii

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

    # Convert the data block into an integer
    m = int(binascii.hexlify(block).decode('ascii'), 16)

    cm = pow(m, e, n)

    # Convert the new integer back to a data block
    cblock = hex(cm)[2:].rstrip('L')
    if len(cblock) % 2 == 1:
        cblock = '0' + cblock
    cblock = binascii.unhexlify(cblock.encode('ascii'))

    return cblock

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
