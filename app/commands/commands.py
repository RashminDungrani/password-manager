from typer import Typer

from app.commands.credential_command import cred_app
from app.commands.domain_command import domain_app

app = Typer()


app.add_typer(domain_app, name="domain")
app.add_typer(cred_app, name="cred")
