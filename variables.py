from sql_functions import *

messages = (
    """
0 -> Save and close
1 -> Add
2 -> Remove
3 -> Edit
4 -> Check
    """,
    """
0 -> Go back
1 -> Person
2 -> Piece
3 -> Exposition
4 -> Create relation (person - piece)
5 -> Visit relation (person - exposition)
6 -> Display relation (exposition - piece)
    """
)

linker = {
    "1": {
        "1": add_person,
        "2": add_piece,
        "3": add_exposition,
        "4": add_creates,
        "5": add_visits,
        "6": add_displays
    },

    "2": {
        "1": remove_person,
        "2": remove_piece,
        "3": remove_exposition,
        "4": remove_creates,
        "5": remove_visits,
        "6": remove_displays
    },

    "3": {
        "1": edit_person,
        "2": edit_piece,
        "3": edit_exposition,
        "4": edit_creates,
        "5": edit_visits,
        "6": edit_displays
    },

    "4": {
        "1": check_person,
        "2": check_piece,
        "3": check_exposition,
        "4": check_creates,
        "5": check_visits,
        "6": check_displays
    }
}
