# File which handles the functionality of the database
from sqlite3 import connect, Connection

class Database:
    """Class which holds all the operations regarding database usage."""

    def __init__(self) -> None:
        self.db = self.connect()
        self.setup()

    def setup(self):
        """Function responsible for setting up the database, and ensuring that everything is in order"""
        self.db.execute("""CREATE TABLE IF NOT EXISTS TrackerTable(
            DATE_ID INTERGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            START_DATE TEXT,
            END_DATE TEXT)""")
        self.db.commit()

    def connect(self) -> Connection:
        """Establishes a connection with the database"""
        return connect("trackerdata.sqlite3")

    def query_all_data(self) -> list:
        """Function that queries the database for all entries, and returns all."""
        cursor = self.db.execute("SELECT * FROM TrackerTable")
        rows = cursor.fetchall()
        return rows

    def commit_and_close(self):
        """Commits all changes and closes the connection to the database"""
        self.db.commit()
        self.close()

    def close(self):
        """Closes the connection to the database"""
        self.db.close()