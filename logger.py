import sys
from datetime import datetime

file_name = sys.argv[1].rstrip()

log_file = open(f"{file_name}", "a")

# Function formats the datetime, action, and message
def format_action_message(action, message):
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M')} [{action}] {message}.\n"

# write the START action
log_file.write(format_action_message("START", "Logging Started"))


while True:
    line = sys.stdin.readline().rstrip()
    
    if line == "QUIT":
        log_file.write(format_action_message("STOPPED", "Logging Stopped"))
        log_file.close()
        sys.exit(0)
    
    action = line[:line.index(' ')]
    message = line[line.index(' ') + 1:]

    log_file.write(format_action_message(action, message))

