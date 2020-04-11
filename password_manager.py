# Python3

import json
import os
import sys
import datetime
from datetime import date, timedelta
from time import sleep
import readline
from pyautogui import typewrite

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

passwords_file_location = "data.json"

def loadJsonFile():
  with open(passwords_file_location) as f:
    json_data = json.load(f)

with open(passwords_file_location) as f:
  json_data = json.load(f)

def help():
  print("""
   __________________________________________________
  |  keyword    |   action                            |
  |  --------------------------                       |
  |  view              To view all Domain             |
  |  view {domain}     To view Spacific Domain        |
  |  del  {domain->*}  To detele domain               |
  |  del  {domain->id} To delete id pass from domain  |
  |  edit {domain->id} To edit id and password        |
  |___________________________________________________|
  """)

def view_domain(domain):
  domain = domain.lower()
  os.system("clear")
  print("\n"+"*"*12 + " " + domain + " " + "*"*11 + "\n")
  if domain in json_data:
    for id_number in range(len(json_data[domain])):
      items = json_data[domain][id_number].items() # * .index(item Val) get item number from list
      for key, value in items:
        if key == "createdAt":
          pass
        else:
          print('{:>16} : {:>}'.format(key, value))
      print("\n")
      
  else:
    print(f"\n\tNo Records Found for {domain}\n")
  isclear = input("\n\n\nEnter to Continue [clear]: ").lower()
  if isclear == "clear":
    os.system("clear")
    print("\n"+"*"*25+"  Password Manager  "+"*"*24)


def view_all():
  # print All Json data with Format
  for domain in json_data:
    
    print(f"[{bcolors.UNDERLINE}" + domain +f"{bcolors.ENDC}]")
    for id_number in range(len(json_data[domain])):
      items = json_data[domain][id_number].items() # * .index(item Val) get item number from list
      for key, value in items:
        if key == "createdAt":
          pass
        else:
          print('{:>16} : {:>}'.format(key, value))  # * From StackOverFlow Python: Format output string, right alignment
      print("\n")
  input("\n\n\nEnter to Continue : ")
  os.system("clear")
  print("\n"+"*"*25+"  Password Manager  "+"*"*24)


def delete_opeation(domain):
  if domain in json_data:
    list_of_id = []
    def id_completor(text, state):
      options = [i for i in list_of_id if i.startswith(text)]
      if state < len(options):
        return options[state]
      else:
        return None
    for ids in range(len(json_data[domain])):
      list_of_id.append(json_data[domain][ids]["id"])
    readline.parse_and_bind("tab: complete")
    readline.set_completer(id_completor)
    delete_input = input("\n\tEnter id : ")
    if delete_input == "0" or delete_input == "":
      print("\nExit")
      pass
    else:
      if delete_input == "*":
        json_data.pop(domain)
        list_of_stored_domains.remove(domain)
        with open(passwords_file_location,'w') as f:
          json.dump(json_data,f)
        print(f"\n\t{bcolors.OKGREEN}✔{bcolors.ENDC} Removed " + domain)
      elif delete_input in list_of_id:
        indexOfId = list_of_id.index(delete_input)
        del json_data[domain][indexOfId]
        with open(passwords_file_location,'w') as f:
          json.dump(json_data,f)
        loadJsonFile()
        print(f"\n\t{bcolors.OKGREEN}✔{bcolors.ENDC} " + delete_input +" Deleted")
      else:
        print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} id not exist")
  else:
    print(f"{bcolors.FAIL}✖{bcolors.ENDC} Domain not exist")


def rlinput(prompt, prefill):
  readline.set_startup_hook(lambda: readline.insert_text(prefill))
  try:
    return input("\t" + prompt + " : ")
  finally:
    readline.set_startup_hook()

def edit_id_pass(domain):
  if domain in json_data:
    list_of_id = []
    def id_completor(text, state):
      options = [i for i in list_of_id if i.startswith(text)]
      if state < len(options):
        return options[state]
      else:
        return None
    for ids in range(len(json_data[domain])):
      list_of_id.append(json_data[domain][ids]["id"])
    readline.parse_and_bind("tab: complete")
    readline.set_completer(id_completor)
    idInput = input("\n\tEner id : ")
    if idInput in list_of_id:
      indexOfId = list_of_id.index(idInput)
      items = json_data[domain][indexOfId].items() # * .index(item Val) get item number from list
      itemsLen = len(items)
      loopCount = 0
      for key, value in items:
        loopCount +=1
        if key == "createdAt":
          pass
        else:
          editedValue = rlinput(key, value)
          if editedValue == "0":
            print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} Exit")
            break
          else:
            # * update value of dict key value
            json_data[domain][indexOfId][key] = editedValue

            if loopCount == itemsLen:
              with open(passwords_file_location,'w') as f:
                json.dump(json_data,f)
              loadJsonFile()
              print(f"\n\t{bcolors.OKGREEN}✔{bcolors.ENDC} " + " Updated")

    else:
      print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} id not exist")
  else:
    print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} Domain not exist")


# Start
# loadJsonFile()

list_of_stored_domains = []
for domain in json_data:
  list_of_stored_domains.append(domain)

# * tab completion from list of words
def domain_completer(text, state):
  options = [i for i in list_of_stored_domains if i.startswith(text)]
  if state < len(options):
    return options[state]
  else:
    return None

keyword_list = ["view","del","edit"]
os.system("clear")
print("\n"+"*"*25+"  Password Manager  "+"*"*24)


