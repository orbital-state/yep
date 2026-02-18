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
from pathlib import Path
from typing import Any

import sh


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

    context_dir_abs = str(Path(str(context_dir)).resolve())
    dockerfile_abs = str(Path(str(dockerfile)).resolve())
    dry = _parse_bool(dry_run)

    cmd = ["docker", "build", "-f", dockerfile_abs, "-t", image_ref, context_dir_abs]
    print(f"$ {' '.join(shlex.quote(p) for p in cmd)}")
    if not dry:
        sh.docker("build", "-f", dockerfile_abs, "-t", image_ref, context_dir_abs)

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
    sh.docker("login", "-u", username, "--password-stdin", _in=f"{token}\n")
    return image_ref, image_repo, publish_latest, dry_run


def docker_push(image_ref: str, image_repo: str, publish_latest: str, dry_run: str) -> str:
    """Push the image, and optionally tag/push :latest."""
    dry = _parse_bool(dry_run)
    cmd = ["docker", "push", image_ref]
    print(f"$ {' '.join(shlex.quote(p) for p in cmd)}")
    if not dry:
        sh.docker("push", image_ref)

    if _parse_bool(publish_latest):
        latest_ref = f"{str(image_repo).strip()}:latest"
        tag_cmd = ["docker", "tag", image_ref, latest_ref]
        print(f"$ {' '.join(shlex.quote(p) for p in tag_cmd)}")
        if not dry:
            sh.docker("tag", image_ref, latest_ref)

        push_latest_cmd = ["docker", "push", latest_ref]
        print(f"$ {' '.join(shlex.quote(p) for p in push_latest_cmd)}")
        if not dry:
            sh.docker("push", latest_ref)
        print(f"Pushed: {image_ref} and {latest_ref}")
    else:
        print(f"Pushed: {image_ref}")

    return image_ref


def done(image_ref: str) -> str:
    return image_ref
