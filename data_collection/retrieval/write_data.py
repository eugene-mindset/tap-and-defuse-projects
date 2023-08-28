from csv import writer as csv_writer
from pathlib import Path

from tqdm import tqdm

from ..models import Player, Team, Match, Maps, Agents
from ..config import OUTPUT_DATA_DIR

if not OUTPUT_DATA_DIR.exists():
    OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)

def generate_dir(rel_path='') -> Path:
    out_path = OUTPUT_DATA_DIR / rel_path

    if not out_path.exists():
        out_path.mkdir(parents=True, exist_ok=True)

    return out_path

def store_tournaments(tournaments: dict[str, str], rel_path=''):
    """
    """

    out_path = generate_dir(rel_path)

    with open(out_path / 'tournaments.csv', 'w', newline='', encoding="utf8") as file:
        writer = csv_writer(file)
        writer.writerow(['ID', 'Name'])

        tourn_tqdm = tqdm(
            tournaments.items(),
            desc='Storing Tournament Data to {0}'.format(out_path))

        for id_num, name in tourn_tqdm:
            writer.writerow([id_num, name])

def store_matches(matches: list[Match], rel_path=''):
    """
    """

    out_path = generate_dir(rel_path)

    with open(out_path / 'matches.csv', 'w', newline='', encoding="utf8") as file:
        writer = csv_writer(file)
        writer.writerow(['ID', 'EventID', 'Completed', 'TeamAID', 'TeamBID', 'WinnerID'])

        matches_tqdm = tqdm(matches, desc='Storing Base Match Data to {0}'.format(out_path))

        for match in matches_tqdm:
            writer.writerow([
                match.id_num,
                match.event_id,
                match.completed,
                match.team_a_id,
                match.team_b_id,
                match.team_winner_id])

    map_matches = [(match.id_num, i, map_match)
        for match in matches for i, map_match in enumerate(match.maps)]


    with open(out_path / 'match_maps.csv', 'w', newline='', encoding="utf8") as file:
        writer = csv_writer(file)
        writer.writerow(['ID', 'Order', 'Map'])

        maps_tqdm = tqdm(map_matches, desc='Storing Maps per Match Data to {0}'.format(out_path))

        for id_num, order, map_match in maps_tqdm:
            writer.writerow([id_num, order, str(map_match)[5:]])

    stats_matches = [(match.id_num, i, stats)
        for match in matches for i, stats in enumerate(match.player_stats)]

    with open(out_path / 'stats_maps.csv', 'w', newline='', encoding="utf8") as file:
        writer = csv_writer(file)
        writer.writerow(['ID', 'Order', 'TeamOrder', 'PlayerID', 'Agent'])

        maps_tqdm = tqdm(stats_matches, desc='Storing Stats Per Map Data to {0}'.format(out_path))

        for id_num, order, map_stats in maps_tqdm:
            for i, team in enumerate(map_stats):
                for player_id, stats in team.items():
                    writer.writerow([id_num, order, str(map_match)[5:], i, player_id, str(stats['agent'])[7:]])

def store_teams(teams: list[Team], rel_path=''):
    """
    """

    out_path = generate_dir(rel_path)

    with open(out_path / 'teams.csv', 'w', newline='', encoding="utf8") as file:
        writer = csv_writer(file)
        writer.writerow(['ID', 'Name'])

        teams_tqdm = tqdm(teams, desc='Storing Team Data to {0}'.format(out_path))

        for team in teams_tqdm:
            writer.writerow([team.id_num, team.name])

def store_players(players: list[Player], rel_path=''):
    """
    """

    out_path = generate_dir(rel_path)

    with open(out_path / 'players.csv', 'w', newline='', encoding="utf8") as file:
        writer = csv_writer(file)
        writer.writerow(['ID', 'Tag'])

        players_tqdm = tqdm(players, desc='Storing Player Data to {0}'.format(out_path))

        for player in players_tqdm:
            writer.writerow([player.id_num, player.tag])

def _test():
    test_dir = 'test'
    
    test_match = Match()
    test_match.maps = [Maps.ASCENT, Maps.BIND]
    test_match.player_stats = [
        [{'0001': {'agent': Agents.ASTRA}}, {'0002': {'agent': Agents.BREACH}}],
        [{'0001': {'agent': Agents.BRIMSTONE}}, {'0002': {'agent': Agents.CHAMBER}}]]

    test_match_2 = Match()
    test_match_2.id_num = '000001'
    test_match_2.maps = [Maps.PEARL, Maps.ICEBOX]
    test_match_2.player_stats = [
        [{'0001': {'agent': Agents.JETT}}, {'0002': {'agent': Agents.PHOENIX}}],
        [{'0001': {'agent': Agents.SKYE}}, {'0002': {'agent': Agents.YORU}}]]

    test_team = Team()

    test_player = Player()

    store_tournaments({'1': 'test', '2': 'test2'}, rel_path=test_dir)
    store_matches([test_match, test_match_2], rel_path=test_dir)
    store_teams([test_team], rel_path=test_dir)
    store_players([test_player], rel_path=test_dir)



if __name__ == '__main__':
    _test()
