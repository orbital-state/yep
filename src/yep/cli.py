import os
import typer
from .project import YepProject

app = typer.Typer()


@app.command()
def init(project_path: str = ''):
    """Initialize yep project."""
    if not project_path:
        project_path = os.getcwd()
    project = YepProject(project_path)



@app.command()
def run(target: str = 'local'):
    print(f"Run pipeline on {target}.")
    

def main():
    app()
