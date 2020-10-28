#!/usr/bin/env python3

import pytest

import requests

from . import (
    BBRAPI,
    # BLESSING_IDS,
    # DAY,
    # DECREE_IDS,
    # DIVISION_ID,
    # GAME_ID,
    # LEAGUE_ID,
    PLAYER_IDS,
    # PLAYOFF_MATCHUP_IDS,
    # PLAYOFF_ROUND_ID,
    SEASON,
    # STANDINGS_ID,
    # SUBLEAGUE_ID,
    # TEAM_ID,
    # TIEBREAKER_ID,
)


def test_repr():
    assert repr(BBRAPI) == "BlaseballReferenceAPI"


def test__get_invalid_request():
    with pytest.raises(requests.exceptions.HTTPError):
        BBRAPI._get("pleebis")


def test_get_raw_data_type():
    r = BBRAPI.get_raw_data(SEASON)
    assert isinstance(r, dict)


####


def test_get_season_leaders_type():
    r = BBRAPI.get_season_leaders(
        SEASON, "batting", "batting_average", order="DESC", limit=25
    )
    assert isinstance(r, list)


def test_get_season_leaders_invalid_category():
    with pytest.raises(ValueError):
        BBRAPI.get_season_leaders(
            SEASON, "pleebis", "batting_average", order="DESC", limit=25
        )


def test_get_season_leaders_invalid_stat():
    with pytest.raises(ValueError):
        BBRAPI.get_season_leaders(
            SEASON, "batting", "pleebis_average", order="DESC", limit=25
        )


def test_get_player_stats_type():
    r = BBRAPI.get_player_stats("batting", PLAYER_IDS)
    assert isinstance(r, list)


def test_get_player_stats_invalid_category():
    with pytest.raises(ValueError):
        BBRAPI.get_player_stats("pleebis", PLAYER_IDS)
