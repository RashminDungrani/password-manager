# Python3

import json
import os
import sys
import datetime
from datetime import date, timedelta
from time import sleep


with open('passwords.json') as f:
  json_data = json.load(f)

def view_platform(platform_name):
  platform_name = platform_name.capitalize()
  os.system("clear")
  print("\n"+"*"*25 + " " + platform_name + " " + "*"*24)

  # Printing All id password from specific platform
  if platform_name in json_data:
    for id_number in range(len(json_data[platform_name])):
      print("\t  id : " + json_data[platform_name][id_number]["id"])
      print("\tpass : " + json_data[platform_name][id_number]["password"])
      print("\n")
  else:
    print(f"\n\tNo Records Found for {platform_name}\n")
  
  input("\n\n\nEnter to Continue :> ")
  

def view_all():
  
  # print All Json data with Format
  for platform_name in json_data:
    print("[" + platform_name +"]")
    for id_number in range(len(json_data[platform_name])):
      print("\t  id : " + json_data[platform_name][id_number]["id"])
      print("\tpass : " + json_data[platform_name][id_number]["password"])
      print("\n")

  input("\n\n\nEnter to Continue :> ")




# Start
keyword_list = ["View","Del","Edit"]

while 1:
  os.system("clear")
  print("\n"+"*"*25+"  Password Manager  "+"*"*24)

  platform_input = input("\nEnter platform :> ")
  platform_input = platform_input.capitalize()

  len_of_input = len(platform_input.split())
  if len_of_input == 2:
    first_word = platform_input.split()[0]
    second_word = platform_input.split()[1]

  if platform_input == "":
    print("\n\tinvalid input")
    input("\n\nPress Enter to Continue :> ")

  elif platform_input in keyword_list or len_of_input == 2 and first_word == "View":
    if platform_input == "View all":
      os.system("clear")
      print("\n"+"*"*25+"  Here Your All Accounts  "+"*"*24)
      view_all()

    elif first_word == "View":
      view_platform(second_word)

    elif platform_input == "Del":
      pass
    elif platform_input == "Edit":
      pass

  elif platform_input == "0":
    print(":<")
    sleep(0.4)
    sys.exit()

  else:

    if platform_input in json_data:
      id_input = input("\nid :> + ")

      if id_input != "":
        for id_number in range(len(json_data[platform_input])):   # Check id is alreadt exist
          if json_data[platform_input][id_number]["id"] == id_input:
            print("\n\tthis ID is already exist\n\tYou can edit this id using edit command")
            input("\n\nPress Enter to Continue :> ") 
            break
        else:   # if id not exist then append entry
          password_input = input("\npassword :> ")
          if password_input != "":
            current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            platform_detail = {
              "created_date": current_time,
              "id": id_input,
              "password":password_input
            }

            json_data[platform_input].append(platform_detail)
            with open('passwords.json','w') as f:
              json.dump(json_data,f)

          else:
            print("\n\tPassword can not be empty")
            input("\n\nPress Enter to Continue :> ")

            

      else:
          print("\n\tId can not be empty")
          input("\n\nPress Enter to Continue :> ")

    else:
      id_input = input("\nid :> ")
      if id_input != "":
        password_input = input("\npassword :> ")
        if password_input != "":
          current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
          platform_detail = {
            "created_date": current_time,
            "id": id_input,
            "password":password_input
          }
         
          new_platform = {
            platform_input:[]
          }
          json_data.update(new_platform)
          json_data[platform_input].append(platform_detail)
          with open('passwords.json','w') as f:
            json.dump(json_data,f)
        else:
          print("\n\tPassword can not be empty")
          input("\n\nPress Enter to Continue :> ")
      else:
        print("\n\tId can not be empty")
        input("\n\nPress Enter to Continue :> ")