while 1:
  readline.parse_and_bind("tab: complete")
  readline.set_completer(domain_completer)
  domain_input = input(f"\n :> ")
  len_of_input = len(domain_input.split())
  if len_of_input == 2:
    first_word = domain_input.split()[0].lower()
    second_word = domain_input.split()[1]

  if domain_input == "":
    pass

  elif domain_input == "view all" or domain_input == "view":
    os.system("clear")
    print("\n"+"*"*25+"  Here Your All Accounts  "+"*"*24)
    view_all()

  elif domain_input.lower() == "clear":
    os.system("clear")
    print("\n"+"*"*25+"  Password Manager  "+"*"*24)

  elif len_of_input == 2 and first_word in keyword_list:
    if first_word == "view":
      view_domain(second_word)

    elif first_word == "del":
      delete_opeation(second_word)

    elif first_word == "edit":
      edit_id_pass(second_word)

  elif domain_input == "0" or domain_input == "exit":
    print(" :<\n")
    sleep(0.25)
    sys.exit()

  elif domain_input == "help":
    help()
    input("\nPress Enter to Continue :")

  elif len_of_input > 1:
    print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} Domain Name should not contain space ")

  else:
    if domain_input in json_data:
      print("\033[A"+ " "*40 +"\033[A")
      print("\n"+" "*5+"Domain Name : " + domain_input)
      if domain_input in json_data:
        for id_number in range(len(json_data[domain_input])):
          print("\n" + " "*14 + "id : " + json_data[domain_input][id_number]["id"])
          print(" "*12 + "pass : " + json_data[domain_input][id_number]["pass"])

      id_input = input("\n" +" "*14 + "id + ")
      if id_input == "0":
        pass

      elif id_input != "":
        for id_number in range(len(json_data[domain_input])):   # Check id is alreadt exist
          if json_data[domain_input][id_number]["id"] == id_input:
            print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} This ID is already exist\n\tYou can edit this id using edit command")
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
                "pass":password_input
              }
              isMoreFields = input("\n\tWant to add more fields (y) : ").lower()
              print("\033[A"+ " "*40 +"\033[A")

              if isMoreFields != "y":
                json_data[domain_input].append(domain_detail)
                with open(passwords_file_location,'w') as f:
                  json.dump(json_data,f)
                print(f"\n\t{bcolors.OKGREEN}✔{bcolors.ENDC} " + " Added")
              else:
                while isMoreFields == "y":
                  print("\033[A"+ " "*40 +"\033[A")
                  field_name = input("field : ")

                  if field_name == "" or field_name == "0":
                    isMoreFields = ""
                  else:
                    print("\033[A"+ " "*40 +"\033[A") # * ansi escape arrow up then overwrite the line
                    field_print = '{:>16} + '.format(field_name)
                    field_val = input(field_print)
                    if field_val == "" or field_name == "0":
                      isMoreFields = ""
                    else:
                      domain_detail[field_name] = field_val
                      isMoreFields = input("\n\tWant to add more fields (y) : ").lower()
                      print("\033[A"+ " "*40 +"\033[A")

                json_data[domain_input].append(domain_detail)
                with open(passwords_file_location,'w') as f:
                  json.dump(json_data,f)
                print(f"\n\t{bcolors.OKGREEN}✔{bcolors.ENDC} " + " Added")

          else:
            print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} Password cannot be empty")
      else:
          print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} Id cannot be empty")
    else:
      print("\033[A"+ " "*40 +"\033[A")
      print("\n"+" "*5+"Domain Name : " + domain_input)
      id_input = input("\n" +" "*14 + "id : ")
      if id_input != "":
        if id_input == "0":
          pass

        else:
          password_input = input(" "*12 + "pass : ")

          if password_input != "":
            if id_input == "0":
              pass

            else:

              new_platform = {
                domain_input:[]
              }

              current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

              domain_detail = {
                "createdAt": current_time,
                "id": id_input,
                "pass":password_input
              }
              json_data.update(new_platform)
              list_of_stored_domains.append(domain_input)
              isMoreFields = input("\n\tWant to add more fields (y) : ").lower()
              print("\033[A"+ " "*40 +"\033[A")
              if isMoreFields != "y":
                json_data[domain_input].append(domain_detail)
                with open(passwords_file_location,'w') as f:
                  json.dump(json_data,f)
                print(f"\n\t{bcolors.OKGREEN}✔{bcolors.ENDC} Added " + domain_input)

              else:
                while isMoreFields == "y":
                  print("\033[A"+ " "*40 +"\033[A")
                  field_name = input("field = ")

                  if field_name == "" or field_name == "0":
                    isMoreFields = ""
                  else:
                    print("\033[A"+ " "*40 +"\033[A") # * ansi escape arrow up then overwrite the line
                    field_print = '{:>16} : '.format(field_name)
                    field_val = input(field_print)
                    if field_val == "" or field_name == "0":
                      isMoreFields = ""
                    else:
                      domain_detail[field_name] = field_val
                      isMoreFields = input("\n\tWant to add more fields (y) : ").lower()
                      print("\033[A"+ " "*40 +"\033[A")


                json_data[domain_input].append(domain_detail)
                with open(passwords_file_location,'w') as f:
                  json.dump(json_data,f)
                print(f"\n\t{bcolors.OKGREEN}✔{bcolors.ENDC} " + domain_input + " Domain Added ")

          else:
            print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} Password cannot be empty")
      else:
        print(f"\n\t{bcolors.FAIL}✖{bcolors.ENDC} Id cannot be empty")