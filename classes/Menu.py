# DADSA - Assignment 1
# Reece Benson

import traceback
from functools import partial
from os import system as call
from collections import OrderedDict

class Builder():
    _app = None
    _menu = None
    _tree = None
    _current = None
    _title = None
    _force_close = None

    @staticmethod
    def init(app, title = False):
        # Set our variables
        Builder._app = app
        Builder._menu = { }
        Builder._tree = [ "main" ]
        Builder._current = "main"
        Builder._title = "Please select an option:" if not title else title
        Builder._force_close = False

    @staticmethod
    def close_menu():
        Builder._force_close = True

    @staticmethod
    def add_menu(menu, name, ref):
        # Check if this submenu exists
        if(not menu in Builder._menu):
            Builder._menu[menu] = { }

        # Update our Menu
        Builder._menu[menu].update({ ref: name })

    @staticmethod
    def add_func(name, ref, func):
        Builder._menu[ref] = func

    @staticmethod
    def get_item(ref):
        if(not ref in Builder._menu):
            return None
        else:
            return Builder._menu[ref]
        return None

    @staticmethod
    def call_func(ref):
        if(Builder.is_func(ref)):
            Builder.get_item(ref)()
        else:
            return None

    @staticmethod
    def is_func(ref):
        return callable(Builder.get_item(ref))

    @staticmethod
    def item_exists(ref):
        return (ref in Builder._menu)

    @staticmethod
    def is_menu(ref):
        is_a_menu = True
        
        # Check if the "menu" exists
        if(not ref in Builder._menu):
            is_a_menu = False

        # Check if the menu is a dictionary
        if(type(Builder.get_item(ref)) != dict):
            is_a_menu = False

        return is_a_menu

    @staticmethod
    def notAvailable(text):
        return text + " (Not Available)"

    @staticmethod
    def find_menu(index):
        # Get our current menu to check the items for
        cur_menu_items = Builder.get_item(Builder.current_menu())

        # Check that our menu exists
        if(cur_menu_items == None):
            print("There was an error with grabbing the selected menu!")
            Builder.set_current_menu("main")
            return False
        else:
            # Iterate through our items to find our index
            for i, (k, v) in enumerate(cur_menu_items.items(), 1):
                if(index == i):
                    return { "menu": Builder.is_menu(k), "ref": k, "name": v }

            # Return Data
            return False

        # Fall back returning statement
        return False

    @staticmethod
    def show():
        print(Builder._menu)

    @staticmethod
    def current_menu():
        return Builder._current

    @staticmethod
    def set_current_menu(new_menu):
        Builder._current = new_menu
        return Builder.current_menu()

    @staticmethod
    def add_menu_tree(ref):
        Builder._tree.append(ref)

    @staticmethod
    def get_menu_tree():
        return "/".join([ m for m in Builder._tree ])

    @staticmethod
    def go_back():
        # Set our flag to true
        Builder.just_called_back = True

        # Pop off the last item of the list
        Builder._tree.pop()

        # Set our current menu to the last element of the list
        Builder._current = Builder._tree[-1]

        # Display our menu
        return Builder.show_current_menu()

    @staticmethod
    def monitor_input():
        # Check if we're force closing the menu
        if(Builder._force_close):
            return

        try:
            # Validate our input
            resp = input("\n>>> ")

            # Validate response
            if(resp.lower() == "exit" or resp.lower() == "quit" or resp.lower() == "x"):
                # Terminate the program after user confirmation
                raise KeyboardInterrupt
            elif(resp == ""):
                # Invalid Input from User
                return Builder.show_current_menu(True, True, "You have entered an invalid option")

            # Check that the menu option exists
            try:
                # See if we're trying to go back a page
                if(resp.lower() == "b" and Builder._current is not "main"):
                    return Builder.go_back()

                # Convert our request to an integer
                req = int(resp)

                # Find the requested menu
                req_menu = Builder.find_menu(req)
                if(type(req_menu) == dict):
                    if(req_menu['menu']):
                        # Display our menu
                        Builder.set_current_menu(req_menu['ref'])
                        Builder.add_menu_tree(req_menu['ref'])
                        Builder.show_current_menu()
                    else:
                        # Double check we're executing a function
                        if(Builder.is_func(req_menu['ref'])):
                            # Clear Terminal
                            call("cls")

                            # Print Function Header
                            print("——————————————————————————————————————————————————————————————")

                            # Execute
                            Builder.call_func(req_menu['ref'])

                            # Hold user (to display output from function)
                            input("\n>>> Press <Return> to continue...")

                            return Builder.show_current_menu()
                        else:
                            if(not Builder.item_exists(req_menu['ref'])):
                                return Builder.show_current_menu(True, True, "That option is unavailable")
                            else:
                                if(req_menu['ref'] == "return"):
                                    # User wants to go back to the default menu
                                    input("\nYou are now going to the main menu!\nWarning: If data has not been added, rounds will not exist!")
                else:
                    # Check if we pressed the Back button
                    current_menu = Builder.get_item(Builder._current)
                    if(req == (len(current_menu) + 1) and Builder._current is not "main"):
                        return Builder.go_back()
                    else:
                        return Builder.show_current_menu(True, True, "You have entered an invalid option")
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except ValueError:
                raise ValueError
            except Exception as err:
                raise Exception
        except KeyboardInterrupt:
            # User has terminated the program (Ctrl+C)
            return Builder._app.exit()
        except ValueError:
            # User has entered an invalid value
            return Builder.show_current_menu(True, True, "You have entered an invalid option")
        except Exception as err:
            # input(traceback.print_exc())
            return Builder.show_current_menu(True, True)

    @staticmethod
    def show_current_menu(shouldClear = True, error = False, errorMsg = None):
        cur_menu_items = Builder.get_item(Builder.current_menu())

        # Should we clear our terminal window?
        if(shouldClear):
            call("cls")

        # Have we got an error?
        if(error):
            if(errorMsg == None):
                print("\nError:\nThere was an error performing your request.\n")
            else:
                print("\nError:\n{0}.\n".format(errorMsg))

        # Check that our Menu exists
        if(cur_menu_items == None):
            print("There was an error with grabbing the selected menu!")
            print("Current menu: {}".format(Builder.current_menu()))
            Builder.set_current_menu("main")
        else:
            # Print menu header
            print("{0} ({1})".format(Builder._title, Builder.get_menu_tree()))
            
            # Print out our menu
            for i, (k, v) in enumerate(cur_menu_items.items(), 1):
                if(Builder.item_exists(k)):
                    print("{0}. {1}{2}".format(i, v, (' -> ' if Builder.is_menu(k) else '')))
                else:
                    print(Builder.notAvailable("{0}. {1}{2}".format(i, v, (' -> ' if Builder.is_menu(k) else ''))))

            # Print our back button
            if(Builder.current_menu() is not "main"):
                print("{0}. Back".format(i + 1))

            # Get input from user
            Builder.monitor_input()

