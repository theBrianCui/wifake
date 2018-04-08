import sys
import subprocess

def print_stdout(completed_process):
    print(completed_process.stdout.decode("utf-8"), end="")

# Synchronously execute a shell command.
# Exits the script with error code 1 if the command exited with a nonzero code.
def exec_sync(command, before="", error="", after="",
              silent=True, err_silent=False, die=True):

    process = None
    stdout = None
    stderr = None

    if silent == True: stdout = subprocess.PIPE
    if err_silent == True: stderr = subprocess.PIPE
    if before != "": print(before, end="", flush=True)
    
    try:
        process = subprocess.run(command,
                                 stdout=stdout, stderr=stderr,
                                 check=True)
    except Exception as e:
        if die:
            raise RuntimeError(error)
        else:
            print(error)

    if after != "": print(after)
    if process != None: return process.stdout
    return ""
