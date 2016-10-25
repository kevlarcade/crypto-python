#!/usr/bin/python

from rsa import *
import argparse
import sys

def readkey(fn):
    f = open(fn, 'r')
    e = int(f.readline())
    n = int(f.readline())
    f.close()
    return (e, n)

def main():
    parser = argparse.ArgumentParser(description='RSA utilities')
    parser.add_argument('action', help='genkeys, encrypt, decrypt, sign, check')
    parser.add_argument('--pub-key', dest='pubkey', default='public.key',
            help='public key with default name public.key')
    parser.add_argument('--priv-key', dest='privkey', default='private.key',
            help='private key with default name private.key')
    parser.add_argument('--size', dest='keylen', default='1024', type=int,
            help='size of the key with default value 1024')
    parser.add_argument('--input', dest='input', help='input file to\
            encrypt/decrypt/sign/check')
    parser.add_argument('--output', dest='output', help='output file')

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    args.action = args.action.lower()

    if args.action == 'genkeys':
        keylen = args.keylen
        pubkey, privkey = genKeys(keylen)
        f = open(args.pubkey, 'w')
        g = open(args.privkey, 'w')
        f.write(str(pubkey[0]) + '\n')
        f.write(str(pubkey[1]) + '\n')
        g.write(str(privkey[0]) + '\n')
        g.write(str(privkey[1]) + '\n')
        g.close()
        f.close()

    elif args.action == 'encrypt':
        key = readkey(args.pubkey)
        m = open(args.input, 'rb')
        msg = m.read()
        m.close()
        fileout = encrypt(key, msg)
        c = open(args.output, 'wb')
        c.write(fileout)
        c.close()

    elif args.action == 'decrypt':
        key = readkey(args.privkey)
        m = open(args.input, 'rb')
        msg = m.read()
        m.close()
        fileout = decrypt(key, msg)
        c = open(args.output, 'wb')
        c.write(fileout)
        c.close()

    elif args.action == 'sign':
        pass

    elif args.action == 'check':
        pass

if __name__ == "__main__":
    main()
