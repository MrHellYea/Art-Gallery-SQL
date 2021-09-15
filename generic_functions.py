def get_remain(cpf: str, start: int, upto: int) -> int:
    total = 0

    for count, num in enumerate(cpf[:upto]):
        try:
            total += int(num) * (start - count)
        except ValueError:
            return None

    remain = (total * 10) % 11
    remain = remain if remain != 10 else 0

    return remain

def padronize_date(date: str) -> str:
    day, month, year = map(lambda x: x.lstrip("0"), date.split("/"))

    day = day if len(day) == 2 else f"0{day}"
    month = month if len(month) == 2 else f"0{month}"
    year = year if len(year) == 4 else f"{'0'*(4-len(year))}{year}"

    return f"{day}/{month}/{year}"

def padronize_time(time: str) -> str:
    hour, minute = map(lambda x: x.lstrip("0"), time.split(":"))

    hour = hour if len(hour) == 2 else f"0{hour}"
    minute = minute if len(minute) == 2 else f"0{minute}"

    return f"{hour}:{minute}"
