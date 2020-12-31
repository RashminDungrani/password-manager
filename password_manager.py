
""" Quicker and easy to use password manager python script """

import os
import sys
import datetime
from time import sleep
import readline
import pyperclip
from utils import *

class BColor:
    '''text background colors'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

passwords_data = get_password_data()


def add_another_id(domain_input):
    '''Add Id pass and other field to domain'''

    id_input = input(" "*14 + "id : ")
    if id_input == "0":
        pass

    elif id_input != "":
        # Check id is alreadt exist
        for id_number in range(len(passwords_data[domain_input])):
            if passwords_data[domain_input][id_number]["id"] == id_input:
                print(
                    f"\n\t{BColor.FAIL}✖{BColor.ENDC} This ID is already exist\n\tNOTE: You can edit this id using edit command")
                break
        else:   # if id not exist then append entry
            password_input = input(
                " "*12 + "pass : ")
            if password_input != "":
                if password_input == "0":
                    pass
                else:
                    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    domain_detail = {
                        "createdAt": current_time,
                        "id": id_input,
                        "pass": password_input
                    }
                    has_more_field = input(
                        "\n\tWant to add more fields (y) : ").lower()
                    print(
                        "\033[A" + " "*50 + "\033[A")

                    if has_more_field != "y":
                        passwords_data[domain_input].append(domain_detail)
                        save_password_data(passwords_data)
                    else:
                        while has_more_field == "y":
                            print(
                                "\033[A" + " "*50 + "\033[A")
                            field_name = input(
                                "field : ")

                            if field_name in ("", "0"):
                                has_more_field = ""
                            else:
                                # * ansi escape arrow up then overwrite the line
                                print(
                                    "\033[A" + " "*50 + "\033[A")
                                field_print = '{:>16} : '.format(
                                    field_name)
                                field_val = input(
                                    field_print)
                                if field_val in ("", "0"):
                                    has_more_field = ""
                                else:
                                    if field_val.lower() == "true":
                                        domain_detail[field_name] = True
                                    elif field_val.lower() == "false":
                                        domain_detail[field_name] = False
                                    else:
                                        domain_detail[field_name] = field_val
                                    has_more_field = input(
                                        "\n\tWant to add more fields (y) ? : ").lower()
                                    print(
                                        "\033[A" + " "*50 + "\033[A")

                        passwords_data[domain_input].append(domain_detail)
                        save_password_data(passwords_data)
            else:
                print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} Password cannot be empty")
    else:
        print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} Id cannot be empty")



def view_domain(domain):
    if domain in passwords_data:
        print("\033[A" + " "*50 + "\033[A")
        print("\n"+"-"*13 + f" [{domain}] " + "-"*13 + "\n")
        for id_number in range(len(passwords_data[domain])):
            # * .index(item Val) get item number from list
            items = passwords_data[domain][id_number].items()
            for key, value in items:
                if key == "createdAt":
                    pass
                else:
                    print('{:>16} : {:>}'.format(str(key), str(value)))
            print("\n")

    else:
        print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} No Records Found for {domain}")

    isclear = input("\nEnter to Continue [clear]: ").lower()
    print("\033[A" + " "*50 + "\033[A")
    if isclear == "clear":
        os.system("clear")
        print("\n"+"*"*25+"  Password Manager  "+"*"*24)


def view_all():
    for domain in passwords_data:
        print(f"[{BColor.UNDERLINE}" + domain + f"{BColor.ENDC}]")
        for id_number in range(len(passwords_data[domain])):
            # * .index(item Val) get item number from list
            items = passwords_data[domain][id_number].items()
            for key, value in items:
                if key == "createdAt":
                    pass
                else:
                    # * From StackOverFlow Python: Format output string, right alignment
                    print('{:>16} : {:>}'.format(str(key), str(value)))
            print("\n")
    input("\n\n\nEnter to Continue : ")
    os.system("clear")
    print("\n"+"*"*25+"  Password Manager  "+"*"*24)


def delete_opeation(domain, list_of_stored_domains):
    if domain in passwords_data:
        list_of_id = []

        delete_input = input_with_tab_complition("\n\tEnter id : ", list_of_stored_domains)
        if delete_input in ("0", "exit", False):
            print("\nExit")
        else:
            if delete_input == "*":
                passwords_data.pop(domain)
                list_of_stored_domains.remove(domain)
                save_password_data(passwords_data)
                print(f"\n\t{BColor.OKGREEN}✔{BColor.ENDC} Removed " + domain)
            elif delete_input in list_of_id:
                indexOfId = list_of_id.index(delete_input)
                del passwords_data[domain][indexOfId]
                save_password_data(passwords_data)
                get_password_data()
                print(f"\n\t{BColor.OKGREEN}✔{BColor.ENDC} " + delete_input + " Deleted")
            else:
                print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} id not exist")
    else:
        print(f"{BColor.FAIL}✖{BColor.ENDC} Domain not exist")




def edit_id_pass(domain):
    if domain in passwords_data:
        list_of_id = []

        def id_completor(text, state):
            options = [i for i in list_of_id if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None
        for ids in range(len(passwords_data[domain])):
            list_of_id.append(passwords_data[domain][ids]["id"])
        readline.parse_and_bind("tab: complete")
        readline.set_completer(id_completor)
        idInput = input("\n\tEnter id : ")
        if idInput in list_of_id:
            indexOfId = list_of_id.index(idInput)
            # * .index(item Val) get item number from list
            items = passwords_data[domain][indexOfId].items()
            itemsLen = len(items)
            loopCount = 0
            for key, value in items:
                loopCount += 1
                if key == "createdAt":
                    pass
                else:
                    editedValue = pre_editable_input(key, value)
                    if editedValue == "0":
                        print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} Exit")
                        break
                    # * update value of dict key value
                    passwords_data[domain][indexOfId][key] = editedValue

                    if loopCount == itemsLen:
                        has_more_field = input("\n\tWant to add more fields (y) : ").lower()
                        print("\033[A" + " "*50 + "\033[A")
                        # ask_add_id = "y"
                        while has_more_field == "y":
                            print("\033[A" + " "*50 + "\033[A")
                            field_name = input("field : ")

                            if field_name == "" or field_name == "0":
                                has_more_field = ""
                            else:
                                # * ansi escape arrow up then overwrite the line
                                print("\033[A" + " "*50 + "\033[A")
                                field_print = '{:>16} + '.format(
                                    field_name)
                                field_val = input(field_print)
                                if field_val == "" or field_name == "0":
                                    has_more_field = ""
                                else:
                                    if field_val.lower() == "true":
                                        passwords_data[domain][indexOfId][field_name] = True
                                    elif field_val.lower() == "false":
                                        passwords_data[domain][indexOfId][field_name] = False
                                    else:
                                        passwords_data[domain][indexOfId][field_name] = field_val
                                    has_more_field = input(
                                        "\n\tWant to add more fields (y) : ").lower()
                                    print("\033[A" + " "*50 + "\033[A")

                        save_password_data(passwords_data)
                        # get_password_data()
                        print(f"\n\t{BColor.OKGREEN}✔{BColor.ENDC} " + " Updated")

        else:
            print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} id not exist")
    else:
        print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} Domain not exist")


def copy_password(domain):
    if domain in passwords_data:
        list_of_id = []

        def id_completor(text, state):
            options = [i for i in list_of_id if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None
        for ids in range(len(passwords_data[domain])):
            list_of_id.append(passwords_data[domain][ids]["id"])
        readline.parse_and_bind("tab: complete")
        readline.set_completer(id_completor)
        idInput = input("\n\tEnter id : ")
        if idInput in list_of_id:
            indexOfId = list_of_id.index(idInput)
            pyperclip.copy(passwords_data[domain][indexOfId]["pass"])
            print(f"\n\t{BColor.OKGREEN}✔{BColor.ENDC} " +
                  " Password Copied to clipboard")
        else:
            print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} id not exist")
    else:
        print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} Domain not exist")


# Start
def password_manager():
    '''main function of the project'''

    keyword_list = ["view", "del", "edit", "copy"]
    os.system("clear")
    print(" Password Manager ".center(65, "*"))

    list_of_stored_domains = []
    for domain in passwords_data:
        list_of_stored_domains.append(domain)


    while True:
        domain_input = input_with_tab_complition("\n :> ", list_of_stored_domains).lower()

        len_of_input = len(domain_input.split())

        if len_of_input == 2:
            first_word = domain_input.split()[0]
            second_word = domain_input.split()[1]

        if domain_input == "":
            pass

        elif domain_input in ("view all", "view"):
            os.system("clear")
            print("\n"+"*"*25+"  Here Your All Accounts  "+"*"*24)
            view_all()

        elif domain_input == "clear":
            os.system("clear")
            print("\n"+"*"*25+"  Password Manager  "+"*"*24)

        elif len_of_input == 2 and first_word in keyword_list:
            if first_word == "view":
                view_domain(second_word)

            elif first_word == "del":
                delete_opeation(second_word, list_of_stored_domains)

            elif first_word == "edit":
                edit_id_pass(second_word)

            elif first_word == "copy":
                copy_password(second_word)

        elif domain_input in ("0", "exit"):
            print(" :<\n")
            sleep(0.25)
            sys.exit()

        elif domain_input == "help":
            help_print()
            input("\nPress Enter to Continue :")

        elif len_of_input > 1:
            print(
                f"\n\t{BColor.FAIL}✖{BColor.ENDC} Domain Name should not contain space ")

        else:
            if domain_input in passwords_data:
                print("\033[A" + " "*50 + "\033[A")
                print("\n" + "-"*13 + f" [{domain_input}] " + "-"*13)
                for id_number in range(len(passwords_data[domain_input])):
                    print("\n" + " "*14 + "id : " + passwords_data[domain_input][id_number]["id"])
                    print(" "*12 + "pass : " + passwords_data[domain_input][id_number]["pass"])

                id_input = input("\n" + " "*14 + "id + ")
                if id_input == "0":
                    pass

                elif id_input != "":
                    # Check id is alreadt exist
                    for id_number in range(len(passwords_data[domain_input])):
                        if passwords_data[domain_input][id_number]["id"] == id_input:
                            print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} This ID is already exist\n\tYou can edit this id using edit command")
                            break
                    else:   # if id not exist then append entry
                        password_input = input(" "*12 + "pass + ")
                        if password_input != "":
                            if password_input == "0":
                                pass
                            else:
                                current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                                domain_detail = {
                                    "createdAt": current_time,
                                    "id": id_input,
                                    "pass": password_input
                                }
                                passwords_data[domain_input].append(domain_detail)
                                has_more_field = input("\n\tWant to add more fields (y) : ").lower()
                                print("\033[A" + " "*50 + "\033[A")
                                ask_add_id = "y"
                                while ask_add_id == "y":
                                    if has_more_field != "y":
                                        ask_add_id = input("\tWant to add more id ? (y) : ").lower()
                                        print("\033[A" + " "*50 + "\033[A")
                                        if ask_add_id == "y":
                                            add_another_id(domain_input)
                                        else:
                                            save_password_data(passwords_data)
                                            print(f"\n\t{BColor.OKGREEN}✔{BColor.ENDC} Added")
                                    else:
                                        while has_more_field == "y":
                                            print("\033[A" + " "*50 + "\033[A")
                                            field_name = input("field : ")

                                            if field_name in ("", "0"):
                                                has_more_field = ""
                                            else:
                                                # * ansi escape arrow up then overwrite the line
                                                print("\033[A" + " "*50 + "\033[A")
                                                field_val = input('{:>16} + '.format(field_name))
                                                if field_val == "" or field_name == "0":
                                                    has_more_field = ""
                                                else:
                                                    if field_val.lower() == "true":
                                                        domain_detail[field_name] = True
                                                    elif field_val.lower() == "false":
                                                        domain_detail[field_name] = False
                                                    else:
                                                        domain_detail[field_name] = field_val
                                                    # domain_detail[field_name] = field_val
                                                    has_more_field = input(
                                                        "\n\tWant to add more fields (y) : ").lower()
                                                    print(
                                                        "\033[A" + " "*50 + "\033[A")

                                        ask_add_id = input("\tWant to add more id ? (y) : ").lower()
                                        print("\033[A" + " "*50 + "\033[A")
                                        if ask_add_id == "y":
                                            add_another_id(domain_input)
                                        else:
                                            save_password_data(passwords_data)
                                            print(f"\n\t{BColor.OKGREEN}✔{BColor.ENDC} Added")
                        else:
                            print(
                                f"\n\t{BColor.FAIL}✖{BColor.ENDC} Password cannot be empty")
                else:
                    print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} Id cannot be empty")
            else:
                print("\033[A" + " "*50 + "\033[A")
                print("\n" + "-"*13 + f" [{domain_input}] " + "-"*13)
                id_input = input("\n" + " "*14 + "id : ")
                if id_input != "":
                    if id_input == "0":
                        pass
                    else:
                        password_input = input(" "*12 + "pass : ")

                        if password_input != "":
                            if id_input == "0":
                                pass

                            else:
                                new_platform = {domain_input: []}
                                passwords_data.update(new_platform)

                                current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                                domain_detail = {
                                    "createdAt": current_time,
                                    "id": id_input,
                                    "pass": password_input
                                }
                                passwords_data[domain_input].append(domain_detail)
                                list_of_stored_domains.append(domain_input)
                                has_more_field = input(
                                    "\n\tWant to add more fields ? (y) : ").lower()
                                print("\033[A" + " "*50 + "\033[A")
                                ask_add_id = "y"
                                while ask_add_id == "y":
                                    if has_more_field != "y":
                                        ask_add_id = input("\tWant to add more id ? (y) : ").lower()
                                        print("\033[A" + " "*50 + "\033[A")
                                        if ask_add_id == "y":
                                            add_another_id(domain_input)
                                        else:
                                            save_password_data(passwords_data)
                                            print(f"\n\t{BColor.OKGREEN}✔{BColor.ENDC} Added " + domain_input)

                                    else:
                                        while has_more_field == "y":
                                            print("\033[A" + " "*50 + "\033[A")
                                            field_name = input("field = ")

                                            if field_name in ("", "0"):
                                                has_more_field = ""
                                            else:
                                                # * ansi escape arrow up then overwrite the line
                                                print("\033[A" + " "*50 + "\033[A")
                                                field_print = '{:>16} : '.format(
                                                    field_name)
                                                field_val = input(field_print)
                                                if field_val in ("", "0"):
                                                    has_more_field = ""
                                                else:
                                                    if field_val.lower() == "true":
                                                        domain_detail[field_name] = True
                                                    elif field_val.lower() == "false":
                                                        domain_detail[field_name] = False
                                                    else:
                                                        domain_detail[field_name] = field_val
                                                    # domain_detail[field_name] = field_val
                                                    has_more_field = input(
                                                        "\n\tWant to add more fields (y) : ").lower()
                                                    print(
                                                        "\033[A" + " "*50 + "\033[A")

                                        ask_add_id = input("\tWant to add more id ? (y) : ").lower()
                                        print("\033[A" + " "*50 + "\033[A")
                                        if ask_add_id == "y":
                                            add_another_id(domain_input)
                                        else:
                                            save_password_data(passwords_data)
                                            print(f"\n\t{BColor.OKGREEN}✔{BColor.ENDC} " + domain_input + " Domain Added ")
                        else:
                            print(
                                f"\n\t{BColor.FAIL}✖{BColor.ENDC} Password cannot be empty")
                else:
                    print(f"\n\t{BColor.FAIL}✖{BColor.ENDC} Id cannot be empty")

if __name__ == "__main__":
    password_manager()
    