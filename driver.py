import sys
from subprocess import Popen, PIPE

logfile = sys.argv[1]
if not logfile:
    print("error")
    sys.exit(1)

logger = Popen(['python', 'logger.py', logfile], stdin = PIPE, stdout = PIPE, encoding='utf8')
encrypter = Popen(['python', 'encryption.py'], stdin = PIPE, stdout = PIPE, encoding='utf8')


menu_text = "------------------------------------------------Menu------------------------------------------------\n\n    password - sets the password key for encrypting/decrypting\n    encrypt - encrypts a given string\n    decrypt - decrypts a given string\n    history - shows history of encrypted/decrypted strings\n    quit - ends the program\n\n----------------------------------------------------------------------------------------------------"

password_error = "You must enter a password before encrypting/decrypting."
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
            logger.stdin.write("STOPPED Logging Stopped\n")
            encrypter.stdin.write("QUIT\n")
            logger.stdin.flush()
            encrypter.stdin.flush()
            logger.wait()
            encrypter.wait()
            sys.exit(0)
        elif line == "history":
            # TODO: display history
            logger.stdin.write("HISTORY SUCCESS\n")
        else:
            sys.stdout.write("Please enter one of the listed commands.")    
    else:
        cmd = line[:line.index(' ')]
        arg = line[line.index(' ') + 1:]

        if cmd == "password":
            # TODO: provide user option of using a string in history or entering a new string

            # set current password to argument
            current_pass = arg

            logger.stdin.write(f"SET_PASSWORD {arg}\n")
            logger.stdin.flush()

            encrypter.stdin.write(f"PASSKEY {arg}\n")
            encrypter.stdin.flush()
            enc_response = encrypter.stdout.readline().rstrip()

            print(enc_response)

            logger.stdin.write("SET_PASSWORD SUCCESS\n")
        elif cmd == "encrypt":
            # TODO: provide user option of using a string in history or entering a new string

            logger.stdin.write(f"ENCRYPT {arg}\n")
            logger.stdin.flush()
            # TODO: save the string that will be encrypted into history 

            encrypter.stdin.write(f"ENCRYPT {arg}\n")
            encrypter.stdin.flush()

            enc_response = encrypter.stdout.readline().rstrip()

            if "ERROR" in enc_response:
                logger.stdin.write(f"ENCRYPT {enc_response}\n")
                print(enc_response)
            else:
                logger.stdin.write(f"ENCRYPT SUCCESS: {enc_response[enc_response.index(' ') + 1:]}\n")
                print(enc_response)

        elif cmd == "decrypt":
            # TODO: provide user option of using a string in history or entering a new string

            logger.stdin.write(f"DECRYPT {arg}\n")
            logger.stdin.flush()
            # TODO: save the string that will be encrypted into history

            encrypter.stdin.write(f"DECRYPT {arg}\n")
            encrypter.stdin.flush()

            enc_response = encrypter.stdout.readline().rstrip()

            if "ERROR" in enc_response:
                logger.stdin.write(f"DECRYPT {enc_response}\n")
                print(enc_response)
            else:
                logger.stdin.write(f"DECRYPT SUCCESS: {enc_response[enc_response.index(' ') + 1:]}\n")
                print(enc_response)
        else:
            sys.stdout.write("Please enter one of the listed commands.")    

    sys.stdout.write("\n")
    logger.stdin.flush()
    



    
