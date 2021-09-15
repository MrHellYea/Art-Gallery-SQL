import sqlite3
import os
from uuid import uuid4
from validation_functions import *

connection = sqlite3.connect("./database/gallery.db")
connection.execute("PRAGMA foreign_keys = 1")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

with open("./database/main.sql", "r") as f:
    with connection:
        cursor.executescript(f.read())

validation_linker = {
    "person": {
        "name": (is_not_empty, False),
        "cpf": (validate_cpf, False),
        "phone": (validate_phone, False),
        "birth": (validate_date, False),
    },
    "piece": {
        "title": (lambda x: True, True),
        "desc": (lambda x: True, True),
        "date": (validate_date, False),
        "person_cpf": (validate_cpf, True),
        "value": (is_num, False),
        "id": (is_not_empty, False)
    },
    "exposition": {
        "title": (is_not_empty, False),
        "date": (validate_date, False),
        "time": (validate_time, False),
        "id": (is_not_empty, False)
    },
    "creates": {
        "person_cpf": (validate_cpf, False),
        "piece_id": (is_not_empty, False)
    },
    "visits": {
        "person_cpf": (validate_cpf, False),
        "exposition_id": (is_not_empty, False),
        "enter": (validate_time, False),
        "leave": (validate_time, False)
    },
    "displays": {
        "piece_id": (is_not_empty, False),
        "exposition_id": (is_not_empty, False)
    }
}


def search(table:str, *texts: Optional[str]) -> None:
    keys = {}
    where = ""

    validation = validation_linker[table]
    for count, text in enumerate(texts):
        if count != 0:
            where += " AND "

        keys[f"search_{text}"] = validate_input(f"{text}: ", validation[text][0], validation[text][1])
        where += f"{text}=:search_{text}"

    user = cursor.execute(f"SELECT * FROM {table} WHERE {where}", keys).fetchone()
    if user is None:
        input("No row with such key. Press enter to continue.")
        return None

    return (user, where, keys)

def add_person() -> None:
    name = validate_input("Name: ", is_not_empty)
    cpf = validate_input("CPF: ", validate_cpf)
    phone = validate_input("Phone: ", validate_phone)
    birth = validate_input("Birth date (DD/MM/YYYY): ", validate_date)

    settings = {"cpf": cpf, "name": name, "phone": phone, "birth": padronize_date(birth)}
    with connection:
        try:
            cursor.execute("INSERT INTO person VALUES (:cpf, :name, :phone, :birth)", settings)
        except sqlite3.IntegrityError:
            input("Person with such CPF already exits. Press Enter to continue")

def add_piece() -> None:
    title = validate_input("Title (leave blank if none): ", lambda x: True, True)
    desc = validate_input("Description (leave blank if none): ", lambda x: True, True)
    date = validate_input("Creation date (DD/MM/YYYY): ", validate_date)
    person_cpf = validate_input("Buyer's CPF (leave blank if none): ", validate_cpf, True)
    value = validate_input("Value: ", is_num)
    id_ = str(uuid4())

    settings = {"id": id_, "value": value, "date": padronize_date(date), "person_cpf": person_cpf, "title": title, "desc": desc}
    with connection:
        try:
            cursor.execute("INSERT INTO piece VALUES (:id, :value, :date, :person_cpf, :title, :desc)", settings)
        except sqlite3.IntegrityError:
            input("No person with such CPF. Press Enter to continue.")

def add_exposition() -> None:
    title = validate_input("Title: ", is_not_empty)
    date = validate_input("Creation date (DD/MM/YYYY): ", validate_date)
    time = validate_input("Time (HH:MM): ", validate_time)
    id_ = str(uuid4())

    settings = {"id": id_, "title": title, "date": padronize_date(date), "time": padronize_time(time)}
    with connection:
        cursor.execute("INSERT INTO exposition VALUES (:id, :title, :date, :time)", settings)

def add_creates() -> None:
    person_cpf = validate_input("Author's CPF: ", validate_cpf)
    piece_id = validate_input("Piece's ID: ", is_not_empty)

    settings = {"person_cpf": person_cpf, "piece_id": piece_id}
    with connection:
        try:
            cursor.execute("INSERT INTO creates VALUES (:person_cpf, :piece_id)", settings)
        except sqlite3.IntegrityError:
            input("No person with such CPF, or piece with such ID. Press Enter to continue.")

