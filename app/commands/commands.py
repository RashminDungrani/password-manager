from typer import Typer

from app.commands.credential_command import cred_app
from app.commands.domain_command import domain_app
from app.commands.third_party_cred_command import third_party_cred_app

app = Typer()

app.add_typer(domain_app, name="domain")
app.add_typer(cred_app, name="cred")
app.add_typer(third_party_cred_app, name="third-party-cred")
