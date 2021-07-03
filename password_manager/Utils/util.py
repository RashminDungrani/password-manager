""" Password Manager frequently used functions """

import os
import json
from password_manager.Utils.locations import Paths
import readline

def check_data_path_available() -> bool:
    if not os.path.exists(Paths.config_path):
        with open(Paths.config_path, 'w') as config_file:
            json.dump({"passwords_file_path": ""}, config_file, indent=4, ensure_ascii=False) 

    with open(Paths.config_path) as config_file:
        config_file = json.load(config_file)

    passwords_file_path = config_file['passwords_file_path']
    
    if os.path.exists(passwords_file_path) and passwords_file_path.endswith('.json'):
        Paths.passwords_file_path = passwords_file_path
        return True

    elif passwords_file_path == "":
        while True:
            user_data_path = input("\n\tWhere you want to store data file or pick a file : ")
            if (user_data_path == ""):
                print("creating data files into project directory")
                passwords_file_path = Paths.passwords_file_path
                
                with open(passwords_file_path, "w") as outfile:
                    outfile.write("{}")
                # Save passwords.json file path to config file
                with open(Paths.config_path, 'w') as config_file:
                    config_file['passwords_file_path'] =  passwords_file_path
                    json.dump(config_file, config_file, indent=4, ensure_ascii=False) 
                
                return True
                
            elif os.path.exists(user_data_path) or os.path.exists(user_data_path[1:-1]) or os.path.exists(user_data_path[1:-2]):
                if os.path.exists(user_data_path[1:-1]):
                    user_data_path = user_data_path[1:-1]
                elif os.path.exists(user_data_path[1:-2]):
                    user_data_path = user_data_path[1:-2]
                if (os.path.isfile and user_data_path.endswith('.json')):
                    # Save passwords.json file path to config file
                    Paths.passwords_file_path = user_data_path
                    with open(Paths.config_path, 'w') as config_file:
                        json.dump({"passwords_file_path": user_data_path}, config_file, indent=4, ensure_ascii=False) 
                    return True
                elif os.path.isfile:
                    print("passwords file must be type of json")
                elif os.path.isdir:
                    # make json file passwords.json
                    passwords_file_path = os.path.join(user_data_path, "passwords.json")
                    with open(passwords_file_path, "w") as outfile:
                        outfile.write({})
                    # Save passwords.json file path to config file
                    with open(Paths.config_path, 'w') as config_file:
                        json.dump({"passwords_file_path": passwords_file_path}, config_file, indent=4, ensure_ascii=False) 
                    
                    Paths.passwords_file_path = passwords_file_path
                    
                    return True
                else:
                    print("\n\tInvalid path...\n")
            else:
                print("\n\tPath not exist\n")
                    
    
    else:
        print(passwords_file_path + " is not valid path so clearning in config path")
        return False
    

def get_password_data():
    ''' Read data from password json file '''
    with open(Paths.passwords_file_path) as passwd_file:
        return json.load(passwd_file)

def save_password_data(passwords_data):
    ''' Save Data to passwords.json file '''
    with open(Paths.passwords_file_path, 'w') as passwords_file:
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