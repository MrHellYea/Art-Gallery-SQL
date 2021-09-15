from typing import Callable, Optional
from generic_functions import *


def is_num(num: str) -> bool:
    try:
        float(num)
    except ValueError:
        return False
    return True

def is_not_empty(text: str) -> bool:
    if text == "":
        return False
    return True

def validate_input(text: str, function: Callable, allow_empty: Optional[bool]=False) -> str:
    while True:
        x = input(text)

        if (allow_empty and x == ""):
            return None
        if function(x):
            return x

def validate_cpf(cpf: str) -> bool:
    if len(cpf) != 11:
        return False

    remain = get_remain(cpf, 10, -2)

    if not str(remain) == cpf[-2]:
        return False

    remain = get_remain(cpf, 11, -1)

    if not str(remain) == cpf[-1]:
        return False

    return True

def validate_date(date: str) -> bool:
    try:
        day, month, year = [int(x) for x in date.split("/")]
    except ValueError:
        return False

    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
        month_lengths[1] = 29

    if 1 <= month <= 12 and 1 <= day <= month_lengths[month - 1]:
        return True
    return False

def validate_phone(phone: str) -> bool:
    if is_num(phone) and len(phone) == 9:
        return True
    return False

def validate_time(time: str) -> bool:
    try:
        hour, minute = [int(x) for x in time.split(":")]
    except ValueError:
        return False

    if 0 <= hour <= 23 and 0 <= minute <= 59:
        return True
    return False
