import typer

cred_app = typer.Typer()


@cred_app.command(name="add")
def credential(username: str, email: str, password: str):
    pass
