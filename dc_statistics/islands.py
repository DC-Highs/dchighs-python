import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from dc_statistics._json import as_uint, get, to_camel_dict


@dataclass
class IslandKindStatistics:
    total_count: int
    actives_count: int
    upcomings_count: int
    pasts_count: int

    def to_dict(self) -> Dict[str, Any]:
        return to_camel_dict(self)


@dataclass
class IslandsStatistics:
    total_count: int
    actives_count: int
    upcomings_count: int
    pasts_count: int
    maze: IslandKindStatistics
    tower: IslandKindStatistics
    fog: IslandKindStatistics
    grid: IslandKindStatistics
    heroic_races: IslandKindStatistics
    runner: IslandKindStatistics
    puzzle: IslandKindStatistics

    def to_dict(self) -> Dict[str, Any]:
        return to_camel_dict(self)


@dataclass
class IslandSections:
    """The ``islands`` arrays of each island kind."""

    maze: Sequence[Dict[str, Any]] = field(default_factory=list)
    tower: Sequence[Dict[str, Any]] = field(default_factory=list)
    fog: Sequence[Dict[str, Any]] = field(default_factory=list)
    grid: Sequence[Dict[str, Any]] = field(default_factory=list)
    heroic_races: Sequence[Dict[str, Any]] = field(default_factory=list)
    runner: Sequence[Dict[str, Any]] = field(default_factory=list)
    puzzle: Sequence[Dict[str, Any]] = field(default_factory=list)


def _now() -> int:
    return int(time.time())


def is_active_island(island: Dict[str, Any], now_in_seconds: int) -> bool:
    availability = get(island, "availability")

    if availability is not None:
        start, end = as_uint(get(availability, "from")), as_uint(get(availability, "to"))

        if start is not None and end is not None:
            return start <= now_in_seconds <= end

    start_ts, end_ts = as_uint(get(island, "start_ts")), as_uint(get(island, "end_ts"))

    if start_ts is not None and end_ts is not None:
        return start_ts <= now_in_seconds <= end_ts

    return False


def is_upcoming_island(island: Dict[str, Any], now_in_seconds: int) -> bool:
    availability = get(island, "availability")

    if availability is not None:
        start = as_uint(get(availability, "from"))

        if start is not None:
            return now_in_seconds < start

    start_ts = as_uint(get(island, "start_ts"))

    if start_ts is not None:
        return now_in_seconds < start_ts

    return False


def is_past_island(island: Dict[str, Any], now_in_seconds: int) -> bool:
    availability = get(island, "availability")

    if availability is not None:
        end = as_uint(get(availability, "to"))

        if end is not None:
            return now_in_seconds > end

    end_ts = as_uint(get(island, "end_ts"))

    if end_ts is not None:
        return now_in_seconds > end_ts

    return False


def generate_island_kind_statistics(
    islands: Sequence[Dict[str, Any]], now_in_seconds: Optional[int] = None
) -> IslandKindStatistics:
    now = _now() if now_in_seconds is None else now_in_seconds

    return IslandKindStatistics(
        total_count=len(islands),
        actives_count=sum(1 for island in islands if is_active_island(island, now)),
        upcomings_count=sum(1 for island in islands if is_upcoming_island(island, now)),
        pasts_count=sum(1 for island in islands if is_past_island(island, now)),
    )


def generate_islands_statistics(
    sections: IslandSections, now_in_seconds: Optional[int] = None
) -> IslandsStatistics:
    """Counts the islands of every kind. ``now_in_seconds`` defaults to the current time."""
    now = _now() if now_in_seconds is None else now_in_seconds

    maze = generate_island_kind_statistics(sections.maze, now)
    tower = generate_island_kind_statistics(sections.tower, now)
    fog = generate_island_kind_statistics(sections.fog, now)
    grid = generate_island_kind_statistics(sections.grid, now)
    heroic_races = generate_island_kind_statistics(sections.heroic_races, now)
    runner = generate_island_kind_statistics(sections.runner, now)
    puzzle = generate_island_kind_statistics(sections.puzzle, now)

    kinds: List[IslandKindStatistics] = [maze, tower, fog, grid, heroic_races, runner, puzzle]

    return IslandsStatistics(
        total_count=sum(kind.total_count for kind in kinds),
        actives_count=sum(kind.actives_count for kind in kinds),
        upcomings_count=sum(kind.upcomings_count for kind in kinds),
        pasts_count=sum(kind.pasts_count for kind in kinds),
        maze=maze,
        tower=tower,
        fog=fog,
        grid=grid,
        heroic_races=heroic_races,
        runner=runner,
        puzzle=puzzle,
    )
