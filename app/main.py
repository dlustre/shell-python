import sys


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        match command.split():
            case [command, *args]:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
