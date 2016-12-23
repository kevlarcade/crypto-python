RSA
===
Security of RSA depends on the difficulty of factoring large integers.  
The file rsa.py is the library that implement:

Key generation:
---------------
* Size of the key (2048 by default)
* 2 random prime numbers p and q
* N a modulus number for private and public key as: N = p * q
* The [Euler's totient
function](https://en.wikipedia.org/wiki/Euler%27s_totient_function) φ(N) = (p
\- 1) * (q - 1)
* e, an integer coprime with φ(N) and between 1 and φ(N).
* d, the [modular multiplicative
inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) of
e[φ(N)].

Public Key | Private Key
---------- | -----------
(N, e)     | (d, N)

Encryption:
-----------
* m, the message send by Alice to Bob.
* (e, N), bob's public key.
* c, the cypher message.
```
c = m^e[N]
```

Decryption:
-----------
* m, the message send by Alice to Bob.
* (d, N), bob's private key.
* c, the cypher message.
```
c^d = m[N]
```

Sign:
-----
* m, the message.
* h, the hash of the message (hash function is sha256).
* s, the signature of the message (s is the encrypted hash).
* signed-message = m + s

Check:
------
Simply rehash the message and verify if it equals the decrypted signature
received.

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

Diffie-Hellman
==============
Alice choose a private number a, and a couple of number p (a prime number), and
g (a number lower than p).  
Then Alice generate A as:
```
A = g^a[p]
```
Then Alice send A, p, and g to Bob.  
Bob generate a private number b, and generate B as:
```
B = g^b[p]
```
Then B was send to Alice and the Diffie-Hellman is calculate as:
```
k = A^b[p] = B^a[p]
```

Client-Server Chat
==================

You have to run the server.py then the client.py.  
By default with no option, the server and the client will send to each other
their public key.  
Then a Diffie-Hellman key will be exchanged using the chat.  
Then all message send will be encrypt and decrypt.  

For a full demo, you have to:
1. Generate server and client keys
```
./crypto.py --pub-key cli.pub --priv-key cli.priv genkeys
./crypto.py --pub-key serv.pub --priv-key serv.priv genkeys
```
2. Start the server with server's keys and client's public key option
```
./server.py --pub-key serv.pub --priv-key serv.priv --cli-key cli.pub
```
3. Start the client with client's key and server's public key option
```
./client.py --pub-key cli.pub --priv-key cli.priv --serv-key serv.pub
```
4. Start chatting, it's a simple chat so you can't send a message before
receiving an answer.
5. You can use tcpdump or wireshark to see encrypted traffic.
6. You can send exit to quit the chat.
