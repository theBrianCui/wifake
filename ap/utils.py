import sys
import subprocess

def print_stdout(completed_process):
    print(completed_process.stdout.decode("utf-8"), end="")

# Synchronously execute a shell command.
# Exits the script with error code 1 if the command exited with a nonzero code.
def exec_sync(command, before="", error="", after=""):
    if before != "": print(before, end="", flush=True)
    process = None
    try:
        process = subprocess.run(command, stdout=subprocess.PIPE, check=True)
    except:
        if error != "": print(error)
        sys.exit(1)

    if after != "": print(after)
    return process.stdout

