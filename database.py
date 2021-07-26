# File which handles the functionality of the database
from sqlite3 import connect, Connection

class Database:
    """Class which holds all the operations regarding database usage."""

    def __init__(self) -> None:
        self.connect()
        self.setup()

    def setup(self):
        """Function responsible for setting up the database, and ensuring that everything is in order"""
        self.db.execute("""CREATE TABLE IF NOT EXISTS TrackerTable(
            DATE_ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            START_DATE TEXT,
            END_DATE TEXT)""")
        self.db.commit()

    def connect(self) -> Connection:
        """Establishes a connection with the database"""
        self.db = connect("trackerdata.sqlite3")

    def insert_period_entry(self, start_date:str, end_date:str) -> bool:
        """Function which accepts a start and end_date (Or ongoing), and inserts the entry into the database"""
        self.db.execute("INSERT INTO TrackerTable (START_DATE, END_DATE) VALUES (?, ?)", (start_date, end_date))
        return True

    def query_all_data(self) -> list:
        """Function that queries the database for all entries, and returns all."""
        cursor = self.db.execute("SELECT * FROM TrackerTable ORDER BY START_DATE ASC;")
        rows = cursor.fetchall()
        return rows

    def query_finished_cycles(self) -> list:
        """Function that queries the database for all cycles that are NOT ongoing"""
        rows = self.query_all_data()
        return [row for row in rows if row[2] != "ongoing"]

    def commit_and_close(self):
        """Commits all changes and closes the connection to the database"""
        self.db.commit()
        self.close()

    def close(self):
        """Closes the connection to the database"""
        self.db.close()