class Menu():
    # Define the variables we will be using
    _app = None
    _menu = None
    _current = [ "main" ]
    _current_menu = "main"
    just_called_back = False

    def __init__(self, app):
        # Set our Application
        self._app = app

    def load(self):
        # Create our Menu
        Builder.init(self._app)

        ## MAIN
        Builder.add_menu("main", "Load Season", "load_season")
        Builder.add_menu("main", "See Developer Information", "info")
        Builder.add_menu("main", "See Debug Information", "d_info")
        Builder.add_func("main", "info", lambda: self.dev_info())
        Builder.add_func("main", "d_info", lambda: self.debug_info())

        ## LOAD SEASON
        for season_id in self._app.handler.get_seasons():
            season = self._app.handler.get_season(season_id)

            # Import Season(s) into our menu
            Builder.add_menu("load_season", season.name(), "ls_[{0}]".format(season.name()))

            ## LOAD TOURNAMENT
            for tournament_name in season.tournaments():
                tournament = season.tournament(tournament_name)

                Builder.add_menu("ls_[{0}]".format(season.name()), tournament_name, "ls_[{0}]_[{1}]".format(season.name(), tournament_name))

                # Import Tournament Options
                tournament_option_name = "ls_[{0}]_[{1}]".format(season.name(), tournament_name)
                Builder.add_menu(tournament_option_name, "Emulate Tournament", "{0}_{1}".format(tournament_option_name, "et"))
                Builder.add_menu(tournament_option_name, "Select Round", "{0}_{1}".format(tournament_option_name, "rs"))
                Builder.add_menu(tournament_option_name, "View Difficulty", "{0}_{1}".format(tournament_option_name, "vd"))
                Builder.add_menu(tournament_option_name, "View Prize Money", "{0}_{1}".format(tournament_option_name, "vpm"))
                Builder.add_menu(tournament_option_name, "View Leaderboard", "{0}_{1}".format(tournament_option_name, "vlb"))

                # Import Tournament Functions
                Builder.add_func(tournament_option_name, "{0}_{1}".format(tournament_option_name, "et"), partial(tournament.emulate, season))
                Builder.add_func(tournament_option_name, "{0}_{1}".format(tournament_option_name, "vd"), partial(print, tournament.display("difficulty")))
                Builder.add_func(tournament_option_name, "{0}_{1}".format(tournament_option_name, "vpm"), partial(print, tournament.display("prize_money")))
                Builder.add_func(tournament_option_name, "{0}_{1}".format(tournament_option_name, "vlb"), partial(print, tournament.display("leaderboard")))

                ## LOAD ROUNDS
                for gdr in season.players():
                    Builder.add_menu("{0}_{1}".format(tournament_option_name, "rs"), "{0} Rounds".format(gdr).title(), "{0}_{1}_{2}".format(tournament_option_name, "rs", gdr))

                    ## IMPORT ROUNDS
                    for r in range(1, (season.settings()['round_count'] + 1)):
                        # Find our Round
                        r_str = str(r)
                        r_name = "round_{0}".format(r)
                        r_view_round = "{0}_{1}_{2}".format(tournament_option_name, "vr", gdr+"_"+r_name)
                        rnd = tournament.round(gdr, r_name)

                        # Find our next round if exists
                        nr_name = "round_{0}".format(r + 1)
                        n_rnd = tournament.round(gdr, nr_name)

                        # Build Menu
                        Builder.add_menu("{0}_{1}_{2}".format(tournament_option_name, "rs", gdr), "Round {0}".format(r), r_view_round)

                        # Add Functionality
                        if(rnd == None):
                            Builder.add_menu(r_view_round, "Generate Data", "{0}_{1}_{2}_gen".format(tournament_option_name, "vr", gdr+"_"+r_name))
                            Builder.add_menu(r_view_round, "Input Data", "{0}_{1}_{2}_input".format(tournament_option_name, "vr", gdr+"_"+r_name))

                            # Add Functionality
                            Builder.add_func(r_view_round, "{0}_{1}_{2}_gen".format(tournament_option_name, "vr", gdr+"_"+r_name), partial(print, "gen stuff"))
                            Builder.add_func(r_view_round, "{0}_{1}_{2}_input".format(tournament_option_name, "vr", gdr+"_"+r_name), partial(print, "input stuff"))
                        else:
                            Builder.add_func(r_view_round, r_view_round, partial(tournament.emulate_round, gdr, r_name))

        # Display Menu
        Builder.show_current_menu()

    def debug_info(self):
        try:
            print("What season would you like to debug?")
            for seasonId in self._app.handler.get_seasons():
                season = self._app.handler.get_season(seasonId)
                print("-> {0}".format(season.name()))

            id = input(">>> ") or "season_1"
            if(self._app.handler.get_season(id) != None):
                season = self._app.handler.get_season(seasonId)
                
                #PRINT DEBUG
                print("Name: {0}".format(season.name()))
                print("Tournament Count: {0}".format(len(season.tournaments())))
                print("Tournament Names: {0}".format([ t for t in season.tournaments() ]))
                for tn in season.tournaments():
                    t = season.tournament(tn)
                    print("Gender Count: {0}".format(len(t.rounds())))
                    for g in t.rounds():
                        print("Round Count for {0}: {1}".format(g, len(t.rounds()[g])))
                print("Settings: {0}".format(season._j_data['settings']))

                #ACTIONS
                print("Perform an action:")
                action = input(">>> ")
                if(action == "gen"):
                    self._app.handler.generate_rounds()
                elif(action == "del rounds"):
                    season._rounds = { }
                else:
                    input("\nError:\nAction does not exist.\nPress <Return> to continue...")
            else:
                input("\nError:\nSeason does not exist.\nPress <Return> to continue...")
            
            self.debug_info()
        except Exception as err:
            print(err)
            input("Continue...")
        
    def dev_info(self):
        # Display Developer Information
        print("Python - Design and Analysis of Data Structures and Algorithms")
        print("Assignment 1, due 30th of November 2017")
        print("")
        print("This implementation was developed by Reece Benson")
        print("Student ID: 16021424")
        print("Student Email: Reece2.Benson@live.uwe.ac.uk")
        print("")
        print("The GitHub repository can be found @ http://github.com/reecebenson/DADSA-Tennis (private repo)")
        print("Thanks!")

    def go_back(self):
        # Set our flag to true
        self.just_called_back = True

        # Pop off the last item of the list
        self._current.pop()

        # Set our current menu to the last element of the list
        self._current_menu = self._current[-1]

    def strike(self, text):
        result = ''
        for c in text:
            result = result + c + '\u0336'
        return result

    def display(self, index = None, error = None):
        # Clear our terminal window
        call("cls")

        # Define our variables
        cur_count = 0
        menu_item = self.get_menu(index or "main")

        # Error Handling
        if(error != None):
            print("\n", "Error!", error, "\n")

        # Menu Title, set tree
        print("Please select an option: ({})".format("/".join(self._current)))

        menu_counter = 0
        for m in menu_item:
            # Get our menu name
            menu_name = menu_item[m]

            # Increase our Counter
            menu_counter += 1

            # Check that the menu option is available
            if(m in self._menu):
                # Is the Menu Item a Function?
                m_type = None
                if(callable(self._menu[m])):
                    m_type = ""
                else:
                    m_type = "->"

                # Print our Menu Item
                print("{0}. {1} {2}".format(menu_counter, menu_name, m_type))
            else:
                print(self.strike("{0}. {1} [?]".format(menu_counter, menu_name)))

        # Get User Input
        self.get_input()

    def validate_menu(self, index):
        try:
            menu_name = [ (v) for k,v in enumerate(self._menu) if(k == index) ][0]
            return menu_name
        except IndexError:
            return None

    def get_menu(self, menu_name):
        # Check our Menu exists
        if(not menu_name in self._menu):
            return None
        else:
            return self._menu[menu_name]

    def menu_exists(self, index):
        # Find our indexed menu
        menu_item = self.get_menu(self._current_menu)

        menu_found = None
        menu_counter = 0
        for m in menu_item:
            # Get our menu name
            menu_name = menu_item[m]

            # Increase our Counter
            menu_counter += 1

            # Check that the menu option is available
            if(m in self._menu):
                # Has our menu been found?
                if(menu_counter == index):
                    # Check if it's a function or a submenu
                    if(callable(self._menu[m])):
                        # Call our function
                        menu_found = self._menu[m]
                    else:
                        menu_found = m
            else:
                menu_found = None
        return menu_found

    def get_input(self):
        # Wrap this in a try/except to validate any errors with input
        try:
            # Get users input
            resp = int(input('\n>>> '))

            # Validate some set input calls
            if(resp == "exit"):
                raise KeyboardInterrupt
            elif(resp == ""):
                return self.display(self._current_menu, "Please select a valid option!")
            
            # Validate input from current menu
            menu_selected = self.menu_exists(resp)
            if(menu_selected != None and callable(menu_selected) != True):
                print(menu_selected)
                self._current.append(menu_selected)
                self._current_menu = menu_selected
                self.display(menu_selected)
            elif(callable(menu_selected)):
                # Clear our screen
                call("cls")

                # Call our function
                menu_selected()

                # Hold the user so they can see the result (if back hasn't just been called)
                if(self.just_called_back == False):
                    input(">>> Press <Return> to continue...")
                else:
                    self.just_called_back = False
        
                # Display our menu again to stop from program termination
                self.display(self._current_menu)
            else:
                self.display(self._current_menu, "Please select a valid option!")

        except KeyboardInterrupt:
            self._app.exit()

        except ValueError:
            self.display(self._current_menu, "Please select a valid option!")

