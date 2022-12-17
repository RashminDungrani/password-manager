import typer

from app.daos.domain_dao import DomainDAO
from app.utils.validators import validate_domain

domain_app = typer.Typer()


@domain_app.command(name="add")
def add_domain(
    domain_url: str = typer.Option(..., prompt=True, callback=validate_domain),
):
    DomainDAO().insert(domain_url)
    typer.secho("Domain Added")


@domain_app.command(name="del-all")
def delete_all_domain(
    confirm: bool = typer.Option(..., prompt=True, confirmation_prompt=True),
):
    if confirm:
        DomainDAO().delete_all()
