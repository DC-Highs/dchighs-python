# Publishing to PyPI

The package is published as **`dchighs`** (the name was free on PyPI when this was written). Releases are built
and uploaded by `.github/workflows/publish.yml` using PyPI *Trusted Publishing*, so no API token is stored in
the repository.

## One-time setup

1. Create the project on PyPI by registering a **pending publisher** at
   <https://pypi.org/manage/account/publishing/>:
   - PyPI project name: `dchighs`
   - Owner: `DC-Highs`, repository: `dchighs-python`
   - Workflow name: `publish.yml`, environment name: `pypi`
2. In the GitHub repository, create an environment named `pypi` (Settings → Environments). Optionally require a
   reviewer so releases need an approval.

(Optional) Do the same on <https://test.pypi.org> to rehearse the release.

## Releasing a version

```sh
poetry version patch          # or minor / major / 0.2.0
# edit CHANGELOG.md
poetry install --all-extras
poetry run poe cov            # must stay at 100%
git commit -am "chore: release $(poetry version -s)"
git tag "v$(poetry version -s)"
git push --follow-tags
```

Then publish a GitHub Release for the tag. The workflow runs the tests, checks that the tag (`vX.Y.Z`) matches
the version in `pyproject.toml`, builds the sdist and wheel, runs `twine check` and uploads them.

## Checking a build locally

```sh
poetry build
pipx run twine check dist/*
```

A `dchighs` wheel installed without extras contains only what `dc_core` needs; installing `dchighs[all]` (or one
of `localization`, `statistics`, `assets`, `config`, `config-mapper`, `client-state`) adds the other modules'
dependencies.

## Manual upload (fallback)

```sh
poetry config pypi-token.pypi <token>
poetry publish --build
```
