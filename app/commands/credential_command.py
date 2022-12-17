import readline

import typer
from pydantic import EmailStr
from rich.console import Console
from rich.table import Table

from app.daos.credential_dao import CredentialDAO
from app.daos.domain_dao import DomainDAO
from app.daos.third_party_dao import ThirdPartyDAO
from app.models.credential_model import (
    Credential,
    CredentialInput,
    CredentialReadWithDomain,
)
from app.models.domain_model import Domain
from app.models.third_party_model import ThirdParty, ThirdPartyInput
from app.utils.tab_completer import TabCompleter
from app.utils.validators import validate_email

cred_app = typer.Typer()


def domain_proc(value: str) -> Domain:
    domain = DomainDAO().select_by_domain_name(value)
    if domain:
        return domain

    raise typer.BadParameter(f"There is no domain start with {value}")


def pin_proc(value: str) -> int | None:
    if value == "":
        return None
    if not value.isnumeric():
        raise typer.BadParameter("pin must be a number")
    int_value: int = int(value)
    if int_value > 999 and int_value < 1_000_000:
        return int_value
    raise typer.BadParameter("pin must be between range 999 - 1_000_000")


def mobile_proc(value: str) -> str | None:
    if value == "":
        return None
    if len(value) < 8:
        raise typer.BadParameter("Please ensure that mobile has at least 8 characters")
    return value


def optional_proc(value: str) -> str | None:
    if value == "":
        return None
    return value


def search_by_third_party_option_proc(value: str) -> str:
    if value in ["username", "email", "mobile"]:
        return value
    raise typer.BadParameter("Please select from 3 options")


@cred_app.command(name="add")
def add_credential(
    # domain: Optional[str] = typer.Option(..., autocompletion=complete_domain,  prompt=True, prompt_required=False, comple)
    # username: Optional[str] = typer.Option(default=None, prompt=True, callback=validate_username),
    # email: Optional[str] = typer.Option(default=None, prompt=True, callback=validate_email),
    # password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True),
    is_third_party_signup: bool = typer.Option(default=False, prompt="Signup with third party?")
):

    available_domains = DomainDAO().select_all()
    available_domains = list(map(lambda x: x.domain_name, available_domains))

    readline.set_completer(TabCompleter(commands=available_domains).complete)
    domain: Domain = typer.prompt(text="Domain", value_proc=domain_proc)

    if is_third_party_signup:
        readline.set_completer(TabCompleter(commands=available_domains).complete)
        domain_of_third_party: Domain = typer.prompt(text="Domain of third party", value_proc=domain_proc)

        readline.set_completer(TabCompleter(commands=["username", "email", "mobile"]).complete)
        search_by_option: str = typer.prompt(
            text="Search third party credential by username | email | mobile?",
            value_proc=search_by_third_party_option_proc,
        )

        available_third_party_creds: list[Credential] = CredentialDAO().select_filter_by_domain_id(domain_id=domain_of_third_party.id)  # type: ignore
        if not available_third_party_creds:
            typer.secho(f"Under {domain_of_third_party.domain_name} domain there are no credential available")
            raise typer.Exit()

        match search_by_option:
            case "username":
                third_party_usernames: list[str] = [
                    x.username for x in available_third_party_creds if x.username != None
                ]
                if not third_party_usernames:
                    typer.secho(f"mobiles not available for domain {domain_of_third_party.domain_name}")
                    raise typer.Exit()
                readline.set_completer(TabCompleter(commands=third_party_usernames).complete)
                signup_with_third_party_cred = typer.prompt(
                    text="Search third party cred by username",
                )
                if signup_with_third_party_cred not in third_party_usernames:
                    raise typer.BadParameter("Invalid third party username")

                signup_with_third_party_cred = available_third_party_creds[
                    third_party_usernames.index(signup_with_third_party_cred)
                ]
            case "email":
                third_party_emails: list[str] = [x.email for x in available_third_party_creds if x.email != None]
                if not third_party_emails:
                    typer.secho(f"emails not available for domain {domain_of_third_party.domain_name}")
                    raise typer.Exit()
                readline.set_completer(TabCompleter(commands=third_party_emails).complete)
                signup_with_third_party_cred = typer.prompt(
                    text="Search third party cred by email",
                )
                if signup_with_third_party_cred not in third_party_emails:
                    raise typer.BadParameter("Invalid third party email")

                signup_with_third_party_cred = available_third_party_creds[
                    third_party_emails.index(signup_with_third_party_cred)
                ]
            case "mobile":
                third_party_mobiles: list[str] = [x.mobile for x in available_third_party_creds if x.mobile != None]
                if not third_party_mobiles:
                    typer.secho(f"mobiles not available for domain {domain_of_third_party.domain_name}")
                    raise typer.Exit()
                readline.set_completer(TabCompleter(commands=third_party_mobiles).complete)
                signup_with_third_party_cred = typer.prompt(
                    text="Search third party cred by mobile",
                )
                if signup_with_third_party_cred not in third_party_mobiles:
                    raise typer.BadParameter("Third party mobile is incorrect")

                signup_with_third_party_cred = available_third_party_creds[
                    third_party_mobiles.index(signup_with_third_party_cred)
                ]

        mobile: str | None = typer.prompt(default="", show_default=False, text="Mobile", value_proc=mobile_proc)

        pin: int | None = typer.prompt(default="", show_default=False, text="Pin", type=int, value_proc=pin_proc)

        note: str | None = typer.prompt(default="", show_default=False, text="Note", value_proc=optional_proc)

        inserted_cred = CredentialDAO().insert(
            inserted_credential=CredentialInput(
                domain_id=domain.id,  # type: ignore
                pin=pin,
                mobile=mobile,
                note=note,
                third_party_cred_id=signup_with_third_party_cred.id,  # type: ignore
            )
        )
        third_part_input = ThirdPartyInput(
            signup_cred_id=inserted_cred.id,  # type: ignore
            signup_with_third_party_cred_id=signup_with_third_party_cred.id,  # type: ignore
        )
        ThirdPartyDAO().insert(third_party_input=third_part_input)
        typer.secho("Credential Saved as third party")

        return

    # third_party_cred: Optional[ThirdParty] = typer.prompt(default=None, text="", value_proc=domain_proc)

    # ✅ Optional username input and checking if username already exist in database with selected domain
    while True:
        username: str | None = typer.prompt(default="", show_default=False, text="Username", value_proc=optional_proc)
        if not username:
            break
        assert domain.id is not None
        creds = CredentialDAO().select_by_username_and_domain(domain_id=domain.id, username=username)

        # print(list(map(lambda x: x.username, creds)))
        if len(creds) > 0:
            raise typer.BadParameter(f"Username {username} is already exist in {domain.domain_name} Domain")
        else:
            break

    email: EmailStr | None = typer.prompt(default="", text="Email", show_default=False, value_proc=validate_email)

    mobile: str | None = typer.prompt(default="", show_default=False, text="Mobile", value_proc=mobile_proc)

    if username == "" and email == None and mobile == None:
        raise typer.BadParameter("At least one value needed from username or email or mobile")

    password: str | None = typer.prompt(
        default="",
        show_default=False,
        text="Password",
        confirmation_prompt=True,
        hide_input=True,
        value_proc=optional_proc,
    )

    pin: int | None = typer.prompt(default="", show_default=False, text="Pin", type=int, value_proc=pin_proc)

    if password == None and pin == None:
        raise typer.BadParameter("At least one value needed from password or pin")

    note: str | None = typer.prompt(default="", show_default=False, text="Note", value_proc=optional_proc)

    CredentialDAO().insert(
        inserted_credential=CredentialInput(
            domain_id=domain.id,  # type: ignore
            username=username,
            email=email,  # type: ignore
            mobile=mobile,
            password=password,
            pin=pin,
            note=note,
            third_party_cred_id=None,
        )
    )
    typer.secho("Credential Saved")


