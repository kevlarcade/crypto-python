Crypto tools
============
The binary crypto.py uses the rsa.py library.

```
usage: crypto.py [-h] [--pub-key PUBKEY] [--priv-key PRIVKEY] [--size KEYLEN]
                 [--input INPUT] [--output OUTPUT]
                 action

RSA utilities

positional arguments:
  action              genkeys, encrypt, decrypt, sign, check

optional arguments:
  -h, --help          show this help message and exit
  --pub-key PUBKEY    public key with default name public.key
  --priv-key PRIVKEY  private key with default name private.key
  --size KEYLEN       size of the key with default value 2048
  --input INPUT       input file to encrypt/decrypt/sign/check
  --output OUTPUT     output file
```

Example:
```
./crypto --pub-key alice.pub --priv-key alice.priv --size 1024 genkeys
./crypto --input clear.txt --output cypher.txt
```

RSA
===
Security of RSA depends on the difficulty of factoring large integers.  
The file rsa.py is the library that implement:

Key generation:
---------------
* Size of the key (2048 by default)
* 2 random prime numbers p and q
* N a modulus number for private and public key as: N = p * q
* The [Euler's totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function) φ(N) = (p - 1) * (q - 1)
* e, an integer coprime with φ(N) and between 1 and φ(N).
* d, the [modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) of e[φ(N)].
