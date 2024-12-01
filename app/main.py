import sys

builtins = ["echo", "exit", "type"]

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        match command.split():
            case ["type", arg]:
                print(f"{arg}{" is a shell builtin" if arg in builtins else ": not found"}")
            case ["echo", *args]:
                print(' '.join(args))
            case ["exit", "0"]:
                exit(0)
            case [command, *args]:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
