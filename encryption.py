import sys


line = ""
passkey = ""


def encrypt(word):
    encrypted = []
    for i in range(0, len(word)):
        ascii_val = ord(word[i].lower()) + (ord(passkey[i % len(passkey)].lower()) - ord('a'))

        if ascii_val > 122:
            diff = ascii_val - 122
            ascii_val = diff + 96
        
        # Is the original letter in Upper case?
        if ord(word[i]) <= 90:
            encrypted.append(chr(ascii_val - 32))
        else:
            encrypted.append(chr(ascii_val))

    return "".join(encrypted)

def decrypt(word):
    decrypted = []
    for i in range(0, len(word)):
        ascii_val = ord(word[i].lower()) - (ord(passkey[i % len(passkey)].lower()) - ord('a'))

        if ascii_val < 97:
            diff = 97 - ascii_val
            ascii_val = 123 - diff
        
        # Is the original letter in Upper case?
        if ord(word[i]) <= 90:
            decrypted.append(chr(ascii_val - 32))
        else:
            decrypted.append(chr(ascii_val))

    return "".join(decrypted)

while True:
    line = sys.stdin.readline().rstrip()

    if line == "QUIT":
        sys.exit(0)

    cmd = line[:line.index(' ')]
    arg = line[line.index(' ') + 1:]

    if cmd == "PASSKEY":
        # set current passkey to arg
        passkey = arg
        # write success response to stdout
        sys.stdout.write("RESULT ")
    elif not passkey:
        sys.stdout.write("ERROR: A passkey must be set before encrypting/decrypting")
    elif cmd == "ENCRYPT":
        # encrypt the string
        enc_string = encrypt(arg)

        sys.stdout.write(f"RESULT {enc_string}")
    elif cmd == "DECRYPT":
        # decrypt the string
        dec_string = decrypt(arg)

        sys.stdout.write(f"RESULT {dec_string}")

    

