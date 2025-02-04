"""
This module implements a cross-platform command-line interface (CLI) bot with
support for command autocompletion.

Modules:
- constants: Contains messages and other constant values.
- command_registry: Manages command execution.

Usage:
- Run the script and follow the prompts to execute commands.
"""
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from constants import Messages
from parser import parse_input
import command_registry as command_service


def main():
    print(Messages.Welcome)

    # Setup command executor and prompt session
    command_executor = command_service.create_command_executor()
    completer = WordCompleter(command_service.get_commands(), ignore_case=True)
    session = PromptSession(completer=completer)

    # Main command loop
    while True:
        user_input = session.prompt(Messages.EnterACommand)
        if not user_input:
            print(Messages.NoCommandEntered)
            continue
        command, *args = parse_input(user_input)
        if command == "exit" or command == "close":
            print(Messages.GoodBye)

            break
        # Execute the command and print the result
        result = command_executor(command, *args)
        print(result)


if __name__ == "__main__":
    main()
