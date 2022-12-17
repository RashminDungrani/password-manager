import os
from pathlib import Path

import typer


class AppPaths:
    # base: str = os.path.dirname(__file__)
    PROJECT_ROOT: str = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent)
    # static: str = os.path.join(base, "static")
    # media: str = os.path.join(static, "media")

    # * app specific
    # TODO: use this path for storing sqlite database but for somehow it throws sqlite connection error on this path
    # app_dir = typer.get_app_dir("PasswordManager")
    # storage_dir: str = os.path.join(app_dir, "storage")
    DB_FILE: str = os.path.relpath(os.path.join(PROJECT_ROOT, "creds.db"))

    def __init__(self) -> None:
        # os.makedirs(self.storage_dir, exist_ok=True)
        # print("dwadawd")
        pass


app_paths = AppPaths()
