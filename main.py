import sys
import subprocess
import os

from constants import SHELL_BUILTINS


def main():
    # Indefinite loop to implement REPL
    while True:
        # Print prompt
        sys.stdout.write("$ ")

        # Wait for user input
        command = input().strip()

        # Exits out of the REPL loop
        if command == "exit":
            break
        # prints out the contents after the echo command
        elif command.startswith("echo"):
            # Grabs the content after the echo command (empty if theres nothing after)
            text = command[5:]

            # Removes '' or "" if it surrounds the text after the command
            if text.startswith('"') and text.endswith('"'):
                text = text.strip('"')
            elif text.startswith("'") and text.endswith("'"):
                text = text.strip("'")

            print(text)

        # Prints the type of command
        elif command.startswith("type"):
            commands = command.split()[1:]

            # Loops over the commands after type if there are multiple
            # Checks if it's built-in else it'll check if it's an executable
            for cmd in commands:
                if cmd in SHELL_BUILTINS:
                    print(f"{cmd} is a shell builtin")
                    continue

                executable_path = search_executables(cmd)

                if executable_path:
                    print(f"{cmd} is {executable_path}")
                else:
                    print(f"{cmd}: not found")

        # Runs the command if it exists with arguments (if there are any passed)
        # else prints command not found
        else:
            cmd = command.split()
            executable_path = search_executables(cmd[0])

            if executable_path:
                completed_process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                )

                print(completed_process.stdout, end="")
                continue

            print(f"{cmd[0] if isinstance(cmd, list) else cmd}: command not found")


# Searches for command in the PATH directories
# Returns absotlue path if it exists and has execute permissions else None
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
