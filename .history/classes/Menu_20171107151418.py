# DADSA - Assignment 1
# Reece Benson

from os import system as call
from collections import OrderedDict

class Menu():
    # Define the variables we will be using
    _app = None
    _menu = None
    _current_menu = 0

    def __init__(self, app):
        # Set our Application
        self._app = app

    def load(self):
        # Define our Menu
        self._menu = { }

        # Create our Menu
        self._menu['main'] = { "new_season": "New Season", "load_season": "Load Season" }
        self._menu['new_season'] = { "ns_players": "Players", "ns_tournaments": "Tournaments", "ns_prizemoney": "Prize Money", "ns_difficulty": "Difficulty" }
        self._menu['load_season'] = { }

        # Append our Seasons to the "Load Season" Menu
        for seasonId in self._app.handler.get_seasons():
            season = self._app.handler.get_season(seasonId)
            self._menu["load_season"].update({ "ls_"+str(seasonId): season.name() })

        # Display our Menu
        self.display()

    def display(self, index = None, error = None):
        # Clear our terminal window
        call("cls")

        # Define our variables
        cur_count = 0
        menu_item = self.get_menu(index or self.get_current_menu_index())

        # Error Handling
        if(error != None):
            print("\n", "Error!", error, "\n")

        # Menu Title, set tree
        print("Please select an option: ({})".format(self.get_menu_name(self.get_current_menu_index())))

        menu_counter = 0
        for m in self._menu[menu_item]:
            # Increase our Counter
            menu_counter += 1

            # Is the Menu Item a Function?
            m_type = None
            if(callable(m)):    m_type = ""
            else:               m_type = "->"

            # Print our Menu Item
            print("{0}. {1} {2}".format(menu_counter, m, m_type))

        # Append the Back Option
        if(self.get_current_menu_index() != 0):
            print("{0}. {1}".format(menu_counter + 1, "Back"))

        # Get User Input
        self.get_input()

    def get_menu(self, menu_name):
        # Check our Menu exists
        if(not menu_name in self._menu):
            return None
        else:
            return self._menu[menu_name]

    def get_input(self):
        # Wrap this in a try/except to validate any errors with input
        try:
            # Get users input
            resp = int(input('>>> '))

            # Validate some set input calls
            if(resp == "exit"):
                raise KeyboardInterrupt
            elif(resp == ""):
                return self.display(None, "Please select a valid option!")
            
            print("got input", resp)

        except KeyboardInterrupt:
            self._app.exit()

        except ValueError:
            self.display(None, "Please select a valid option!")

    def load_action(self, menu_id):
        #TODO: Load Action from Menu_ID
        print("Load Action")