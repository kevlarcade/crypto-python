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
        f = open(args.input, 'rb')
        msg = f.read()
        f.close()

        cmsg = encrypt(key, msg)

        f = open(args.output, 'wb')
        f.write(cmsg)
        f.close()

    elif args.action == 'decrypt':
        key = readkey(args.privkey)
        f = open(args.input, 'rb')
        cmsg = f.read()
        f.close()

        msg = decrypt(key, cmsg)

        f = open(args.output, 'wb')
        f.write(msg)
        f.close()

    elif args.action == 'sign':
        key = readkey(args.privkey)
        f = open(args.input, 'rb')
        msg = f.read()
        f.close()

        smsg = sign(key, msg)

        f = open(args.output, 'wb')
        f.write(smsg)
        f.close()

    elif args.action == 'check':
        key = readkey(args.pubkey)
        f = open(args.input, 'rb')
        msg = f.read()
        f.close()

        c = check(key, msg)

        if c:
            print("Your signature is valid")
        else:
            print("Your signature is invalid")

if __name__ == "__main__":
    main()
