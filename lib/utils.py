import re


def remove_command_string(text):
    return re.sub(r"\/\S+ ", "", text)
