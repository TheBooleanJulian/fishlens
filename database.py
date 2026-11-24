# ============================================================
# FILE: database.py
# LESSON: Saving data so it survives after your program closes
# ============================================================
#
# Normally, variables disappear when your program ends.
# A DATABASE saves data permanently in a file on your computer.
#
# We use SQLite — it comes built into Python, no installation
# needed, and stores everything in one file: fish_data.db
#
# Think of a database like a spreadsheet:
#   TABLE  = a spreadsheet tab
#   ROW    = one line of data
#   COLUMN = one field (e.g. species, confidence)
# ============================================================

import sqlite3   # Built into Python — handles our database file

# The name of our database file.
# It will be created automatically the first time we run.
DATABASE_FILE = "fish_data.db"


def setup_database():
    """Create the database file and table if they don't exist yet."""

    # sqlite3.connect() opens the file — or creates it if it's new
    connection = sqlite3.connect(DATABASE_FILE)

    # A cursor is our "pen" for sending commands to the database
    cursor = connection.cursor()

    # CREATE TABLE IF NOT EXISTS means:
    #   "Make this table only if it doesn't already exist."
    #   Safe to call every time the program starts.
    #
    # Each line inside () defines one column and its data type:
    #   INTEGER = whole numbers (1, 2, 100)
    #   TEXT    = words and sentences
    #   REAL    = decimal numbers (0.95, 3.14)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sightings (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            filename   TEXT,
            species    TEXT,
            confidence REAL,
            scanned_at TEXT
        )
    """)

    # commit() saves changes permanently to the file
    connection.commit()
    connection.close()


def save_sighting(filename, species, confidence, scanned_at):
    """
    Save one fish sighting to the database.

    Parameters:
        filename   - the image file name, e.g. "nemo.jpg"
        species    - the fish species, e.g. "Clownfish"
        confidence - how sure the AI was, e.g. 0.95
        scanned_at - date and time as a string
    """
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # INSERT INTO adds a new row to the table.
    #
    # IMPORTANT: We use ? as placeholders — never build the
    # SQL string using f-strings or + with user data.
    # Doing so opens a security hole called SQL injection.
    # The ? approach is safe because SQLite handles the escaping.
    cursor.execute(
        "INSERT INTO sightings (filename, species, confidence, scanned_at) VALUES (?, ?, ?, ?)",
        (filename, species, confidence, scanned_at)
    )

    connection.commit()
    connection.close()


def get_all_sightings():
    """
    Read every saved sighting from the database.

    Returns a list of tuples, where each tuple is one row:
        (filename, species, confidence, scanned_at)
    """
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # SELECT retrieves rows from a table.
    # ORDER BY scanned_at DESC = newest first
    cursor.execute(
        "SELECT filename, species, confidence, scanned_at FROM sightings ORDER BY scanned_at DESC"
    )

    # fetchall() returns ALL matching rows as a list of tuples
    rows = cursor.fetchall()
    connection.close()

    return rows


def get_species_counts():
    """
    Count how many times each species appears.

    Returns a list of tuples like:
        [("Clownfish", 5), ("Blue Tang", 3), ("Pufferfish", 1)]
    """
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # GROUP BY groups rows with the same species together.
    # COUNT(*) counts how many rows are in each group.
    cursor.execute(
        "SELECT species, COUNT(*) FROM sightings GROUP BY species ORDER BY COUNT(*) DESC"
    )

    rows = cursor.fetchall()
    connection.close()

    return rows
