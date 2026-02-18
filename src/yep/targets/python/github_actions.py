"""GitHub Actions target.

This target is generate-only: it writes a workflow YAML under `.github/workflows/`.
Execution still happens via the existing `local` target (the workflow runs `yep run --target local`).
"""

from __future__ import annotations

from pathlib import Path

from ..base import BaseTarget


class GithubActionsTarget(BaseTarget):
    def generate_wrapper(self, pipeline_name, pipeline_config, pipeline_file_path, update: bool = False):
        pipeline = pipeline_config["project"]["pipelines"][pipeline_name]
        workflow_path_value = pipeline.get("workflow_path")
        if not workflow_path_value:
            raise ValueError(
                "Missing `workflow_path` in .yep/project.toml for this pipeline. "
                "Set it to a path like '../../.github/workflows/yep-dockerhub.yml'."
            )

        workflow_path = (self.project_folder / workflow_path_value).resolve()
        workflow_path.parent.mkdir(parents=True, exist_ok=True)

        if workflow_path.exists() and not update:
            print(f"Workflow already exists at: {workflow_path}")
            return workflow_path

        # Workflow runs from the example project directory so local wrappers can import modules.
        project_rel = self.project_folder.relative_to(Path.cwd()) if self.project_folder.is_relative_to(Path.cwd()) else None
        working_dir = str(project_rel) if project_rel else str(self.project_folder)

        content = self._render_workflow_yaml(working_dir=working_dir)
        workflow_path.write_text(content)
        print(f"Workflow written to: {workflow_path}")
        return workflow_path

    def run_pipeline(self, pipeline_name, config, pipeline_file_path, vars):
        raise RuntimeError(
            "github-actions target does not execute pipelines locally. "
            "Run `yep wrap` to generate the workflow, then let GitHub Actions run it."
        )

    @staticmethod
    def _render_workflow_yaml(*, working_dir: str) -> str:
        # Keep the workflow deliberately simple and cheap:
        # - Push sha-tagged images on every push to main and on tags
        # - Push latest only from main
        return f"""name: yep dockerhub publish

on:
  push:
    branches: [\"main\"]
    tags: [\"*\"]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: \"3.11\"

      - name: Install yep
        run: python -m pip install -e .

      - name: Wrap pipelines (local + github-actions)
        working-directory: {working_dir}
        run: yep wrap --update

      - name: Build + push yep image (via local target)
        working-directory: {working_dir}
        env:
          DOCKERHUB_USERNAME: ${{{{ secrets.DOCKERHUB_USERNAME }}}}
          DOCKERHUB_TOKEN: ${{{{ secrets.DOCKERHUB_TOKEN }}}}
        run: |
          set -euo pipefail
          publish_latest=false
          if [[ \"${{{{ github.ref }}}}\" == \"refs/heads/main\" ]]; then
            publish_latest=true
          fi

          yep run --target local --vars \
            image_repo:orbitalstate/yep,\
            image_tag:${{{{ github.sha }}}},\
            publish_latest:$publish_latest,\
            dry_run:false
"""