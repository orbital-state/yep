"""Dockerize yep (build + push) example.

This pipeline is intentionally simple and linear to match yep's current wrapper model.
It shells out to `docker`.

Notes:
- Defaults are strings because the current reflector only extracts top-level string assignments.
- Each step only declares the inputs it actually needs; the yep wrapper injects only the
    first step's declared arguments.
"""

from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path
from typing import Any


# Reflected defaults (strings only)
image_repo = "orbitalstate/yep"
image_tag = "dev"
publish_latest = "false"
dry_run = "true"

# Run docker build from the repo root (paths are relative to this example directory)
context_dir = "../.."
dockerfile = "../../Dockerfile"


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _run(cmd: list[str], *, cwd: str | None, env: dict[str, str] | None, dry: bool) -> None:
    rendered = " ".join(shlex.quote(p) for p in cmd)
    print(f"$ {rendered}")
    if dry:
        return
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def docker_build(
    image_repo: str,
    image_tag: str,
    context_dir: str,
    dockerfile: str,
    publish_latest: str,
    dry_run: str,
) -> tuple[str, str, str, str]:
    """Build the docker image."""
    image_repo = str(image_repo).strip()
    image_tag = str(image_tag).strip()
    image_ref = f"{image_repo}:{image_tag}"

    _run(
        [
            "docker",
            "build",
            "-f",
            dockerfile,
            "-t",
            image_ref,
            context_dir,
        ],
        cwd=None,
        env=None,
        dry=_parse_bool(dry_run),
    )

    # Pass through values needed by later steps.
    return image_ref, image_repo, publish_latest, dry_run


def docker_login(image_ref: str, image_repo: str, publish_latest: str, dry_run: str) -> tuple[str, str, str, str]:
    """Login to Docker Hub (skipped in dry-run mode)."""
    _ = image_ref

    if _parse_bool(dry_run):
        print("$ docker login -u $DOCKERHUB_USERNAME --password-stdin")
        return image_ref, image_repo, publish_latest, dry_run

    username = os.environ.get("DOCKERHUB_USERNAME", "").strip()
    token = os.environ.get("DOCKERHUB_TOKEN", "")
    if not username or not token:
        raise RuntimeError(
            "Missing Docker Hub credentials. Set env vars DOCKERHUB_USERNAME and DOCKERHUB_TOKEN."
        )

    cmd = ["docker", "login", "-u", username, "--password-stdin"]
    print(f"$ {' '.join(shlex.quote(p) for p in cmd)}")
    subprocess.run(cmd, input=token.encode("utf-8"), check=True)
    return image_ref, image_repo, publish_latest, dry_run


def docker_push(image_ref: str, image_repo: str, publish_latest: str, dry_run: str) -> str:
    """Push the image, and optionally tag/push :latest."""
    dry = _parse_bool(dry_run)
    _run(["docker", "push", image_ref], cwd=None, env=None, dry=dry)

    if _parse_bool(publish_latest):
        latest_ref = f"{str(image_repo).strip()}:latest"
        _run(["docker", "tag", image_ref, latest_ref], cwd=None, env=None, dry=dry)
        _run(["docker", "push", latest_ref], cwd=None, env=None, dry=dry)
        print(f"Pushed: {image_ref} and {latest_ref}")
    else:
        print(f"Pushed: {image_ref}")

    return image_ref


def done(image_ref: str) -> str:
    return image_ref
