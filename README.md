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

1. Install dependencies with poetry
    ```bash
    poetry install
    ```
1. Run DB migration
    ```bash
    alembic upgrade head
    ```
1. Start CLI app
    ```bash
    python -m app --help
    ```

## Usage
<!-- TODO -->