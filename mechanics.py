# Folder where all the mechanics for the program will be handled.
from datetime import date

class Menu:
    """Class responsible for the menu interface that will be provided for users"""

    def __init__(self) -> None:
        self.rh = RequestHandler()

    def menu(self):
        # Function which will have the menu
        pass

class RequestHandler:
    """Class responsible for handling and organising user input and program responses"""

    def __init__(self) -> None:
        pass

    def handle(self, request:str):
        """Main function. Accepts a task from the user, determines what the task is, and executes the correct function."""

        if request == "predict":
            # Function for making predictions
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