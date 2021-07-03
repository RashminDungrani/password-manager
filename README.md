<h1 align="center">
  Password Manager
</h1>

<h4 align="center">
  Store id, passwords and more for command-line habitat
</h4>

## Description

By utilizing a simple and minimal usage syntax, that requires a flat learning curve, Password Manager enables you to effectively manage your Id, passwords and more within your terminal. All data are written atomically to the storage in order to prevent corruptions, and are never shared with anyone or anything.

## Highlights

- Add Id, password and more custom filed you want
- List all your account info in just one keyword
- View Specific Domain of id password with formatted text
- Tab compilation for existing domain and id
- While adding password type "random" to generate random password
- copy password to your clipboard without displaying password

## Installation

- Python 3 or higher version supported

```bash
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

----------
#### alias pypasswords="PATH OF THE run.py" # set alias
----------

## Usage

```
   ____________________________________________________
  |  keyword           | action                        |
  |  -----------------------------------------------   |
  |  view              | To view all Domain            |
  |  view {domain}     | To view Spacific Domain       |
  |  del  {domain->*}  | To detele domain              |
  |  del  {domain->id} | To delete id pass from domain |
  |  edit {domain->id} | To edit id and password       |
  |  copy {domain->id} | to copy pass into clipboard   |
  |____________________________________________________|
```
