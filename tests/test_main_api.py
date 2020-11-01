#!/usr/bin/env python3

from json import JSONDecodeError
import pytest
import types

from . import (
    BBAPI,
    BLESSING_IDS,
    DAY,
    DECREE_IDS,
    DIVISION_ID,
    GAME_ID,
    GAME_STATSHEET_IDS,
    LEAGUE_ID,
    PLAYER_IDS,
    PLAYOFF_MATCHUP_IDS,
    PLAYOFF_ROUND_ID,
    SEASON,
    STANDINGS_ID,
    SEASON_STATSHEET_IDS,
    SUBLEAGUE_ID,
    TEAM_ID,
    TIEBREAKER_ID,
)


def test_repr():
    assert repr(BBAPI) == "BlaseballAPI"


def test__get_invalid_request():
    with pytest.raises(JSONDecodeError):
        BBAPI._get("pleebis")


def test__sse():
    r = BBAPI._sse("database/streamData")
    assert isinstance(r, types.GeneratorType)


def test_stream_data_type():
    r = BBAPI.stream_data()
    assert isinstance(r, types.GeneratorType)


def test_get_league_info_type():
    r = BBAPI.get_league_info(LEAGUE_ID)
    assert isinstance(r, dict)


def test_subleague_info_type():
    r = BBAPI.get_subleague_info(SUBLEAGUE_ID)
    assert isinstance(r, dict)


def test_get_division_info_type():
    r = BBAPI.get_division_info(DIVISION_ID)
    assert isinstance(r, dict)


def test_get_team_info_type():
    r = BBAPI.get_team_info(TEAM_ID)
    assert isinstance(r, dict)


def test_get_player_info_single_type():
    r = BBAPI.get_player_info(PLAYER_IDS[0])
    print(r)
    assert isinstance(r, list)


def test_get_player_info_multi_type():
    r = BBAPI.get_player_info(PLAYER_IDS)
    print(r)
    assert isinstance(r, list)


def test_get_season_info_type():
    r = BBAPI.get_season_info(SEASON)
    assert isinstance(r, dict)


def test_get_game_by_date_type():
    r = BBAPI.get_game_by_date(SEASON, DAY)
    assert isinstance(r, list)


def test_get_game_by_id_type():
    r = BBAPI.get_game_by_id(GAME_ID)
    assert isinstance(r, dict)


def test_get_playoff_details_type():
    r = BBAPI.get_playoff_details(SEASON)
    assert isinstance(r, dict)


def test_get_playoff_round_details_type():
    r = BBAPI.get_playoff_round_details(PLAYOFF_ROUND_ID)
    assert isinstance(r, dict)


def test_get_playoff_matchups_single_type():
    r = BBAPI.get_playoff_matchups(PLAYOFF_MATCHUP_IDS[0])
    assert isinstance(r, list)


def test_get_playoff_matchups_multi_type():
    r = BBAPI.get_playoff_matchups(PLAYOFF_MATCHUP_IDS)
    assert isinstance(r, list)


def test_get_simulation_data_type():
    r = BBAPI.get_simulation_data()
    assert isinstance(r, dict)


def test_list_idol_leaderboard_type():
    r = BBAPI.list_idol_leaderboard()
    assert isinstance(r, list)


def test_list_hall_of_flame_type():
    r = BBAPI.list_hall_of_flame()
    assert isinstance(r, list)


def test_list_all_divisions_type():
    r = BBAPI.list_all_divisions()
    assert isinstance(r, list)


def test_list_all_teams_type():
    r = BBAPI.list_all_teams()
    assert isinstance(r, list)


def test_list_global_events_type():
    r = BBAPI.list_global_events()
    assert isinstance(r, list)


def test_get_standings_type():
    r = BBAPI.get_standings(STANDINGS_ID)
    assert isinstance(r, dict)


def test_get_tiebreaker_type():
    r = BBAPI.get_tiebreakers(TIEBREAKER_ID)
    assert isinstance(r, list)


def test_get_blessing_results_single_type():
    r = BBAPI.get_blessing_results(BLESSING_IDS[0])
    assert isinstance(r, list)


def test_get_blessing_results_multi_type():
    r = BBAPI.get_blessing_results(BLESSING_IDS)
    assert isinstance(r, list)


def test_get_decree_results_single_type():
    r = BBAPI.get_decree_results(DECREE_IDS[0])
    assert isinstance(r, list)


def test_get_decree_results_multi_type():
    r = BBAPI.get_decree_results(DECREE_IDS)
    assert isinstance(r, list)


def test_get_election_recap_type():
    r = BBAPI.get_election_recap(SEASON)
    assert isinstance(r, dict)


def test_list_election_details_type():
    r = BBAPI.list_election_details()
    assert isinstance(r, dict)


def test_get_season_statsheets_type():
    r = BBAPI.get_season_statsheets(SEASON_STATSHEET_IDS)
    assert isinstance(r, list)


def test_get_game_statsheets_type():
    r = BBAPI.get_game_statsheets(GAME_STATSHEET_IDS)
    assert isinstance(r, list)


def test_get_team_statsheets_type_single():
    r = BBAPI.get_team_statsheets(TEAM_ID)
    assert isinstance(r, list)


def test_get_team_statsheets_type_multi():
    r = BBAPI.get_team_statsheets(TEAM_ID)
    assert isinstance(r, list)


def test_get_player_statsheets_type_single():
    r = BBAPI.get_player_statsheets(PLAYER_IDS[0])
    assert isinstance(r, list)


def test_get_player_statsheets_type_multi():
    r = BBAPI.get_player_statsheets(PLAYER_IDS)
    assert isinstance(r, list)
