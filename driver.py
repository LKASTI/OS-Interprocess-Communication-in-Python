import sys,re
from subprocess import Popen, PIPE
from collections import deque

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
history = deque(["(Go Back)"])

def display_history():
    print("------------------------------------------------History------------------------------------------------\n\n")
    # Print all options in history
    for i,word in enumerate(history):
        print(f"{i+1}. {word}\n")

    print("-------------------------------------------------------------------------------------------------------\n")
    
def use_history():
    print("Would you like to use the history? (Y/N) ")
    ans = sys.stdin.readline().rstrip()

    if ans.lower() == "y":
        display_history()

        num = -1
        while 0 > num or num >= len(history):
            print("Choose a word: ")
            num = sys.stdin.readline().rstrip()
            if int(num) < 0 or int(num) >= len(history):
                print("Please enter the number representing the word from the listed strings.\n")            
        return history[int(num) - 1] 

while True:
    sys.stdout.write(menu_text)
    sys.stdout.write("\nEnter a command: ")

    # Waiting for user to write to terminal
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
            display_history()
            logger.stdin.write("HISTORY SUCCESS\n")
        else:
            logger.stdin.write(f"UNKNOWN_CMD {line}\n")
            sys.stdout.write("Please enter one of the listed commands.\n")    
    else:
        cmd = line[:line.index(' ')]
        arg = line[line.index(' ') + 1:]

        if cmd == "password":
            # TODO: provide user option of using a string in history or entering a new string

            # Log password action 
            logger.stdin.write(f"SET_PASSWORD {arg}\n")
            logger.stdin.flush()

            # Check if argument is a latin letter a-z, A-Z
            if bool(re.match(r'^[a-zA-z]+$', arg)):
                # Store password in history
                if arg not in history:
                    history.appendleft(arg)
                # Send password to encrypter and read response
                encrypter.stdin.write(f"PASSKEY {arg}\n")
                encrypter.stdin.flush()
                enc_response = encrypter.stdout.readline().rstrip()

                # Print response and log response
                print(enc_response)
                logger.stdin.write("SET_PASSWORD SUCCESS\n")
            else:
                # Log failed response and print to stdout
                logger.stdin.write("SET_PASSWORD ERROR: password must contain letters only\n")
                print("ERROR: password must contain letters only")
        elif cmd == "encrypt" or cmd =="decrypt":
            # TODO: Provide user option of using a string in history or entering a new string

            # TODO: Save the string that will be encrypted into history 
            if arg not in history:
                history.appendleft(arg)

            if cmd == "encrypt":
                # Log the action
                logger.stdin.write(f"ENCRYPT {arg}\n")
                logger.stdin.flush()


                # Send string to encrypter and read response
                encrypter.stdin.write(f"ENCRYPT {arg}\n")
                encrypter.stdin.flush()
                enc_response = encrypter.stdout.readline().rstrip()

                # Log the response, and print the response to stdout
                if "ERROR" in enc_response:
                    logger.stdin.write(f"ENCRYPT {enc_response}\n")
                else:
                    logger.stdin.write(f"ENCRYPT SUCCESS: {enc_response[enc_response.index(' ') + 1:]}\n")
                print(enc_response)
            else:
                # Log the action
                logger.stdin.write(f"DECRYPT {arg}\n")
                logger.stdin.flush()

                # Send string to decrypter and read response
                encrypter.stdin.write(f"DECRYPT {arg}\n")
                encrypter.stdin.flush()
                enc_response = encrypter.stdout.readline().rstrip()

                # Log the response and print to stdout
                if "ERROR" in enc_response:
                    logger.stdin.write(f"DECRYPT {enc_response}\n")
                else:
                    logger.stdin.write(f"DECRYPT SUCCESS: {enc_response[enc_response.index(' ') + 1:]}\n")
                print(enc_response)
        else:
            # Log unknown command
            logger.stdin.write(f"UNKNOWN_CMD_{cmd.upper()} UNKNOWN_ARG_{arg}\n")
            sys.stdout.write("Please enter one of the listed commands.\n")    

    logger.stdin.flush()

    # Press enter to continue
    print("Press enter to continue...")
    sys.stdin.readline()
    
    sys.stdout.write("\n")



    
