#!/usr/bin/env python3
"""
"""
# import logging

from typing import Generator, List, Optional

import requests
from sseclient import SSEClient

from blaser.__version__ import __title__, __version__


class BlaseballAPI:
    """Class to interact with the internal API for IBL blaseball."""

    def __init__(self) -> None:
        """
        Interacts with the internal Blaseball API.

        Attributes:
          user_agent:
          headers:
          base_url:
          sess: A requests Session() object
        """
        self.user_agent = f"{__title__}/{__version__}"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        self.base_url = "https://www.blaseball.com"
        self.sess = requests.Session()

    def __repr__(self) -> str:
        """REPR returns the name of the class."""
        return f"{self.__class__.__name__}"

    def _get(self, request: str, payload: Optional[dict] = None) -> dict:
        """
        Performs an HTTP GET request.

        Args:
          request: A string containing the URI of the requested API endpoint
          payload: A dict containing the params to URL-encode into the URI (optional)
        Returns:
          A dict containing the JSON output of the GET request.
        """
        url = f"{self.base_url}/{request}"
        resp = self.sess.get(url, params=payload, headers=self.headers)
        if resp.ok:
            return resp.json()
        else:
            resp.raise_for_status()

    def _sse(
        self, request: str, payload: Optional[dict] = None
    ) -> Generator[dict, None, None]:
        """
        Subscribes to a Server Sent Event stream.

        Args:
          request: A string containing the URI of the requested API endpoint
          payload: A dict containing the params to URL-encode into the URI (optional)
        Yields:
          Something once this actually starts working.
        """
        url = f"{self.base_url}/{request}"
        messages = SSEClient(url)
        for msg in messages:
            yield msg.json()

    # Live Data
    def stream_data(self) -> dict:
        """
        Subscribes to the same datastream the API uses to power the www.blaseball.com
            site using Server-sent Events.

        Every few seconds a data event will be sent.

        Returns:
        """
        request = "database/streamData"
        return self._sse(request)

    # Objects
    def get_league_info(self, league_id: str) -> dict:
        """
        Gets information for a league given its ID.

        Args:
          league_id:
        Returns:
        """
        request = "database/league"
        params = {"id": league_id}
        return self._get(request, payload=params)

    def get_subleague_info(self, subleague_id: str) -> dict:
        """
        Gets information for a subleague given its ID.

        Args:
          subleague_id:
        Returns:
        """
        request = "database/subleague"
        params = {"id": subleague_id}
        return self._get(request, payload=params)

    def get_division_info(self, division_id: str) -> dict:
        """
        Gets information for a division given its ID.

        Returns:
        """
        request = "database/division"
        params = {"id": division_id}
        return self._get(request, payload=params)

    def get_team_info(self, team_id: str) -> dict:
        """
        Gets information for a team given its ID.

        Args:
          team_id:

        Returns:
        """
        request = "database/team"
        params = {"id": team_id}
        return self._get(request, params)

    def get_player_info(self, player_ids: List[str]) -> dict:
        """
        Gets information for a player or list of players provided their ID(s).

        Args:
          player_ids: A string or list of strings specifying the player or players
              whose information to look up
        Returns:
          A dict
        """
        request = "database/players"
        if isinstance(player_ids, list):
            player_ids = ",".join(player_ids)
        params = {"ids": player_ids}
        return self._get(request, params)

    def get_season_info(self, season_number: int) -> dict:
        """
        Gets information for the given season number.

        The API zero-indexes the season numbers, so this method does that math before
            submitting the request for user-friendliness.

        Args:
          season_number:

        Returns:
        """
        request = "database/season"
        params = {"number": season_number - 1}
        return self._get(request, params)

    def get_game_by_date(self, season: int, day: int) -> dict:
        """
        Gets the last game update for the requested day and season.

        Completed games will show the final update of the game; currently-running games
            will show the updated present, and future games will show a placeholder
            update if the game is already scheduled.

        Args:
          day:
          season:

        Returns:
        """
        request = "database/games"
        params = {"day": day - 1, "season": season - 1}
        return self._get(request, payload=params)

    def get_game_by_id(self, game_id: str) -> dict:
        """
        Gets the last game update for a game given its ID.

        Completed games will show the final update of the game; currently-running games
            will show the updated present, and future games will show a placeholder
            update if the game is already scheduled.

        Args:
          game_id:
        Returns:
        """
        request = f"database/gameById/{game_id}"
        return self._get(request)

    def get_playoff_details(self, season: int) -> dict:
        """
        Gets details about the playoffs for a given season number.

        The API zero-indexes season numbers, so this method handles that math for
            user-friendliness.

        Args:
          season:
        Returns:
        """
        request = "database/playoffs"
        params = {"number": season - 1}
        return self._get(request, payload=params)

    def get_playoff_round_details(self, round_id: str) -> dict:
        """
        Gets informatino about a specific round in the playoffs given its ID.

        Args:
          round_id
        """
        request = "database/playoffRound"
        params = {"id": round_id}
        return self._get(request, payload=params)

    def get_playoff_matchups(self, matchup_ids: List[str]) -> dict:
        """
        Gets information about one or more playoff matchups given their IDs.

        Returns:
        """
        request = "database/playoffMatchups"
        if isinstance(matchup_ids, list):
            matchup_ids = ",".join(matchup_ids)
        params = {"ids": matchup_ids}
        return self._get(request, params)

    def get_simulation_data(self) -> dict:
        """
        Gets current data about the simulation (day, season, time to next cycle, etc).

        Returns:
          A dict
        """
        request = "database/simulationData"
        return self._get(request)

    def list_idol_leaderboard(self) -> dict:
        """
        Lists the players on the Idol leaderboard.

        Returns:
          A list
        """
        request = "api/getIdols"
        return self._get(request)

    def list_hall_of_flame(self) -> dict:
        """
        Lists players in the hall of flame along with their peanut count.

        Returns:
        """
        request = "api/getTribute"
        return self._get(request)

    # Summaries
    def list_all_divisions(self) -> dict:
        """
        Lists each division and its member teams.

        Returns:
        """
        request = "database/allDivisions"
        return self._get(request)

    def list_all_teams(self):
        """
        Lists all teams.

        Returns:
        """
        request = "database/allTeams"
        return self._get(request)

    def list_global_events(self):
        """
        Lists the messages that make the content of the ticker at the top of the
        window.

        Returns:
        """
        request = "database/globalEvents"
        return self._get(request)

    def get_standings(self, standings_id: str) -> dict:
        """
        Gets information for the requested standings ID from a season object.

        Args:
          standings_id: A string specifying the ID of the standings object
        Returns:
        """
        request = "database/standings"
        params = {"id": standings_id}
        return self._get(request, payload=params)

    def get_tiebreakers(self, tiebreakers_id: str) -> dict:
        """
        Gets information for a tiebreaker.

        Args:
          tiebreakers_id: A string specifying the ID of the tiebreaker object
        Returns:
        """
        request = "database/tiebreakers"
        params = {"id": tiebreakers_id}
        return self._get(request, payload=params)

    # Elections
    def get_blessing_results(self, blessing_ids: List[str]) -> List[dict]:
        """
        Gets the information about one or more blessings.

        Args:
          blessing_ids: A list of strings containing IDs of blessing objects
        Returns:
          A list of dicts containing information about the requested blessings.
        """
        request = "database/bonusResults"
        if isinstance(blessing_ids, list):
            blessing_ids = ",".join(blessing_ids)
        params = {"ids": blessing_ids}
        return self._get(request, payload=params)

    def get_decree_results(self, decree_ids: List[str]) -> List[dict]:
        """
        Gets information about one or more decrees.

        Args:
          decree_ids: A list of strings containing IDs of decree objects
        Returns:
          A list of dicts containing information about the requested decrees.
        """
        request = "database/decreeResults"
        if isinstance(decree_ids, list):
            decree_ids = ",".join(decree_ids)
        params = {"ids": decree_ids}
        return self._get(request, payload=params)

    def get_election_recap(self, season: int) -> dict:
        """
        Gets information about the decrees and blessings passed for a given season.

        The API zero-indexes the season, so this method performs that math for
        user-friendliness.

        Args:
          season: An int specifying the season number
        Returns:
          A dict containing the election results for the requested season.
        """
        request = "database/offseasonRecap"
        params = {"season": season - 1}
        return self._get(request, payload=params)

    def list_election_details(self) -> dict:
        """
        Lists the decrees and blessings for the end of the current season.

        Returns:
          A dict containing decrees and blessings for the current season.
        """
        request = "database/offseasonSetup"
        return self._get(request)

    # Statsheets
    def get_season_statsheets(self, seasons: List[str]) -> dict:
        """
        Gets statsheets for one or more seasons.

        Args:
          seasons: A list of season IDs
        Returns:
          A list of dicts each containing the statsheet for a requested season.
        """
        request = "database/seasonStatSheets"
        params = {"ids": seasons}
        return self._get(request, payload=params)

    def get_game_statsheets(self, games: List[str]) -> dict:
        """
        Gets statsheets for one or more games.

        Args:
          games: A list of game IDs.
        Returns:
          A list of dicts each containing the statsheet for a requested game.
        """
        request = "database/gameStatSheet"
        params = {"ids": games}
        return self._get(request, payload=params)

    def get_team_statsheets(self, teams: List[str]) -> dict:
        """
        Gets statsheets for one or more teams.

        Team statsheets are associated with a particular game, so the statsheets are
            only for that game.

        Args:
          teams: A list of team IDs
        Returns:
          A list of dicts containing the requested teams' statsheets.
        """
        request = "database/teamStatSheets"
        if isinstance(teams, list):
            teams = ",".join(teams)
        params = {"ids": teams}
        return self._get(request, payload=params)

    def get_player_statsheets(self, players: List[str]) -> dict:
        """
        Gets statsheets for one or more players.

        Player statsheets are associated with a particular game, so the statsheets are
            only for that game.

        Args:
          players: A list of player IDs
        Returns:
          A list of dicts containing the requested players' statsheets.
        """
        request = "database/playerSeasonStats"
        params = {"ids": players}
        return self._get(request, payload=params)


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

    def get_player_info(self) -> dict:
        """
        Gets extended info for a given player: name, attributes, ratings, and stars.

        Args:
        Returns
        """
        method = "playerInfo"
        return self._get(method)

    def list_tagged_players(self) -> dict:
        """
        Lists all players with a given modification tag.

        Args:
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
