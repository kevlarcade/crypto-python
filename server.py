#!/bin/python

import argparse
import time
from socket import *
from rsa import *
from diffieHellman import *

HOST = '127.1' #127.1 = 127.0.0.1
PORT = 4242

def readkey(fn): #Function that read key from the file
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
    parser.add_argument('--cli-key', dest='clikey', default='cliPub.key',
            help='public key with default name cliPub.key')
    parser.add_argument('--size', dest='keylen', default='2048', type=int,
            help='size of the key with default value 2048')

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
    e = int(conn.recv(4096).decode('utf-8')) #received e
    n = int(conn.recv(4096).decode('utf-8')) #received n

    try: #if client public key is defined in parameters
        cliPub = readkey(args.clikey)
    except FileNotFoundError:
        cliPub = e, n
    time.sleep(1)
    conn.send(str(servPub[0]).encode('utf-8')) #send e
    time.sleep(1)
    conn.send(str(servPub[1]).encode('utf-8')) #send n

    print('Key exchange for Diffie-Hellman')

    #Receiving A
    a = conn.recv(4096)
    a = decrypt(servPriv, a)
    h, a = check(cliPub, a)
    if (h != True):
        print('Warning the signature contain error')
    a = int(a.decode('utf-8'))

    #Receiving p
    p = conn.recv(4096)
    p = decrypt(servPriv, p)
    h, p = check(cliPub, p)
    if (h != True):
        print('Warning the signature contain error')
    p = int(p.decode('utf-8'))

    #Receiving g
    g = conn.recv(4096)
    g = decrypt(servPriv, g)
    h, g = check(cliPub, g)
    if (h != True):
        print('Warning the signature contain error')
    g = int(g.decode('utf-8'))

    #Generating the private number
    r = generatePrivate() #random private number
    #Generating B
    b = generatePart(p, g, n) #b = part to send to other member
    #Generating the key
    k = generateKey(a, n, p) #k = the diffie-hellman generated key
    print('k = ', k)
    #sending B
    b = sign(servPriv, str(b).encode('utf-8')) #sign B
    b = encrypt(cliPub, b) #encrypt B
    conn.send(b)

    #Start the chat
    while True:
        #Receiving client message
        data = conn.recv(4096)
        if (len(data) == 0):
            break
        data = decrypt(servPriv, data)
        h, m = check(cliPub, data)
        if (h != True):
            print('The message signature contain error!')
        print('Received: ', m.decode('utf-8'))
        #Sending a message to the client
        reply = input('Reply: ')
        if (reply == 'exit'):
            break
        reply = sign(servPriv, reply.encode('utf-8'))
        reply = encrypt(cliPub, reply)
        conn.sendall(reply)

    conn.close()

if __name__ == "__main__":
    main()
