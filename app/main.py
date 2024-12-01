import sys
import os
import subprocess

builtins = ["echo", "exit", "type"]

def matching_dirs(dirs, exe):
    return [dir for dir in dirs if os.path.exists(os.path.join(dir, exe))]

def dir_contains_exec(dir, exe):
    return os.path.exists(os.path.join(dir, exe))

def main():
    dirs = os.environ["PATH"].split(":")

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        match command.split():
            case ["type", arg]:
                msg = ": not found"
                
                for d in dirs:
                    if dir_contains_exec(d, arg):
                        msg = " is " + os.path.join(d, arg)
                        break

                if arg in builtins:
                    msg = " is a shell builtin"
                print(f"{arg}{msg}")
            case ["echo", *args]:
                print(' '.join(args))
            case ["exit", "0"]:
                exit(0)
            case [cmd, *args]:
                match matching_dirs(dirs, cmd):
                    case []:
                        print(f"{cmd}: command not found")
                    case [first, *_]:
                        subprocess.run([os.path.join(first, cmd), *args])

if __name__ == "__main__":
    main()
