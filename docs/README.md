# Documentation

`dchighs` is a set of independent modules. **`dc_core` is the only required one**; everything else is opt-in
through a pip/Poetry *extra* that installs just the third-party packages that module needs.

| module | extra | third-party deps | docs |
| --- | --- | --- | --- |
| `dc_core` | *(always installed)* | none | [dc-core](dc-core.md) |
| `dc_localization` | `localization` | `httpx` | [dc-localization](dc-localization.md) |
| `dc_statistics` | `statistics` | none | [dc-statistics](dc-statistics.md) |
| `dc_assets` | `assets` | `httpx` | [dc-assets](dc-assets.md) |
| `dc_config` | `config` | `httpx`, `pydantic` | [dc-config](dc-config.md) |
| `dc_config_mapper` | `config-mapper` | `httpx`, `pydantic`, `pluralizer` | [dc-config-mapper](dc-config-mapper.md) |
| `dc_client_state` | `client-state` | none | [dc-client-state](dc-client-state.md) |

`dc_config_mapper` also uses `dc_localization` (hence `httpx`), and every module uses `dc_core`.

## Installing

```sh
poetry add dchighs                              # dc_core only
poetry add "dchighs[localization,assets]"       # pick the modules you need
poetry add "dchighs[all]"                       # everything

pip install "dchighs[config-mapper]"            # same with pip
```

Importing a module whose extra is not installed fails with the usual `ModuleNotFoundError` for the missing
package (`httpx`, `pydantic` or `pluralizer`).

Working on this repository:

```sh
poetry install --all-extras
poetry run pytest
```

## Releasing

See [publishing](publishing.md) for the PyPI release process.

## Conventions

- Every import name keeps the `dc_` prefix of the original `@dchighs/dc-*` packages.
- Network calls are `async` and use `httpx`; pass your own `httpx.AsyncClient` through the `client` argument.
- Enum members are `UPPER_CASE`; string enums subclass `str`, so they compare equal to their wire value.
- Fan-made, not affiliated with SocialPoint.
