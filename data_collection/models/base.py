#!/usr/bin/env python3
"""
"""

from enum import Enum, auto
from typing import TypeAlias, TypedDict

class Regions(Enum):
    """
    """

    NONE = auto()
    AMER = auto()
    EMEA = auto()
    APAC = auto()
    CHIN = auto()
    INTE = auto()


class Maps(Enum):
    """
    """

    ASCENT = auto()
    BREEZE = auto()
    BIND = auto()
    FRACTURE = auto()
    HAVEN = auto()
    ICEBOX = auto()
    LOTUS = auto()
    PEARL = auto()
    SPLIT = auto()
    SUNSET = auto()


class Agents(Enum):
    """
    """

    NONE = auto()
    ASTRA = auto()
    BREACH = auto()
    BRIMSTONE = auto()
    CHAMBER = auto()
    CYPHER = auto()
    DEADLOCK = auto()
    FADE = auto()
    GEKKO = auto()
    HARBOR = auto()
    JETT = auto()
    KAYO = auto()
    KILLJOY = auto()
    NEON = auto()
    OMEN = auto()
    PHOENIX = auto()
    RAZE = auto()
    REYNA = auto()
    SAGE = auto()
    SKYE = auto()
    SOVA = auto()
    VIPER = auto()
    YORU = auto()


AgentPlayRates: TypeAlias = dict[Agents, int]


class Team:
    """
    """

    def __init__(self):
        self.id_num: str = '0000'
        self.region: Regions = Regions.NONE
        self.name: str = "NONE"
        self.acronym: str = "NN"

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Team {0} | {1}'.format(self.id_num, self.name)

class Player:
    """
    """

    def __init__(self):
        self.id_num: str = '00000'
        self.tag: str = "NONE"
        self.full_name: str = "NONE"

    def __str__(self):
        return self.tag

    def __repr__(self):
        return 'Player {0} | {1}'.format(self.id_num, self.tag)


class PlayerStats(TypedDict):
    """
    """

    agent: Agents


class Match:
    """
    """

    def __init__(self, team_a='0000a', team_b='0000b'):
        self.id_num: str = '000000'
        self.event_id: str = '0000'
        self.completed: bool = False

        self.team_a_id: str = team_a
        self.team_b_id: str = team_b
        self.team_winner_id: str = "NONE"

        self.maps: list[Maps] = []
        self.player_stats: list[list[dict[str, PlayerStats]]] = []

    def __str__(self):
        return self.id_num

    def __repr__(self):
        return 'Tournament {0} '.format(self.id_num)
