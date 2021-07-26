# Folder where all the mechanics for the program will be handled.
from datetime import date
from os import system, get_terminal_size
from pyinputplus import inputDate, inputNum, inputYesNo
from database import Database
from time import sleep


def divider(to_center="-", dividend="-"):
    """Function that prints out a dividing line"""
    print(to_center.center(get_terminal_size().columns, dividend))

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

    def main(self):
        """Main function of the Menu class. Contains an infinite loop to be exited by raising KeyboardInterrupt"""
        while True:
            input("Press enter:")
            system("CLS")
            print("Press ctrl + z at any time to quit")
            try:
                self.menu()
            except KeyboardInterrupt:
                print("Bye, was fun having you")
                sleep(1)    
                raise SystemExit

    def menu(self):
        # Function which will have the menu
        divider()
        # Formats the key-value pairs in a more readable format
        # Adds an integer (starting from 1) in front of for all of the now formatted pairs
        options = [f"{i+1}){k} - {v}" for i, (k, v) in enumerate(self.menu_to_descriptions.items())]
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
        self.db = Database()

    def handle(self, request:str):
        """Main function. Accepts a task from the user, determines what the task is, and executes the correct function."""
        print("\n")
        divider(request, "=")
        if request == "Predict":
            # Function for making predictions
            self.handle_predictions()
        elif request == "Add Period":
            # Function to add a Cycle duration
            self.handle_add_period()
        elif request == "View":
            # Function to display all entries nicely formatted
            print(self.handle_view())
            pass
        elif request == "Extra":
            # Function to handle extra information, such as stuff needed to prepare for period. Currently unavailable
            print("Currently unavailable")
            pass
        else:
            # Function that cleanly exits the program
            pass

    def handle_predictions(self):
        """Function that looks at data from the database, analyzes it, find averages, make comparisons, and then returns a guess as to when the next period should be expected."""
        self.db.connect()
        cycles = self.db.query_finished_cycles()
        if not cycles: print("Sorry, you have no previous finished cycles for me to work with."); return False
        if len(cycles) < 2: print("Oh dear, I don't have enough data to work with. I need at least 2 entries"); return False
        predictor = Predictor(cycles)
        predictor.main()


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

        self.db.connect()
        self.db.insert_period_entry(str(start), str(end) if isinstance(end, date) else end)
        self.db.commit_and_close()

        print("Ok, I will remember that.")
        return True

    def handle_view(self) -> bool:
        """Function that displays all recorded cycles."""
        self.db.connect()
        cycles = self.db.query_all_data()
        self.db.close()
        dh = DateHandler()
        if not cycles:
            print("You don't seem to have any cycles registered for me to display.")
            return False
        
        to_send_list = [f"{i}) From {dh.get_format_date(dh.get_date_object(v[1]))} to {dh.get_format_date(dh.get_date_object(v[2]))}" for i, v in enumerate(cycles)]
        return "\n".join(to_send_list)
    
        
        
class DateHandler:
    """Closs responsible for handling date conversions, and reading date objects"""

    def __init__(self) -> None:
        pass

    def get_date_object(self, d:str) -> date:
        """Function which receives a given date string, and creates a date object and returns it"""
        return date.fromisoformat(d)

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

    def add_days(self, do:date, days:int) -> date:
        """Function which accepts a date object, and a number of days, adds the number of days to the date object, and then return the result."""
        to_return = do
        print(days)
        for _ in range(days):
            try:
                to_return = to_return.replace(day=to_return.day + 1)
            except ValueError:
                try:
                    to_return = to_return.replace(month=to_return.month+1, day=1)
                except ValueError:
                    to_return = to_return.replace(year=to_return.year+1, month=1, day=1)
        return to_return

class Predictor:
    """Class responsible for dealing the 'predictive' part of the program"""
    def __init__(self, cycles:list) -> None:
        self.cycles = cycles

    def main(self):
        """Main function of the Predictor class, which runs all of the functions, and analyzes the data"""
        self.get_start_end_date_objects()
        avg_duration = self.get_average_duration(self.get_cycle_durations())
        avg_time_between = self.get_average_time_between(self.get_time_betweens())
        self.predict(avg_time_between, avg_duration)

    def get_start_end_date_objects(self):
        """Function that loops through the list of cycles, and converts the start and end dates to date objects."""

        dh = DateHandler()
        
        self.cycles = [(dh.get_date_object(cycle[1]), dh.get_date_object(cycle[2])) for cycle in self.cycles]

    def get_cycle_durations(self) -> list:
        """Function that loops through the list of cycles, and gets the duration of each cycle via subtraction
        
        Returns a list of tuples, where the first value is it's position, and the second is the number of days"""
        time_deltas =  [do[1] - do[0] for do in self.cycles]
        durations = [(i, v.days) for i, v in enumerate(time_deltas)]
        return durations

    def get_average_duration(self, cycle_durations: list) -> int: 
        """Function that accepts a list of cycle_durations returned from get_cycle_durations, as an argument and calculates and returns the average."""
        times = [val[1] for val in cycle_durations]
        avg = sum(times) // len(times)
        return avg

    def get_time_betweens(self) -> list:
        """Function that calculates the time between the end of one cycle, and the start of the next"""
        time_betweens = []
        # Need to reverse list to get larger dates first
        to_use = sorted(self.cycles, reverse=True)

        for i in range(len(to_use)):
            if i == len(to_use) - 1: break

            time_between = to_use[i][1] - to_use[i+1][0]
            time_betweens.append(time_between.days)   

        return time_betweens

    def get_average_time_between(self, time_betweens:list) -> int:
        """Function that accepts a list of time_betweens, and find the average."""
        return sum(time_betweens) // len(time_betweens)

    def predict(self, avg_time_between:int, avg_duration:int) -> str:
        """Function that accepts the avg time between given dates, and attempts to make a prediction of when the next period may occur"""
        dh = DateHandler()
        last_time = self.cycles[-1]
        divider()
        print(f"The last cycle started on {dh.get_format_date(last_time[0])}, and ended on {dh.get_format_date(last_time[1])}.")
        print(f"Lasting an average duration of {avg_duration} days, I predict, the next cycle will come on the...")
        result = dh.add_days(last_time[1], avg_time_between)
        divider()
        print(f"{dh.get_format_date(result)}")
        
