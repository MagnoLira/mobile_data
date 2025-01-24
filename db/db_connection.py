import cx_Oracle
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DBConnection:
    def __init__(self, user, password, dsn):
        self.user = user
        self.password = password
        self.dsn = dsn
        self.connection = None

    def connect(self):
        """Establish a connection to the Oracle database."""
        try:
            self.connection = cx_Oracle.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
            )
            logging.info("Database connection established.")
        except cx_Oracle.DatabaseError as e:
            logging.error(f"Failed to connect to the database: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.connection:
            try:
                self.connection.close()
                logging.info("Database connection closed.")
            except cx_Oracle.DatabaseError as e:
                logging.error(f"Failed to close the database connection: {e}")

    def get_connection(self):
        """Return the active database connection."""
        if not self.connection:
            self.connect()
        return self.connection