def view_option_proc(value: str):
    try:
        if int(value) in [1, 2, 3, 4]:
            return int(value)
        raise typer.BadParameter("Please select from 1 to 4 range")
    except:
        raise typer.BadParameter("Please select from 1 to 4 range")


@cred_app.command("view")
def view_credential():

    # readline.set_completer(TabCompleter(commands=["view all", "by domain", "specific"]).complete)
    print(
        """
1. All
2. Filter By Domain
3. Specific
4. All Third party creds
"""
    )
    search_option: int = typer.prompt(
        text="View by?",
        type=int,
        value_proc=view_option_proc,
    )

    def display_credentials_into_table(data: list[CredentialReadWithDomain]):
        table = Table()

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Domain", style="magenta")
        table.add_column("Email", style="magenta")
        table.add_column("Username", style="magenta")
        table.add_column("Password", style="magenta")
        table.add_column("Pin", style="magenta")
        table.add_column("Mobile", style="magenta")
        table.add_column("Signup with Third party", justify="center", style="green")

        for item in data:
            table.add_row(
                str(item.id) if item.id else None,
                item.domain.domain_name,
                item.email,
                item.username,
                item.password,
                str(item.pin) if item.pin else None,
                item.mobile,
                str(item.third_party_cred_id) if item.third_party_cred_id else None,
            )

        console = Console()
        console.print(table)

    match search_option:
        case 1:
            # "view all"
            data = CredentialDAO().select_all_with_domain()
            display_credentials_into_table(data)

        case 2:
            # "by domain"
            available_domains = DomainDAO().select_all()
            available_domains = list(map(lambda x: x.domain_name, available_domains))

            if not available_domains:
                typer.secho("Domains are not available")
                raise typer.Exit()

            readline.set_completer(TabCompleter(commands=available_domains).complete)
            domain: Domain = typer.prompt(text="Domain", value_proc=domain_proc)

            data = CredentialDAO().select_under_x_domain_with_domain(domain_id=domain.id)  # type: ignore
            display_credentials_into_table(data)
        case 3:
            # "specific"
            print(
                """
1. ID
2. Username
3. Email
4. Mobile
"""
            )
            search_option: int = typer.prompt(
                text="Search by?",
                type=int,
                value_proc=view_option_proc,
            )
            match search_option:
                case 1:
                    credential_id: int = typer.prompt("Credential ID", type=int)
                    cred = CredentialDAO().select_one_with_domain(credential_id=credential_id)
                    display_credentials_into_table([cred])
                case 2:
                    username: str = typer.prompt("Username (ilike)", type=str)
                    creds = CredentialDAO().select_by_username(username=username)
                    display_credentials_into_table(creds)
                case 3:
                    email: str = typer.prompt("Email (ilike)", type=str)
                    creds = CredentialDAO().select_by_email(email=email)
                    display_credentials_into_table(creds)
                case 4:
                    mobile: str = typer.prompt("Mobile (ilike)", type=str)
                    creds = CredentialDAO().select_by_mobile(mobile=mobile)
                    display_credentials_into_table(creds)

        case 4:
            # "All Third party creds"
            data = CredentialDAO().select_all_third_party_with_domain()
            display_credentials_into_table(data)