def add_visits() -> None:
    person_cpf = validate_input("Visitor's CPF: ", validate_cpf)
    exposition_id = validate_input("Exposition's ID: ", is_not_empty)
    enter = padronize_time(validate_input("Enter time (HH:MM): ", validate_time))
    leave = padronize_time(validate_input("Leave time (HH:MM): ", validate_time))

    settings = {"person_cpf": person_cpf, "exposition_id": exposition_id, "enter": enter, "leave": leave}
    with connection:
        try:
            cursor.execute("INSERT INTO visits VALUES (:person_cpf, :exposition_id, :enter, :leave)", settings)
        except sqlite3.IntegrityError:
            input("No piece or exposition with such ID. Press Enter to continue.")

def add_displays() -> None:
    piece_id = validate_input("Piece's ID: ", is_not_empty)
    exposition_id = validate_input("Exposition's ID: ", is_not_empty)

    settings = {"piece_id": piece_id, "exposition_id": exposition_id}
    with connection:
        try:
            cursor.execute("INSERT INTO displays VALUES (:piece_id, :exposition_id)", settings)
        except sqlite3.IntegrityError:
            input("No piece or exposition with such ID. Press Enter to continue.")

def remove(table:str, *texts: Optional[str]) -> None:
    locate = search(table, *texts)

    if locate is None:
        return
    
    user, where, keys = locate
    option = validate_input(f"Delete the following row (y/n)\n{list(user)}\n", lambda x: x in ("y", "n"))
    if option == "n":
        return
    
    with connection:
        cursor.execute(f"DELETE FROM {table} WHERE {where}", keys)

def remove_person() -> None:
    remove("person", "cpf")

def remove_piece() -> None:
    remove("piece", "id")

def remove_exposition() -> None:
    remove("exposition", "id")

def remove_creates() -> None:
    remove("creates", "person_cpf", "piece_id")

def remove_visits() -> None:
    remove("visits", "person_cpf", "exposition_id")

def remove_displays() -> None:
    remove("displays", "piece_id", "exposition_id")

def edit(table:str, *texts: Optional[str]):
    locate = search(table, *texts)

    if locate is None:
        return
    
    row, where, keys = locate
    row = dict(row)

    while True:
        os.system("clear||cls")
        print("Insert '-1' to save and leave. Insert '-2' to discard.\n")

        print("Select which attribute to change")
        for key, value in row.items():
            print(f"{key} -> {value}")

        option = validate_input("Attribute: ", is_not_empty).lower().strip()

        if option in ("-1", "-2"):
            break

        if row.get(option) is None or option == "id":
            continue

        validation = validation_linker[table][option]
        row[option] = validate_input(f"New {option}: ", validation[0], validation[1])
        if option == "date":
            row[option] = padronize_date(row[option])
        elif option in ("time", "enter", "leave"):
            row[option] = padronize_time(row[option])

    set_text = ""
    for count, attribute in enumerate(row.keys()):
        if count != 0:
            set_text += ", "

        set_text += f"{attribute}=:{attribute}"

    if option == "-1":
        try:
            with connection:
                cursor.execute(f"UPDATE {table} SET {set_text} WHERE {where}", keys|row)
        except sqlite3.IntegrityError:
            input("Error finding one of the keys. Press Enter to continue.")

def edit_person() -> None:
    edit("person", "cpf")

def edit_piece() -> None:
    edit("piece", "id")

def edit_exposition() -> None:
    edit("exposition", "id")

def edit_creates() -> None:
    edit("creates", "person_cpf", "piece_id")

def edit_visits() -> None:
    edit("visits", "person_cpf", "exposition_id")

def edit_displays() -> None:
    edit("displays", "piece_id", "exposition_id")

def check(options: str, table: str) -> None:
    search = validate_input(f"Insert the value of one of the following: {options}: ", is_not_empty)

    count = 1
    cursor.execute(f"SELECT * FROM {table} WHERE :search IN ({options})", {"search": search})
    for person in cursor.fetchall():
        print(f"{count} -> {list(person)}")
        count += 1

    if count == 1:
        print("Nothing found.")
    input("Press Enter to continue.")

def check_person() -> None:
    check("cpf, name, birth, phone", "person")

def check_piece() -> None:
    check("id, value, date, person_cpf, title, desc", "piece")

def check_exposition() -> None:
    check("id, title, date, time", "exposition")

def check_creates() -> None:
    check("person_cpf, piece_id", "creates")

def check_visits() -> None:
    check("person_cpf, exposition_id, enter, leave", "visits")

def check_displays() -> None:
    check("piece_id, exposition_id", "displays")
