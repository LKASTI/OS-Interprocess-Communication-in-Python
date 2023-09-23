import sys
from subprocess import Popen, PIPE

logfile = sys.argv[1]
if not logfile:
    print("error")
    sys.exit(1)

logger = Popen(['python', 'logger.py', logfile], stdin = PIPE, stdout = PIPE, encoding='utf8')

menu_text = "|------------------------Menu------------------------|\n    password - sets the password key for encrypting/decrypting\n    encrypt - encrypts a given string\n    decrypt - decrypts a given string\n     history - shows history of encrypted/decrypted strings\n quit - ends the program\n\n|----------------------------------------------------|"

line = ""
current_pass = ""

while line != "quit":
    sys.stdout.write(menu_text)
    sys.stdout.write("Enter a command and argument: ")

    line = sys.stdin.readline().rstrip()
    cmd = line[:line.index(' ')]
    arg = line[line.index(' ') + 1:]

    sys.stdout.write("\n")

    if cmd == "password":
        logger.stdin.write(f"SET_PASSWORD {arg}")
    elif cmd == "encrypt":
        # TODO: password must be set first
        logger.stdin.write(f"ENCRYPT {arg}")
        # TODO: save encrypted word in history if not already there
    elif cmd == "decrypt":
        logger.stdin.write(f"ENCRYPT {arg}")
    elif cmd == "history":
    elif cmd == "quit":
    else:
        sys.stdout.write("Please enter one of the listed commands.")


    
