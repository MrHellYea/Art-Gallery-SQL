import sys
from variables import *


def main():
    while True:
        os.system("cls||clear")
        print(messages[0])
        option1 = input("Option: ")

        if option1 == "0":
            sys.exit(1)

        try:
            option1 = linker[option1]
        except KeyError:
            continue

        print(messages[1])
        option2 = input("Option: ")

        try:
            option1[option2]()
        except KeyError:
            pass


if __name__ == "__main__":
    main()
