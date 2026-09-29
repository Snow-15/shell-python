import sys


def main():
    # Indefinite loop to implement REPL
    while True:
        # Print prompt
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        # Exits out of the REPL loop
        if command == "exit":
            break
        # prints out the contents after the echo command
        elif command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            _, cmd = command.split(maxsplit=1)
            if cmd in {"exit", "echo", "type"}:
                print(f"{cmd} is a shell builtin")
            else:
                print(f"{cmd}: not found")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
