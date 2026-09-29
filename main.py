import sys
import os


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
                continue

            executable_path = search_executables(cmd)

            if executable_path:
                print(f"{cmd} is {executable_path}")
            else:
                print(f"{cmd}: not found")
        else:
            print(f"{command}: command not found")


# Searches for command in the PATH directories
# Returns True if it exists and has execute permissions else None
def search_executables(command: str) -> str | None:
    # Get the PATH env variable
    env_path = os.environ.get("PATH")

    path_directories = env_path.split(":")

    # Loops through each directory
    for directory_abs in path_directories:
        # Skips the directory if it doesn't exist
        if not os.path.isdir(directory_abs):
            continue

        # Loops through each item in the directory
        for executable in os.listdir(directory_abs):
            # Skips items that don't match the command
            if executable != command:
                continue
            
            file_path_abs = os.path.join(directory_abs, executable)
            # returns True if the file has execute (X) permissions
            has_execute_permission = os.access(file_path_abs, os.X_OK)

            # skips this item if it doesn't have execute permissions
            if not has_execute_permission:
                continue
            
            return file_path_abs

    return None


if __name__ == "__main__":
    main()
