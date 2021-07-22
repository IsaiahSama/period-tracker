# Folder where all the mechanics for the program will be handled.
from datetime import date
from os import system, get_terminal_size
from pyinputplus import inputDate, inputNum, inputYesNo
from database import Database


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
        3: "View",
        4: "Extra"
    }

    menu_to_descriptions = {
        "Predict": "Makes a prediction based on previous data as to when the next period may be",
        "Add Period": "Add a start and end date (duration) of a cycle.",
        "View": "View all cycle dates that I know.",
        "Extra": "Add extra information"
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

        print(request.center(get_terminal_size().columns, " "))
        if request == "Predict":
            # Function for making predictions
            pass 
        elif request == "Add Period":
            # Function to add a Cycle duration
            self.handle_add_period()
        elif request == "View":
            # Function to display all entries nicely formatted
            self.handle_view()
            pass
        elif request == "Extra":
            # Function to handle extra information, such as stuff needed to prepare for period. Currently unavailable
            pass
        else:
            # Function that cleanly exits the program
            pass

    def handle_view(self) -> bool:
        """Function that displays all recorded cycles."""
        db = Database()
        cycles = db.query_all_data()
        db.close()
        dh = DateHandler()
        if not cycles:
            print("You don't seem to have any cycles registered for me to display.")
            return False
        
        to_send_list = [f"{i}) From {dh.get_format_date(dh.get_date_object(v[1]))} to {dh.get_format_date(dh.get_date_object(v[2]))}" for i, v in cycles]
        del dh, db
        return "\n".join(to_send_list)
    
    def handle_add_period(self):
        """Function that prompts for information to fill in to the period table."""
        print("When did the cycle begin? Enter date in format yyyy/mm/dd")
        start = inputDate(": ")
        print("Is the cycle still going on?")
        resp = inputYesNo(": ")
        if resp == "yes":
            end = "ongoing"
        else:
            print("When did the cycle end? Enter date in format yyyy/mm/dd")
            end = inputDate(": ")

        db = Database()
        dh = DateHandler()
        db.insert_period_entry(dh.get_format_date(start), dh.get_format_date(end) if isinstance(end, date) else end)
        db.commit_and_close()

        print("Ok, I will remember that.")
        return True
        
        
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

    def get_format_date(self, do:date) -> str:
        """Function which accepts a date object as an arguments, and returns a string in the format of:
        WeekDay Month Day Year"
        
        Arguments -> Date Object (do)
        """

        # Step one, get the full string by the ctime method
        # str_date = date.ctime(do)
        # Step two, Replace the 00's and colons with empty spaces
        # purged_date = str_date.replace("00", '').replace(":: ", "")
        # return purged_date
        # OR!!!
        return date.ctime(do).replace("00", "").replace(":: ", "")

class Predictor:
    """Class responsible for dealing the 'predictive' part of the program"""
    def __init__(self) -> None:
        pass

    def predict(self):
        pass