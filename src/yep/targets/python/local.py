"""Local target implementation."""

import importlib
import os
from pathlib import Path
from ..base import BaseTarget
from ...reflectors.pipeline import YepPipeline


class LocalTarget(BaseTarget):
        
    def generate_wrapper(self, pipeline_name, pipeline_config, pipeline_file_path, update: bool = False):
        """
        Generate pipeline wrapper for local target.
        
        Generate code like below and write into wrapper file

            words = read_file(file_path)
            mapped_words = map_words_to_counts(words)
            word_counts = reduce_word_counts(mapped_words)

        Note that input of the next function is the output of the previous function
        except the first function which takes input from the `vars` dictionary.
        Also the last output is returned as the result of the pipeline function.
        """
        # Init wrapper location
        wrapper_path = self.target_folder /f"{pipeline_name}_wrapper.py"
        if wrapper_path.exists() and not update:
            print(f"Wrapper already exists at: {wrapper_path}")
            return
        print(f"Wrapper will be generated at: {wrapper_path}")
        # touch '__init__.py' file in target folder
        init_file = self.target_folder / "__init__.py"
        if not init_file.exists():
            init_file.touch()

        # Reflect pipeline structure from source code
        yep_pipeline = self.reflect_pipeline(pipeline_name, pipeline_config, pipeline_file_path)
        # Generate code from yep_pipeline

        mod_name = str(pipeline_file_path.name).split('.')[0]
        with open(wrapper_path, 'w') as f:
            f.write(f"# Wrapper for local target\n")
            step_functions = ', '.join([task['name'] for task in yep_pipeline.tasks])
            # Import all functions from pipeline file
            f.write(f"from {mod_name} import {step_functions}\n") 
            f.write(f"\n\ndef run(vars):\n")
            for index, task in enumerate(yep_pipeline.tasks):
                # TODO: below logic gets complicated when we want to substitute arbitrary variables
                print(f"\tTask: {task['name']} with args: {task['args']}")
                is_first = index == 0
                is_last = index == len(yep_pipeline.tasks) - 1
                # lookup the names of the next input args
                if is_last:
                    next_arg_names = []
                else:
                    next_arg_names = [arg for arg in yep_pipeline.tasks[index + 1]['args']]
                # Call the function to get the output as next input
                print(f"\tNext arg names: {next_arg_names}")
                if len(next_arg_names) > 0:
                    if is_first:
                        f.write(f"    {', '.join(next_arg_names)} = {task['name']}(**vars)\n")
                    else:
                        f.write(f"    {', '.join(next_arg_names)} = {task['name']}({', '.join(task['args'])})\n")
                else:
                    f.write(f"    return {task['name']}({', '.join(task['args'])})\n")
            f.write(f"\n\nif __name__ == '__main__':\n")
            f.write(f"    print(run({{}}))\n")
        print(f"Wrapper code written to: {wrapper_path}")
        return wrapper_path

    def run_pipeline(self, pipeline_name, config, pipeline_file_path, vars):
        """Run pipeline on local target."""
        # append current working directory to sys.path
        import sys
        sys.path.append(os.getcwd())
        # exec file with wrapper module
        wrapper_path = self.target_folder / f"{pipeline_name}_wrapper.py"
        spec=importlib.util.spec_from_file_location(f"{pipeline_name}_wrapper", wrapper_path)
        # creates a new module based on spec
        wrapper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper)
        # run pipeline
        return wrapper.run(vars)
