import os
import typer
from .project import YepProject

app = typer.Typer()


def _get_project_path(project_path: str):
    if not project_path:
        project_path = os.getcwd()
        print(f"Project path not provided. Using current directory: {project_path}")
    return project_path


@app.command()
def init(project_path: str = ''):
    """Initialize yep project."""
    project = YepProject(_get_project_path(project_path))
    project.initialize()


@app.command()
def wrap(project_path: str = '', target: str = 'local'):
    """Generate pipeline wrapper for target."""
    print(f"Generate pipeline wrapper for {target}.")
    project = YepProject(_get_project_path(project_path))
    project.wrap(target)


@app.command()
def run(project_path: str = '', target: str = 'local'):
    """Run pipeline on target."""
    print(f"Run pipeline on {target}.")
    project = YepProject(_get_project_path(project_path))
    project.run(target)
    

def main():
    app()
