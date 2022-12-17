import typer
from pydantic import EmailStr
from validators import domain


def validate_email(value: str) -> EmailStr | None:
    if value == "":
        return None
    try:
        EmailStr.validate(value)
        return EmailStr(value)
    except:
        raise typer.BadParameter("Email is not valid")


def validate_domain(value: str):
    if domain(value):  # type: ignore
        return value
    else:
        raise typer.BadParameter("Domain URL is not valid")
