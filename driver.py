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
        if i == len(history)-1:
            continue
        print(f"{i+1}. {word}\n")

    print("-------------------------------------------------------------------------------------------------------")
    
def use_history():
    sys.stdout.write("Would you like to use the history? (Y/N) ")
    sys.stdout.flush()
    ans = sys.stdin.readline().rstrip()

    if ans.lower() == "y":
        display_history()
        print(f"{len(history)}. (Go Back)")
        print("-------------------------------------------------------------------------------------------------------")

        num = -1
        while 0 > num or num >= len(history):
            sys.stdout.write("Choose a word: ")
            sys.stdout.flush()
            num = int(sys.stdin.readline().rstrip())
            if num == len(history):
                # -2 means to go back and prompt for user to enter new string
                return -2  
            if num <= 0 or num > len(history):
                print("Please enter the number representing the word from the listed strings.\n")     
        return history[num - 1] 
    # -1 means they won't use history so continue asking for input
    return -1

while True:
    sys.stdout.write(menu_text)
    sys.stdout.write("\nEnter a command: ")

    # Waiting for user to write to terminal
    cmd = sys.stdin.readline().rstrip()


    if cmd == "quit":
        logger.stdin.write("STOPPED Logging Stopped\n")
        encrypter.stdin.write("QUIT\n")
        logger.stdin.flush()
        encrypter.stdin.flush()
        logger.wait()
        encrypter.wait()
        sys.exit(0)
    elif cmd == "history":
        # Display history
        display_history()
        logger.stdin.write("HISTORY SUCCESS\n")  
    else:
        arg = ""
        # Provide user option of using a string in history or entering a new string
        if cmd == "password" or cmd == "encrypt" or cmd == "decrypt":
            if len(history) > 1:
                temp = use_history()
                if type(temp) == str:
                    arg = temp
                # Log user went back in history
                elif temp == -2:
                    logger.stdin.write(f"ATTEMPTED_USE_HISTORY {cmd}\n")
                    logger.stdin.flush()
                    logger.stdin.write(f"GO_BACK SUCCESS\n")
                    logger.stdin.flush()
                # When temp == -1 then continue as normal

        if cmd == "password":
            # Ask user to enter an argument if arg is empty            
            if arg == "":
                sys.stdout.write("Enter a password: ")
                sys.stdout.flush()
                arg = sys.stdin.readline().rstrip()
                sys.stdout.write("\n")
                sys.stdout.flush()

            # Log password action 
            logger.stdin.write(f"SET_PASSWORD {arg}\n")
            logger.stdin.flush()

            # Check if argument is a latin letter a-z, A-Z
            if bool(re.match(r'^[a-zA-z]+$', arg)):
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
                sys.stdout.write("ERROR: password must contain letters only")
                sys.stdout.flush()
        elif cmd == "encrypt" or cmd =="decrypt":
            # Ask user to enter an argument if arg is empty            
            if arg == "":
                sys.stdout.write("Enter a word to encrypt/decrypt: ")
                sys.stdout.flush()
                arg = sys.stdin.readline().rstrip()
                sys.stdout.write("\n")

            # Save the string that will be encrypted into history 
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
                    result = enc_response[enc_response.index(' ') + 1:]
                    logger.stdin.write(f"ENCRYPT SUCCESS: {result}\n")
                    # Store result in history
                    if result not in history:
                        history.appendleft(result)
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
                    result = enc_response[enc_response.index(' ') + 1:]
                    logger.stdin.write(f"DECRYPT SUCCESS: {result}\n")
                    # Store result in history
                    if result not in history:
                        history.appendleft(result)
                print(enc_response)
        else:
            # Log unknown command
            logger.stdin.write(f"UNKNOWN_CMD {cmd}\n")
            sys.stdout.write("Please enter one of the listed commands.\n")    

    logger.stdin.flush()

    # Press enter to continue
    sys.stdout.write("Press enter to continue...")
    sys.stdout.flush()
    sys.stdin.readline()
    
    sys.stdout.write("\n")



    
