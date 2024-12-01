import sys
import os
import subprocess

builtins = ["echo", "exit", "type", "pwd", "cd"]

def consume(s, char):
    if s[0] != char:
        raise f"Expect '{char}' between args"
    
    return s[1:]

def literal(args_str):
    return args_str[0], args_str[1:]

# Intended for parsing backslashes.
def unary(args_str):
    if args_str[0] != '\\':
        return literal(args_str)

    return unary(args_str[1:])
    
def unquoted(args_str):
    arg = ''
    rest = args_str
    
    while rest and rest[0] != " ":
        literal, rest = unary(rest)
        arg += literal

    return arg, rest.lstrip()

def quoted(args_str):
    if args_str[0] not in ['"', "'"]:
        return unquoted(args_str)

    quote_kind = args_str[0]
    arg = ''
    rest = args_str[1:]
    
    while rest[0] != quote_kind:
        arg += rest[0]
        rest = rest[1:]

    rest = consume(rest, quote_kind)

    return arg, rest.lstrip()

def parse_args(args_str):
    parsed = []

    while args_str:
        parsed_arg, args_str = quoted(args_str)
        parsed.append(parsed_arg)

    return parsed


def matching_dirs(dirs, exe):
    return [dir for dir in dirs if os.path.exists(os.path.join(dir, exe))]

def dir_contains_exec(dir, exe):
    return os.path.exists(os.path.join(dir, exe))

def main():
    dirs = os.environ["PATH"].split(":")

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        user_in = input()

        command = user_in.split(' ', 1)

        args = parse_args(command[1]) if len(command) > 1 else []

        match [command[0], *args]:
            case ["cd", "~"]:
                os.chdir(os.environ["HOME"])
            case ["cd", path]:
                if not os.path.exists(path):
                    print(f"cd: {path}: No such file or directory")
                else:
                    os.chdir(path)
            case ["pwd"]:
                print(os.getcwd())
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
