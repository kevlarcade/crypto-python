#!/bin/python

import argparse
import time
from socket import *
from rsa import *
from diffieHellman import *

HOST = '127.1'
PORT = 4242

def readkey(fn):
    f = open(fn, 'r')
    e = int(f.readline())
    n = int(f.readline())
    f.close()
    return (e, n)

def main():
    parser = argparse.ArgumentParser(description='Secure Chat Server')
    parser.add_argument('--pub-key', dest='pubkey', default='servPub.key',
            help='public key with default name servPub.key')
    parser.add_argument('--priv-key', dest='privkey', default='servPriv.key',
            help='private key with default name servPriv.key')
    parser.add_argument('--size', dest='keylen', default='1024', type=int,
            help='size of the key with default value 1024')

    args = parser.parse_args()

    try:
        servPub = readkey(args.pubkey)
        servPriv = readkey(args.pubkey)
    except FileNotFoundError:
        print('No key found. Generating…')
        servPub, servPriv = genKeys(args.keylen)

    print('Awaiting for connection…')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print('Connected by ')
    print(addr)
    e = int(conn.recv(4096).decode('utf-8'))
    n = int(conn.recv(4096).decode('utf-8'))
    cliPub = e, n
    print('Received the client public key')
    time.sleep(1)
    conn.send(str(servPub[0]).encode('utf-8'))
    time.sleep(1)
    conn.send(str(servPub[1]).encode('utf-8'))

    print('Key exchange for Diffie-Hellman')
    a = int(conn.recv(4096).decode('utf-8'))
    p = int(conn.recv(4096).decode('utf-8'))
    g = int(conn.recv(4096).decode('utf-8'))
    r = generatePrivate()
    b = generatePart(p, g, n)
    k = generateKey(a, n, p)
    print('k = ', k)
    conn.send(str(b).encode('utf-8'))

    while True:
        data = conn.recv(4096)
        if (len(data) == 0):
            break
        data = decrypt(servPriv, data)
        print('Received: ', data.decode('utf-8'))
        reply = input('Reply: ')
        if (reply == 'exit'):
            break
        reply = reply.encode('utf-8')
        reply = encrypt(cliPub, reply)
        conn.sendall(reply)

    conn.close()

if __name__ == "__main__":
    main()
