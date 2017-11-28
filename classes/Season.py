# DADSA - Assignment 1
# Reece Benson

import traceback
from classes import Player
from classes import Round
from classes.File import File
from classes.QuickSort import quick_sort as sort
from os import system as call

class Season():
    _app = None
    _j_data = None
    _name = None
    _players = { }
    _tournaments = { }
    _rounds = { }
    _rounds_raw = { }
    _settings = { }

    def __init__(self, _app, name, j_data):
        # Set our application as a variable
        self._app = _app
        
        # Set our Season JSON Data in a variable
        self._j_data = j_data

        # Debug
        if(self._app.debug):
            print("[LOAD]: Loaded Season '{0}'".format(name))

        # Set variables
        self._name = name
        self._settings = j_data['settings'] or None

    def name(self):
        return self._name

    def settings(self):
        return self._settings

    def display(self, detail, extra = None):
        # Set our header text
        ret = "Details about '{0}':".format(self.name()) + "\n"
        ret += "—————————————————————————————————————————————————————————" + "\n"
            
        # What detail are we handling?
        if(detail == "details"):
            # Add details to the return string
            ret += "There have been {0} genders defined within this season".format(len(self.players())) + "\n"
            for gdr in self.players():
                ret += " -> The gender '{0}' has {1} players stored within it:".format(gdr, len(self.players()[gdr])) + "\n"
                ret += " ALL: " + ", ".join([p.name() for p in self.players()[gdr] ]) + "\n"
            
            # Add settings
            ret += "\n" + "Settings for this season:" + "\n"
            for setting in self.settings():
                ret += " -> The setting '{0}' is set to '{1}'".format(setting, self.settings()[setting]) + "\n"

            # Show tournaments
            ret += "\n" + "Tournaments in this season:" + "\n"
            for tournament_name in self.tournaments():
                tournament = self.tournament(tournament_name)
                ret += " -> {0} — Difficulty: {1}".format(tournament_name, tournament.difficulty()) + "\n"
                ret += "    Prize Money:" + "\n"
                ret += "      {0}".format(" — ".join([ "#{0}: £{1:,}".format(i, int(t)) for i, t in enumerate(tournament.prize_money(), 1) ])) + "\n\n"
        elif(detail == "players"):
            if(extra == None):
                ret += "Error! Please define a gender."
            else:
                for i, player in enumerate(self.players()[extra], 1):
                    ret += "{0}. '{1}'\n".format(i, player.name())
        else:
            ret += "An unknown error has been handled..."
        return ret

    def tournaments(self):
        return self._tournaments

    def tournament(self, name):
        if(name in self.tournaments()):
            return self._tournaments[name]
        else:
            return None

    def add_tournament(self, name, tournament):
        # Add our tournament to our list
        self._tournaments.update({ name: tournament })
        
        # Add this tournament to all of our players scores
        for gdr in self.players():
            for p in self.players()[gdr]:
                p._score.update({ name: { } })

        # Debug
        if(self._app.debug):
            print("[LOAD]: Loaded Tournament '{0}' for '{1}'".format(name, self.name()))

        return self.tournament(name)

    def add_gender(self, name, cap):
        # Update Memory
        self._players.update({ name: [ ] })
        self._rounds.update({ name: [ ] })
        self._j_data['settings'].update({ name + "_cap": cap })

        # Update Files
        File.add_gender(self.name(), name, cap)

    def player(self, gender, name):
        if(gender in self.players()):
            for plyr in self.players()[gender]:
                if(plyr.name() == name):
                    return plyr
        return None

    def players(self):
        return self._players

    def add_player(self, name, gender):
        if(not gender in self.players()):
            self._players[gender] = [ ]
            self._rounds[gender] = [ ]

        # Append our Players to their specific gender category
        self._players[gender].append(Player.Player(name, gender, len(self.players()[gender])))

    def overall_view(self):
        # Menu Selection
        available_tournaments = [ tn for tn in self.tournaments() ]
        selected_tournaments = [ ]
        selected_gender = False
        all_selected = False

        # Handling
        error = False
        error_msg = ""

        # Pick gender
        while(not selected_gender):
            # Clear Terminal
            call("cls")

            print("What gender would you like to view?")
            print("{0}".format(", ".join([g for g in self.players()])))
            gender_input = input(">>> ")
            if(gender_input in [ g for g in self.players() ]):
                selected_gender = gender_input

        # Show Options
        while(not all_selected):
            # Clear Terminal
            call("cls")

            # Show Error
            if(error):
                print("\nError:\n{}\n".format(error_msg))
                error = False

            print("Select tournaments you would like to migrate together:")
            for i, tn in enumerate(self.tournaments(), 1):
                if(len(self.tournament(tn).rounds()[gender_input]) == self.settings()["round_count"]):
                    print("{0}. {1} ({2})".format(i, tn, ("Selected" if tn in selected_tournaments else "Not Selected")))
                else:
                    print("{0}. {1} (Not Available, this tournament is incomplete at Round {2})".format(i, tn, len(self.tournament(tn).rounds()[gender_input])))
            print("b. Back")

            # Print Final
            if(len(selected_tournaments) > 0):
                print("\n{0}. View Overall Leaderboard for {1}".format(i + 1, (", ".join(selected_tournaments) if len(selected_tournaments) != 0 else "[None Selected]")))

            # Debug
            resp = input(">>> ")
            if(resp.isdigit()):
                got = int(resp)
                if(got >= 1 and got <= len(self.tournaments()) + (1 if(len(selected_tournaments) > 0) else 0)):
                    # Check if we're trying to view overall
                    if(got == len(available_tournaments) + 1):
                        all_selected = True
                        break
                    else:
                        # Toggle state of selected tournament
                        if(available_tournaments[got-1] in selected_tournaments):
                            del selected_tournaments[selected_tournaments.index(available_tournaments[got-1])]
                        else:
                            selected_tournaments.append(available_tournaments[got-1])
                else:
                    error = True
                    error_msg = "Please input a valid option"
            elif(resp == "b"):
                return "SKIP"
            else:
                error = True
                error_msg = "Please input a valid option"

        # Check if we have selected tournaments
        if(all_selected and len(selected_tournaments) != 0):
            # Clear Terminal
            call("cls")

            # Assign our players temporary "total" values
            for p in self.players()[selected_gender]:
                # This will set (and reset) variables
                p._total_wins = 0
                p._total_prize_money = 0
                p._total_score = 0

            # Process our leaderboard data
            players = [ ]
            for tn in self.tournaments():
                # Debug
                if(self._app.debug):
                    print("Process Tournament: {}".format(tn))

                # Check our tournament is within our selected tournaments
                if(not tn in selected_tournaments):
                    continue

                # Get our tournament
                t = self.tournament(tn)
                t.unique_prize_money()

                # Increase players data
                rnd_final_name = "round_{0}".format(self.settings()["round_count"])
                rnd_final = t.round(selected_gender, rnd_final_name)

                # Debug
                if(self._app.debug):
                    print("Processing '{0}' on {1}".format(rnd_final_name, tn))

                # Sort the players
                srt = sort(self.players()[selected_gender], tn)
                place = 1
                for i in reversed(range(len(srt))):
                    # Increment Score
                    score_increment = (srt[i].score(tn, rnd_final_name) if (srt[i].score(tn, rnd_final_name) != 0) else srt[i].highest_score(tn, False))
                    srt[i]._total_score += score_increment

                    # Increment Prize Money
                    money_increment = t._prize_money_unique[srt[i].wins(tn)]
                    srt[i]._total_prize_money += money_increment
                    
                    # Increment Match Wins
                    wins_increment = srt[i].wins(tn)
                    srt[i]._total_wins += wins_increment

                    if(self._app.debug):
                        print("[{0}] Score [{1} -> {2}] Money [{3} -> {4}] Wins [{5} -> {6}]".format(srt[i].name(), score_increment, srt[i]._total_score, money_increment, srt[i]._total_prize_money, wins_increment, srt[i]._total_wins))
                    place += 1

            # Set our header text
            print("Selected Tournaments: {}".format(", ".join(selected_tournaments)))
            print("—————————————————————————————————————————————————————————")

            # Print our data
            srt_overall = sort(self.players()[selected_gender], tn)
            overall_place = 1
            for i in reversed(range(len(srt_overall))):
                # Print Data
                print("#{0}: {1} — Score: {2:03d} — Wins: {3:03d} — Money: £{4:,}".format(f"{overall_place:02}", srt_overall[i].name(), srt_overall[i]._total_score, srt_overall[i]._total_wins, srt_overall[i]._total_prize_money))
                overall_place += 1
        
        return None