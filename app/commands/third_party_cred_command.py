import typer

third_party_cred_app = typer.Typer()


@third_party_cred_app.command(name="add")
def provider(
    provider: str = typer.Option(..., prompt=True),
):
    print(provider)
