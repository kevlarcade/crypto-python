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
