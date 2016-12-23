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
    parser = argparse.ArgumentParser(description='Secure Chat Client')
    parser.add_argument('--pub-key', dest='pubkey', default='cliPub.key',
            help='public key with default name cliPub.key')
    parser.add_argument('--priv-key', dest='privkey', default='cliPriv.key',
            help='private key with default name cliPriv.key')
    parser.add_argument('--serv-key', dest='servkey', default='servPub.key',
            help='public key with default name servPub.key')
    parser.add_argument('--size', dest='keylen', default='2048', type=int,
            help='size of the key with default value 2048')

    args = parser.parse_args()

    try: #if key are defined in parameters
        cliPub = readkey(args.pubkey)
        cliPriv = readkey(args.pubkey)
    except FileNotFoundError: #else generating a new set of key
        print('No key found. Generating…')
        cliPub, cliPriv = genKeys(args.keylen)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))

    time.sleep(1)
    s.send(str(cliPub[0]).encode('utf-8')) #send e
    time.sleep(1)
    s.send(str(cliPub[1]).encode('utf-8')) #send n
    print('Awaiting key')
    e = int(s.recv(4096).decode('utf-8')) #received e
    n = int(s.recv(4096).decode('utf-8')) #received n
    try: #if server public key is defined in parameters
        servPub = readkey(args.servkey)
    except FileNotFoundError:
        servPub = e, n
    print('Received the server key')

    print('Key exchange for Diffie-Hellman')
    p, g = generateCommon() #p = primal number, g < p
    n = generatePrivate() #n = random private number
    a = generatePart(p, g, n) #a = part to send to other member
    a = sign(cliPriv, str(a).encode('utf-8')) #sign A
    a = encrypt(servPub, a) #encrypt A
    s.send(a) #send a
    time.sleep(1)
    p1 = p
    p1 = sign(cliPriv, str(p1).encode('utf-8')) #sign p
    p1 = encrypt(servPub, p1) #encrypt p
    s.send(p1) #send p
    time.sleep(1)
    g = sign(cliPriv, str(g).encode('utf-8')) #sign g
    g = encrypt(servPub, g) #encrypt g
    s.send(g) #send g
    #received B
    b = s.recv(4096)
    b = decrypt(cliPriv, b)
    h, b = check(servPub,b)
    if (h != True):
        print('Warning the signature contain error')
    b = int(b.decode('utf-8'))
    k = generateKey(b, n, p) #k = the diffie-hellman generated key
    print('k = ', k)

    while True:
        message = input('Your message: ')
        if (message == 'exit'):
            break
        message = sign(cliPriv, message.encode('utf-8')) #sign the message
        message = encrypt(servPub, message) #encrypt the message
        s.send(message)
        print('Awaiting reply')
        reply = s.recv(4096)
        if (len(reply) == 0):
            break
        reply = decrypt(cliPriv, reply)
        h, m = check(servPub, reply)
        if (h != True):
            print('The message signature contain error!')
        print('Received ', m.decode('utf-8'))

    s.close()

if __name__ == "__main__":
    main()
