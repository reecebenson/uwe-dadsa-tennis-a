# DADSA - Assignment 1
# Reece Benson
import json
from classes import Player as Player
from classes import Season as Season
from classes import Tournament as Tournament
from classes import Round as Round
from classes import Match as Match

class Handler():
    # Define the variables we will be using
    seasons = { }

    def __init__(self):
        print("HANDLIN FUCK ALL")

    def load_players(self):
        with open('./data/players.json') as tData:
            data = json.load(tData)

            # Players are classed within Seasons
            for season in data:
                # If the season does not yet exist, create it
                if(not season in seasons):
                    seasons[season] = { }

            for gender in data:
                print(gender)
                if(not gender in players):
                    players[gender] = []

                for player in data[gender]:
                    players[gender].append(player)
                    print(player)