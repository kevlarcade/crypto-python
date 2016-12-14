import random
import gmpy2

def generatePrivate():
    return random.randint(1, 65535)

def generateCommon():
    p = random.randint(1, 65536)
    p = gmpy2.next_prime(p)
    g = random.randint(1, p)
    return (p, g)

def generatePart(p, g, n):
    return pow(g, n, p)

def generateKey(o, n, p):
    return pow(o, n, p)
