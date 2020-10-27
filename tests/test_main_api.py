#!/usr/bin/env python3

from . import (
    BBAPI,
    BLESSING_IDS,
    DAY,
    DECREE_IDS,
    DIVISION_ID,
    GAME_ID,
    LEAGUE_ID,
    PLAYER_IDS,
    PLAYOFF_MATCHUP_IDS,
    PLAYOFF_ROUND_ID,
    SEASON,
    STANDINGS_ID,
    SUBLEAGUE_ID,
    TEAM_ID,
    TIEBREAKER_ID,
)


def test_stream_data():
    pass


def test_get_league_info():
    r = BBAPI.get_league_info(LEAGUE_ID)
    assert isinstance(r, dict)


def test_subleague_info():
    r = BBAPI.get_subleague_info(SUBLEAGUE_ID)
    assert isinstance(r, dict)


def test_get_division_info():
    r = BBAPI.get_division_info(DIVISION_ID)
    assert isinstance(r, dict)


def test_get_team_info():
    r = BBAPI.get_team_info(TEAM_ID)
    assert isinstance(r, dict)


def test_get_player_info_single():
    r = BBAPI.get_player_info(PLAYER_IDS[0])
    print(r)
    assert isinstance(r, list)


def test_get_player_info_multi():
    r = BBAPI.get_player_info(PLAYER_IDS)
    print(r)
    assert isinstance(r, list)


def test_get_season_info():
    r = BBAPI.get_season_info(SEASON)
    assert isinstance(r, dict)


def test_get_game_by_date():
    r = BBAPI.get_game_by_date(SEASON, DAY)
    assert isinstance(r, list)


def test_get_game_by_id():
    r = BBAPI.get_game_by_id(GAME_ID)
    assert isinstance(r, dict)


def test_get_playoff_details():
    r = BBAPI.get_playoff_details(SEASON)
    assert isinstance(r, dict)


def test_get_playoff_round_details():
    r = BBAPI.get_playoff_round_details(PLAYOFF_ROUND_ID)
    assert isinstance(r, dict)


def test_get_playoff_matchups_single():
    r = BBAPI.get_playoff_matchups(PLAYOFF_MATCHUP_IDS[0])
    assert isinstance(r, list)


def test_get_playoff_matchups_multi():
    r = BBAPI.get_playoff_matchups(PLAYOFF_MATCHUP_IDS)
    assert isinstance(r, list)


def test_get_simulation_data():
    r = BBAPI.get_simulation_data()
    assert isinstance(r, dict)


def test_list_idol_leaderboard():
    r = BBAPI.list_idol_leaderboard()
    assert isinstance(r, list)


def test_list_hall_of_flame():
    r = BBAPI.list_hall_of_flame()
    assert isinstance(r, list)


def test_list_all_divisions():
    r = BBAPI.list_all_divisions()
    assert isinstance(r, list)


def test_list_all_teams():
    r = BBAPI.list_all_teams()
    assert isinstance(r, list)


def test_list_global_events():
    r = BBAPI.list_global_events()
    assert isinstance(r, list)


def test_get_standings():
    r = BBAPI.get_standings(STANDINGS_ID)
    assert isinstance(r, dict)


def test_get_tiebreaker():
    r = BBAPI.get_tiebreakers(TIEBREAKER_ID)
    assert isinstance(r, list)


def test_get_blessing_results_single():
    r = BBAPI.get_blessing_results(BLESSING_IDS[0])
    assert isinstance(r, list)


def test_get_blessing_results_multi():
    r = BBAPI.get_blessing_results(BLESSING_IDS)
    assert isinstance(r, list)


def test_get_decree_results_single():
    r = BBAPI.get_decree_results(DECREE_IDS[0])
    assert isinstance(r, list)


def test_get_decree_results_multi():
    r = BBAPI.get_decree_results(DECREE_IDS)
    assert isinstance(r, list)


def test_get_election_recap():
    r = BBAPI.get_election_recap(SEASON)
    assert isinstance(r, dict)


def test_list_election_details():
    r = BBAPI.list_election_details()
    assert isinstance(r, dict)
