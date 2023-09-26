import sys
import asyncio
from subprocess import Popen, PIPE

logfile = sys.argv[1]
if not logfile:
    print("error")
    sys.exit(1)

async def main():
    logger = await asyncio.subprocess.create_subprocess_exec(
            "python", "logger.py", logfile, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, encoding="utf-8"
    )


    menu_text = "------------------------------------------------Menu------------------------------------------------\n\n    password - sets the password key for encrypting/decrypting\n    encrypt - encrypts a given string\n    decrypt - decrypts a given string\n    history - shows history of encrypted/decrypted strings\n    quit - ends the program\n\n----------------------------------------------------------------------------------------------------"

    line = ""
    current_pass = ""

    while True:
        sys.stdout.write(menu_text)
        sys.stdout.write("\nEnter a command: ")

        # waiting for user to write to terminal
        line = sys.stdin.readline().rstrip()
        sys.stdout.write("\n")

        if line.find(' ') == -1:
            if line == "quit":
                logger.stdin.write("QUIT")
                sys.exit(0)
            elif line == "history":
                logger.stdin.write("HISTORY SUCCESS")
            else:
                sys.stdout.write("Please enter one of the listed commands.")    
        else:
            cmd = line[:line.index(' ')]
            arg = line[line.index(' ') + 1:]

            if cmd == "password":
                # set current password to argument
                logger.stdin.write(f"SET_PASSWORD {arg}")
            elif cmd == "encrypt":
                # TODO: password must be set first
                logger.stdin.write(f"ENCRYPT {arg}")
                # TODO: save the string that will be encrypted into history
            elif cmd == "decrypt":
                logger.stdin.write(f"DECRYPT {arg}")
                # TODO: save the string that will be decrypted into history
            else:
                sys.stdout.write("Please enter one of the listed commands.")    

        sys.stdout.write("\n")
        sys.stdin.flush()
        logger.stdin.flush()

asyncio.run(main())


    
