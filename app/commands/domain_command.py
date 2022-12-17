import typer

from app.utils.validators import validate_domain

domain_app = typer.Typer()


@domain_app.command(name="add")
def domain(
    domain_url: str = typer.Option(..., prompt=True, callback=validate_domain),
):
    print(domain_url)
