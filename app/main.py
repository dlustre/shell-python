import sys
import os
import subprocess

builtins = ["echo", "exit", "type", "pwd", "cd"]

def consume(s, char):
    if s[0] != char:
        raise f"Expect '{char}' between args"
    
    return s[1:]

def literal(s):
    return s[0], s[1:]

def unquoted_backslash(s):
    if s[0] != '\\':
        return literal(s)

    return unquoted_backslash(s[1:])
    
def unquoted(s):
    arg = ''
    rest = s
    
    while rest and rest[0] != " ":
        literal, rest = unquoted_backslash(rest)
        arg += literal

    return arg, rest.lstrip()

# Double-quote backslash
def escape(s):
    if s[0] != '\\':
        return literal(s)

    match s[0], s[1]:
        case '\\', '"':
            return '"', s[2:]
        case '\\', '\\':
            return '\\', s[2:]

    return s[0], s[1:]

def quoted(s):
    if s[0] not in ['"', "'"]:
        return unquoted(s)

    quote_kind = s[0]
    arg = ''
    rest = s[1:]
    
    while rest[0] != quote_kind:
        token, rest = escape(rest) if quote_kind == '"' else literal(rest)
        arg += token

    rest = consume(rest, quote_kind)

    if not rest or rest[0].isspace():
        return arg, rest.lstrip()

    # Addresses edge-case where an arg can be a mix of quoted and unquoted
    attached, rest = quoted(rest)
    return arg + attached, rest.lstrip()

def parse_args(s):
    parsed = []

    while s:
        parsed_arg, s = quoted(s)
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

        match parse_args(user_in):
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
