# Folder where all the mechanics for the program will be handled.
from datetime import date
from os import system, get_terminal_size
from pyinputplus import inputDate, inputNum


def divider():
    """Function that prints out a dividing line"""
    print("-".center(get_terminal_size().columns, "-"))

class Menu:
    """Class responsible for the menu interface that will be provided for users"""

    def __init__(self) -> None:
        self.rh = RequestHandler()

    menu_dict = {
        1: "Predict", 
        2: "Add Period",
        3: "View"
    }

    menu_to_descriptions = {
        "Predict": "Makes a prediction based on previous data as to when the next period may be",
        "Add Period": "Add a start and end date (duration) of a cycle.",
        "View": "View all cycle dates that I know."
    }

    def menu(self):
        # Function which will have the menu
        system("CLS")
        divider()
        # Formats the key-value pairs in a more readable format
        # Adds an integer (starting from 1) in front of for all of the now formatted pairs
        options = [f"{i}){k} - {v}" for i, (k, v) in enumerate(self.menu_to_descriptions.items())]
        # Joins the list of formatted pairs onto new lines
        options_msg = "\n".join(options)
        # Sets the prompt
        prompt = f"Hey. What would you like to do?\n{options_msg}\n:"
        # Prompts for input
        response = inputNum(prompt, min=1, max=len(self.menu_to_descriptions))
        divider()
        self.rh.handle(self.menu_dict[int(response)])
        

class RequestHandler:
    """Class responsible for handling and organising user input and program responses"""

    def __init__(self) -> None:
        pass

    def handle(self, request:str):
        """Main function. Accepts a task from the user, determines what the task is, and executes the correct function."""

        if request == "Predict":
            # Function for making predictions
            pass 
        elif request == "Add Period":
            # Function to add a starting date
            pass 
        else:
            # Function that cleanly exits the program
            pass

class DateHandler:
    """Closs responsible for handling date conversions, and reading date objects"""

    def __init__(self) -> None:
        pass

    def get_date_object(self, dt:str) -> date:
        """Function which receives a given date time string, and creates a date object and returns it"""
        return date.fromisoformat(dt)

    def get_today_date(self) -> date:
        """Function that returns the current date and time as a date object"""
        return date.today()

class Predictor:
    """Class responsible for dealing the 'predictive' part of the program"""
    def __init__(self) -> None:
        pass

    def predict(self):
        pass