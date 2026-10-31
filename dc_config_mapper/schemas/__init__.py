"""Strict input schemas (``*In``) and their ``transform()`` into the normalized output.

Every ``*In`` model rejects unknown top-level fields (like ``z.object().strict()``), so a game update
that adds a field makes the mapper fail loudly instead of silently dropping data.
"""

from dc_config_mapper.schemas import chests, fog, grid, heroic, items, maze, runner, skills, tower

__all__ = ["chests", "fog", "grid", "heroic", "items", "maze", "runner", "skills", "tower"]
