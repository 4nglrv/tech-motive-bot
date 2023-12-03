import re
from typing import Dict, List

from pydantic_core import ErrorDetails

from pydantic import ValidationError


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Bregexp:
    PHONE = '^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$'


def err_print(msg: str):
    print(f"{Bcolors.WARNING}{msg}{Bcolors.ENDC}")


def is_phone(phone: str):
    match = re.match(Bregexp.PHONE, phone)
    return True if match else False


def convert_errors(
    e: ValidationError, custom_messages: Dict[str, str]
) -> List[ErrorDetails]:
    new_errors: List[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error['type'])
        if custom_message:
            ctx = error.get('ctx')
            error['msg'] = (
                custom_message.format(**ctx) if ctx else custom_message
            )
        new_errors.append(error)
    return new_errors