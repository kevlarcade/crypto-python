import random
import gmpy2
import binascii
import struct

def genKeys(keylen):
    while True:
        plen = random.randint(keylen // 2 - 20, keylen // 2 - 1)
        qlen = keylen - plen
        p = random.getrandbits(plen)
        q = random.getrandbits(qlen)

        # Make sure p*q will be the right length
        p |= 1 << (plen - 1)
        q |= 1 << (qlen - 1)

        p = gmpy2.next_prime(p)
        q = gmpy2.next_prime(q)
        e = 65537
        phi = (p - 1) * (q - 1)

        # If e is not coprime with phi, decryption is not unique
        if gmpy2.gcd(e, phi) != 1:
            continue

        d = gmpy2.invert(e, phi)
        N = p * q

        if N.bit_length() == keylen:
            break

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
    blksize = n.bit_length() - 1
    blksize //= 8
    cmsg = b''

    for s in range(0, len(msg), blksize):
        cblock = encryptblock(key, msg[s:s+blksize])
        l = struct.pack('<H', len(cblock))
        cmsg += l + cblock

    return cmsg

def decrypt(key, cmsg):
    e, n = key
    msg = b''
    blockstart = 0

    while blockstart < len(cmsg):
        (l,) = struct.unpack('<H', cmsg[blockstart:blockstart+2])
        blockstart += 2
        msg += encryptblock(key, cmsg[blockstart:blockstart+l])
        blockstart += l

    return msg

def sign(key, msg):
    pass

def check(key, msg):
    pass
