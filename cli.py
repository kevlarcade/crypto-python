#!/usr/bin/python

from rsa import *
import argparse

def main():
    parser = argparse.ArgumentParser(description='RSA utilities')
    parser.add_argument('action')
    parser.add_argument('--pub-key', dest='pubkey', default='public.key')
    parser.add_argument('--priv-key', dest='privkey', default='private.key')

    args = parser.parse_args()

    args.action = args.action.lower()

    if args.action == 'genkeys':
        pubkey, privkey = genKeys()
        f = open(args.pubkey, 'w')
        g = open(args.privkey, 'w')
        f.write(str(pubkey[0]) + '\n')
        f.write(str(pubkey[1]) + '\n')
        g.write(str(privkey[0]) + '\n')
        g.write(str(privkey[1]) + '\n')
        g.close()
        f.close()

    elif args.action =='encrypt':
        pass

    elif args.action =='decrypt':
        pass

    elif args.action =='sign':
        pass

    elif args.action =='check':
        pass


if __name__ == "__main__":
    main()
