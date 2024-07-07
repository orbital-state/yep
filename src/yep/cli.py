import os
import typer
from .project import Project

app = typer.Typer()


@app.command()
def init(project_path: str = ''):
    """Initialize yep project."""
    if not project_path:
        project_path = os.getcwd()
    project = Project(project_path)


@app.command()
def run(username: str):
    print(f"Deleting user: {username}")


def main():
    app()
