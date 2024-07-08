import os
import typer
from typing import Dict
from .project import YepProject

app = typer.Typer()


def _get_project_path(project_path: str):
    if not project_path:
        project_path = os.getcwd()
        print(f"Project path not provided. Using current directory: {project_path}")
    return project_path


def _parse_dict(value: str) -> Dict[str, str]:
    """
    Parse a comma-separated list of key:value pairs into a dictionary.
    
    Takes a string like "key1:value1,key2:value2" and converts it into a dictionary.
    """
    items = value.split(',')
    return dict(item.split(':') for item in items if ':' in item)


@app.command()
def init(project_path: str = ''):
    """Initialize yep project."""
    project = YepProject(_get_project_path(project_path))
    project.initialize()


@app.command()
def wrap(pipeline: str = '*', project_path: str = '', target: str = 'local', update: bool = False):
    """Generate pipeline wrapper for target."""
    project = YepProject(_get_project_path(project_path))
    if pipeline == '*':
        project.wrap_all_pipelines(update=update)
    else:
        # todo: add new target to `.yep/project.toml` under the pipeline section
        project.wrap_pipeline(pipeline, target, update=update)


@app.command()
def run(pipeline: str = None, project_path: str = '', target: str = 'local', 
        vars: str = typer.Option("", help="Variables as key:value pairs separated by commas")):
    """Run pipeline on target."""
    print(f"Run pipeline on {target}.")
    project = YepProject(_get_project_path(project_path))
    if pipeline is None:
        config = project.load_config()
        if len(config['project']['pipelines']) == 0:
            print("No pipelines found in project configuration - see '.yep/project.toml'.")
            return
        # if pipeline is not provided, run the first pipeline
        pipeline = list(config['project']['pipelines'].keys())[0]
    variables = _parse_dict(vars)
    project.run_pipeline(pipeline, target, variables)


def main():
    app()
