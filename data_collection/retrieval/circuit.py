#!/usr/bin/env python3

"""
All related code to fetching VCT stats for a given year.
"""

from datetime import date
from time import sleep

from bs4 import BeautifulSoup, Tag as BSTag
import requests
from tqdm import tqdm

from ..config import VLR_URL, VCT_URL, VLR_EVENT_MATCHES_URL
from ..models import Player, PlayerStats, Team, Match, Agents, Maps
from .write_data import store_tournaments, store_matches, store_teams, store_players

class CircuitScrapper:
    """
    Scrapes for an entire circuit.
    """

    def __init__(self, circuit_path: str):
        self._url: str = VLR_URL + circuit_path
        self._tournament_ids: dict[str, str] = {}
        self._matches: dict[str, Match] = {}
        self._teams: dict[str, Team] = {}
        self._players: dict[str, Player] = {}

    def collect_circuit_data(self):
        """
        """

        self.get_tournaments()
        self.get_matches()

    def _fetch_tournaments(self):
        """
        """

        # fetch and cache tourney ids if empty
        vct_resp = requests.get(self._url, timeout=5.0)
        vct_html = vct_resp.text

        soup = BeautifulSoup(vct_html, 'html.parser')
        event_btns = soup.find_all('a', {'class': 'event-item'})
        event_btns.reverse()
        
        for event_btn in tqdm(event_btns, desc='Fetching Tournaments'):
            event_url = event_btn.get('href')
            i = 7 # get rid of first characters "/event/"
            j = event_url[i:].index('/') + i

            event_name = event_btn.find('div', {'class': 'event-item-title'}).get_text().strip()
            self._tournament_ids[event_url[i:j]] = event_name

    def get_tournaments(self) -> dict[str, str]:
        """
        Get all associated tournaments with circuit
        """
        if not self._tournament_ids:
            self._fetch_tournaments()

        return self._tournament_ids

    def _fetch_matches(self):
        """
        """
        tourn_tqdm = tqdm(self._tournament_ids.items(), desc='Retreiving Matches')
        for tourn_id, tourn_name in tourn_tqdm:
            tourn_tqdm.set_description('Retreiving Matches for {0}'.format(tourn_name))
            tourn_tqdm.refresh()
            self._fetch_matches_from_tournament(tourn_id)
            sleep(3.0)

        match_tqdm = tqdm(self._matches.values(), desc='Retrieve Necesscary Match Info')
        for match in match_tqdm:
            match_tqdm.set_description('Retrieve Match Info for {0}'.format(match.id_num))
            match_tqdm.refresh()
            self._fetch_match_info(match)
            sleep(3.0)

    def get_matches(self) -> list[Match]:
        """
        """
        if not self._matches:
            self._fetch_matches()

        return self._matches

    def _fetch_matches_from_tournament(self, tourn_id: str) -> dict[str, Match]:
        """
        """
        tourn_url = VLR_URL + VLR_EVENT_MATCHES_URL.format(tourn_id)
        tourn_resp = requests.get(tourn_url, timeout=5.0)
        tourn_html = tourn_resp.text

        soup = BeautifulSoup(tourn_html, 'html.parser')
        match_btns = soup.find_all('a', {'class': 'match-item'})

        for match_btn in match_btns:
            match_url = match_btn.get('href')

            # dont include matches that are for fune
            if match_url.find('showmatch') < 0 and match_url.find('match') < 0:
                new_match = Match()
                new_match.event_id = tourn_id

                i = 1 # get rid of first character
                j = match_url[i:].index('/') + i
                new_match.id_num = match_url[i:j]

                if match_btn.find('div', {'class': 'mod-completed'}):
                    new_match.completed = True

                self._matches[new_match.id_num] = new_match

        return self._matches

    def _parse_team_btn(self, team_btn: BSTag) -> str:
        team_url = team_btn.get('href')

        i = 6 # get rid of first characters "/team/"
        j = team_url[i:].index('/') + i
        team_id = team_url[i:j]

        if team_id not in self._teams:
            new_team = Team()
            new_team.id_num = team_id

            new_team.name = team_btn.find('div', {'class': 'wf-title-med'}).get_text().strip()
            self._teams[new_team.id_num] = new_team

        return team_id

    def _parse_game_table(self, table: BSTag) -> dict[str, PlayerStats]:
        """
        """
        stats = {}

        player_rows = table.tbody.find_all('tr')
        for player_row in player_rows:
            new_player = Player()

            # get player id
            player_url = player_row.find('a').get('href')
            i = 8 # get rid of first characters "/player/"
            j = player_url[i:].index('/') + i
            new_player.id_num = player_url[i:j]

            # get player name
            new_player.tag = player_row.find('a').div.get_text().strip()

            # get player agent
            player_agent = Agents[player_row.find('img').get('title').upper()]

            self._players[new_player.id_num] = new_player
            stats[new_player.id_num] = {'agent': player_agent}

        return stats


    def _fetch_match_info(self, match: Match):
        """
        """
        match_url = VLR_URL + '/' + match.id_num
        match_resp = requests.get(match_url, timeout=5.0)
        match_html = match_resp.text

        soup = BeautifulSoup(match_html, 'html.parser')

        # get the major match info
        match_vs = soup.find('div', {'class': 'match-header-vs'})
        team_a_btn, team_b_btn = match_vs.find_all('a', {'class': 'match-header-link'})
        match.team_a_id = self._parse_team_btn(team_a_btn)
        match.team_b_id = self._parse_team_btn(team_b_btn)

        # get the winner and loser of the match
        score_container = soup.find('div', {'class': 'match-header-vs-score'})
        score_values =  score_container.find('div', {'class': 'js-spoiler'})

        if score_values.span['class'][0].find('winer'):
            match.team_winner_id = match.team_a_id
        else:
            match.team_winner_id = match.team_b_id

        # get map stats
        map_stats_containers = soup.find_all('div', {'class': 'vm-stats-game'})

        for map_stats_container in map_stats_containers:
            if map_stats_container.get('data-game-id') == 'all':
                continue

            # get map
            map_name = map_stats_container.find('div', {'class': 'map'}).div.span.contents[0]
            match.maps.append(Maps[map_name.strip().upper()])

            # get stats
            table_a, table_b = map_stats_container.find_all('table')
            player_stats_a = self._parse_game_table(table_a)
            player_stats_b = self._parse_game_table(table_b)
            match.player_stats.append([player_stats_a, player_stats_b])

    def store_data(self, rel_path: str):
        store_tournaments(self._tournament_ids, rel_path=rel_path)
        store_matches(self._matches.values(), rel_path=rel_path)
        store_teams(self._teams.values(), rel_path=rel_path)
        store_players(self._players.values(), rel_path=rel_path)



class VCTScrapper(CircuitScrapper):
    """
    Scrapper and ORM for 
    """

    def __init__(self):
        self.year: int = date.today().year
        super().__init__(VCT_URL.format(self.year))

def _main():
    scrapper = VCTScrapper()
    scrapper.collect_circuit_data()
    scrapper.store_data('vct_' + str(scrapper.year))


if __name__ == '__main__':
    _main()
