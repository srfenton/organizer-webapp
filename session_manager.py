import random
import string
import sqlite3

# Keep the connection open for the entire process
connection = sqlite3.connect("daily_list.db")

def random_id():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=16))

def validate_session(session_id, user_id):
    # Connect to the database
    cursor = connection.cursor()

    # Check if the session ID exists in the sessions table
    cursor.execute('SELECT * FROM sessions WHERE session_id = ? and user_id = ?', (session_id, user_id))
    session = cursor.fetchone()

    # Don't close the connection here. Let the caller manage it.
    if session:
        print('session ok')
        return session  # Return session details (or user ID if necessary)
    else:
        print('session invalid')
        return None  # Invalid session


# Testing functions
def test_random_id():
    print("Testing random_id...")
    session_id = random_id()
    assert len(session_id) == 16
    assert session_id.isalnum()

def test_validate_session_valid():
    print("Testing validate_session with valid ID...")
    # Add a test session to the database
    test_id = random_id()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO sessions (user_id, session_id) VALUES (3, ?)", (test_id,))
    connection.commit()

    session = validate_session(test_id, 3)
    assert session is not None
    assert session[2] == test_id  # session_id is the 3rd field

    # Clean up: Remove the test session after the test
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (test_id,))
    connection.commit()

def test_validate_session_invalid():
    print("Testing validate_session with invalid ID...")
    session = validate_session("invalidsessionid12345678", 3)
    assert session is None

if __name__ == "__main__":
    test_random_id()
    test_validate_session_valid()
    test_validate_session_invalid()
    print("Done.")
