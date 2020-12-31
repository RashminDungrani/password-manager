""" Password Manager frequently used functions """

import json
import readline

PASSWORDS_FILE_LOCATION = "data.json"

def get_password_data():
    ''' Read data from password json file '''
    with open(PASSWORDS_FILE_LOCATION) as passwd_file:
        passwords_data = json.load(passwd_file)
    return passwords_data

def save_password_data(passwords_data):
    ''' Save Data to passwords.json file '''
    with open(PASSWORDS_FILE_LOCATION, 'w') as passwords_file:
        json.dump(passwords_data, passwords_file, indent=4, ensure_ascii=False)


def help_print():
    ''' printing all commands '''
    print("""
  _____________________________________________________
  |  keyword           | action                        |
  |  -----------------------------------------------   |
  |  1                 |   Timeline.py                 |
  |  2                 |   passwordmanager.py          |
  |  3                 |   wantstoknow.py              |
  |  0                 |   back to script              |
  |                                                    |
  |  view              | To view all Domain            |
  |  view {domain}     | To view Spacific Domain       |
  |  del  {domain->*}  | To detele domain              |
  |  del  {domain->id} | To delete id pass from domain |
  |  edit {domain->id} | To edit id and password       |
  |  copy {domain->id} | To copy pass into clipboard   |
  |  clear             | To clear screen               |
  |____________________________________________________|
  """)


def clean_n_lines(n_lines=1):
    '''overwrite terminal lines'''
    for _ in range(n_lines):
        print("\033[A"+ " "*92 +"\033[A")


def confirm_input(asked_str: str):
    '''Just confirm user_input with -> \\t[Are you sure ?] " + asked_str + " [y\\n]) : '''
    while True:
        user_input = input("\t[Are you sure ?] " + asked_str + " [y\\n]) : ").lower()
        if user_input not in ['y', 'n']:
            clean_n_lines(1)
        else:
            return user_input == 'y'


def pre_editable_input(prompt, prefill):
    ''' Edit with Pre string '''
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input("\t" + prompt + " : ")
    finally:
        readline.set_startup_hook()


def input_with_tab_complition(input_str: str, completor_list: list, input_must_in_list=False):
    '''Tab complition user input with list of string'''

    def tab_completor(text, state):
        options = [i for i in completor_list if i.startswith(text)]
        if state < len(options):
            return options[state]
        return None
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tab_completor)
    return_input = input(input_str)

    if input_must_in_list:
        while return_input not in completor_list:
            if return_input == '0':
                return False

            print('\tinput must be in tab completor_list')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(tab_completor)
            return_input = input(input_str)
    return return_input