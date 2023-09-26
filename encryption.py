import sys

line = ""
curr_pass = ""

while True:
    line = sys.stdin.readline().rstrip()

    if line == "QUIT":
        sys.exit(0)

    cmd = line[:line.index(' ')]
    arg = line[line.index(' ') + 1:]

    if cmd == "PASSKEY":
        # set current passkey to arg
        curr_pass = arg
    elif cmd == "ENCRYPT":
        pass
    elif cmd == "DECRYPT":
        pass

