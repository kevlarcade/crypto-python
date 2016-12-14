#!/bin/python

import argparse
import time
from socket import *
from rsa import *
from diffieHellman import *

HOST = '127.1' # 127.1 = 127.0.0.1
PORT = 4242

def readkey(fn):
    f = open(fn, 'r')
    e = int(f.readline())
    n = int(f.readline())
    f.close()
    return (e, n)

def main():
    parser = argparse.ArgumentParser(description='Secure Chat Client')
    parser.add_argument('--pub-key', dest='pubkey', default='cliPub.key',
            help='public key with default name cliPub.key')
    parser.add_argument('--priv-key', dest='privkey', default='cliPriv.key',
            help='private key with default name cliPriv.key')
    parser.add_argument('--size', dest='keylen', default='1024', type=int,
            help='size of the key with default value 1024')

    args = parser.parse_args()

    try:
        cliPub = readkey(args.pubkey)
        cliPriv = readkey(args.pubkey)
    except FileNotFoundError:
        print('No key found. Generating…')
        cliPub, cliPriv = genKeys(args.keylen)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))

    time.sleep(1)
    s.send(str(cliPub[0]).encode('utf-8'))
    time.sleep(1)
    s.send(str(cliPub[1]).encode('utf-8'))
    print('Awaiting key')
    e = int(s.recv(4096).decode('utf-8'))
    n = int(s.recv(4096).decode('utf-8'))
    servPub = e, n
    print('Received the server key')

    print('Key exchange for Diffie-Hellman')
    p, g = generateCommon()
    n = generatePrivate()
    a = generatePart(p, g, n)
    s.send(str(a).encode('utf-8'))
    time.sleep(1)
    s.send(str(p).encode('utf-8'))
    time.sleep(1)
    s.send(str(g).encode('utf-8'))
    b = int(s.recv(4096).decode('utf-8'))
    k = generateKey(b, n, p)
    print('k = ', k)

    while True:
        message = input('Your message: ')
        if (message == 'exit'):
            break
        message = message.encode('utf-8')
        message = encrypt(servPub, message)
        s.send(message)
        print('Awaiting reply')
        reply = s.recv(4096)
        if (len(reply) == 0):
            break
        reply = decrypt(cliPriv, reply)
        print('Received ', reply.decode('utf-8'))

    s.close()

if __name__ == "__main__":
    main()
