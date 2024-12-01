import sys
import os
import subprocess

builtins = ["echo", "exit", "type"]

def matching_dirs(dirs, exe):
    return [os.path.exists(os.path.join(dir, exe)) for dir in dirs]

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
            case [command, *args]:
                match matching_dirs(dirs, command):
                    case []:
                        print(f"{command}: command not found")
                    case [first, *_]:
                        subprocess.run([command] + args, capture_output=True)

if __name__ == "__main__":
    main()
