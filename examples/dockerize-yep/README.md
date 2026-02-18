# dockerize-yep (example)

This example demonstrates using **yep** to run a simple DevOps-style pipeline that:

1. Builds the yep Docker image
2. Logs into Docker Hub
3. Pushes the image as `orbitalstate/yep:<tag>`
4. Optionally tags/pushes `orbitalstate/yep:latest`

## Prereqs

- `docker` installed and running
- (For pushing) env vars:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`

## Local (dry-run)

By default this pipeline runs in dry-run mode and prints docker commands.

```bash
cd examples/dockerize-yep
python -m pip install -e ../..
yep wrap --update
yep run --target local --vars image_tag:dev,publish_latest:false,dry_run:true
```

## Local (push for real)

```bash
cd examples/dockerize-yep
python -m pip install -e ../..
export DOCKERHUB_USERNAME=...
export DOCKERHUB_TOKEN=...

yep wrap --update
yep run --target local --vars image_tag:dev,publish_latest:false,dry_run:false
```

## GitHub Actions

The `github-actions` target generates a workflow at `.github/workflows/yep-dockerhub.yml`.

Required repo secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
