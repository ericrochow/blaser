#!/usr/bin/env python3
"""
"""
# import logging

# from typing import Generator, List, Optional
from typing import Optional

import requests

# from sseclient import SSEClient

# from blaser.__version__ import __title__, __version__


class BlaseballReferenceAPI:

    VALID_CATEGORIES = ["batting", "pitching", "fielding", "running"]
    VALID_STATS = {
        "batting": [
            "batting_average",
            "on_base_percentage",
            "slugging",
            "plate_appearances",
            "at_bats",
            "hits",
            "walks",
            "singles",
            "doubles",
            "triples",
            "home_runs",
            "runs_batted_in",
            "strikeouts",
            "sacrifices",
            "at_bats_risp",
            "hits_risps",
            "batting_average_risp",
            "on_base_slugging",
            "total_bases",
            "hbps",
            "ground_outs",
            "flyouts",
            "gidps",
        ],
        "pitching": [
            "games",
            "pitch_count",
            "outs_recorded",
            "innings",
            "runs_allowed",
            "era",
            "strikeouts",
            "k_per_9",
            "walks",
            "hrs_allowed",
            "hits_allowed",
        ],
        "fielding": ["plays"],
        "running": ["stolen_bases", "caught_stealing", "runs"],
    }

    def __init__(self) -> None:
        self.base_url = "https://api.blaseball-reference.com/v1"
        self.sess = requests.Session()

    def __repr__(self) -> str:
        """"""
        return f"{self.__class__.__name__}"

    def _get(self, request: str, payload: Optional[dict] = None) -> dict:
        url = f"{self.base_url}/{request}"
        resp = self.sess.get(url, params=payload)
        if resp.ok:
            return resp.json()
        else:
            resp.raise_for_status()

    # Raw Data
    def get_raw_data(self, season: int) -> dict:
        """

        Args:
          season:
        Returns:
          A dict
        """
        method = "/data/events"
        params = {"season": season - 1}
        return self._get(method, payload=params)

    # Game Events
    def get_game_events(self) -> dict:
        """
        Queries for game events.

        Args:
        Returns:
        """
        method = "events"
        return self._get(method)

    def count_by_type(self, event_type: str, player_type: str, player_id: str) -> dict:
        """
        Calculates the number of events for each batter or pitcher.

        Args:
        Returns:
        """
        method = "countByType"
        params = {"eventType": event_type}
        if player_type.lower() == "batter":
            params["batterId"] = player_id
        elif player_type.lower() == "pitcher":
            params["pitcherId"] = player_id
        else:
            raise ValueError("player_type must be one of ['batter', 'pitcher']")
        return self._get(method, payload=params)

    # Players
    def list_deceased_players(self) -> dict:
        """
        Gets a list of all currently deceased players.

        Args:
        Returns:
        """
        method = "deceased"
        return self._get(method)

    def list_player_ids_by_name(
        self, name: str, current: Optional[bool] = False
    ) -> dict:
        """
        Lists player IDs matching a given player name.

        Args:
          name:
          current:
        Returns:
        """
        method = "playerIdsByName"
        params = {"name": name, "current": current}
        return self._get(method, payload=params)

    def get_player_info(
        self,
        player_id: Optional[str] = None,
        name: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> dict:
        """
        Gets extended info for a given player: name, attributes, ratings, and stars.

        Args:
          player_id
          name:
          slug:
        Returns
        """
        method = "playerInfo"
        params = {}
        if player_id:
            params["playerId"] = player_id
        elif name:
            params["name"] = name
        elif slug:
            params["slug"] = slug
        else:
            raise ValueError("Must specify one of ['player_id', 'name', 'slug'].")
        return self._get(method, payload=params)

    def list_tagged_players(self) -> list:
        """
        Lists all players with a given modification tag.

        Returns:
        """
        method = "taggedPlayers"
        return self._get(method)

    def list_all_players(self, include_shadows: Optional[bool] = False) -> dict:
        """
        Lists all players

        Args:
        Returns
        """
        method = "allPlayers"
        params = {"includeShadows": include_shadows}
        return self._get(method, payload=params)

    def list_all_players_for_gameday(self, season: int, day: int) -> dict:
        """
        Lists all players for a given season and gameday.

        The internal API objects are zero-indexed, so the method performs the math for
            user-friendlyness.

        Args:
          season:
          day:
        Returns:
        """
        method = "allPlayersForGameday"
        params = {"season": season - 1, "day": day - 1}
        return self._get(method, payload=params)

    # Teams
    def get_current_roster(self, team_id: str = None, slug: str = None) -> dict:
        """
        Args:
        Returns:
        Raises:
          ValueError: Neither team_id nor slug were set.
        """
        method = "currentRoster"
        if not (team_id or slug):
            raise ValueError("Either team_id or slug must be set.")
        params = {}
        if team_id:
            params["teamId"] = team_id
        if slug:
            params["slug"] = slug
        return self._get(method, payload=params)

    def list_all_teams(self) -> dict:
        """
        List all teams.

        Args:
        Returns:
        """
        method = "allTeams"
        return self._get(method)

    def list_team_stars(self) -> dict:
        """
        Args:
        Returns:
        """
        method = "allTeamStars"
        return self._get(method)

    # Statistics
    def get_season_leaders(
        self,
        season: int,
        category: str,
        stat: str,
        order: str = "DESC",
        limit: int = 10,
    ) -> dict:
        """
        Gets the season leaders for a given category and stat.

        Args:
          season:
          category:
          stat:
          order:
          limit:
        Returns:
        """
        valid_orders = ["ASC", "DESC"]
        method = "seasonLeaders"
        if category.lower() not in self.VALID_CATEGORIES:
            raise ValueError(f"'category' must be one of {self.VALID_CATEGORIES}.")
        if stat.lower() not in self.VALID_STATS[category]:
            raise ValueError(f"'stat' must be one of {self.VALID_STATS[category]}.")
        if order.upper() not in valid_orders:
            raise ValueError(f"'order' must be one of {valid_orders}.")
        params = {
            "season": season - 1,
            "category": category.lower(),
            "stat": stat,
            "order": order.upper(),
            "limit": limit,
        }
        return self._get(method, payload=params)

    def get_player_stats(
        self, category: str, player_ids: list, season: int = None
    ) -> dict:
        """
        Args:
        Returns:
        """
        method = "playerStats"
        if category.lower() not in self.VALID_CATEGORIES:
            raise ValueError(f"'category' must be one of {self.VALID_CATEGORIES}")
        if isinstance(player_ids, list):
            player_ids = ",".join(player_ids)
        params = {"category": category, "playerIds": player_ids}
        if season:
            params["season"] = season - 1
        return self._get(method, payload=params)
