from validation import Validation

_validator = Validation()


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def detect_parameters(user_input):
    cmd, *args = parse_input(user_input)
