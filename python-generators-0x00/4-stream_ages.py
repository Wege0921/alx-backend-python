#!/usr/bin/python3
from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields ages of users one by one from the database.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()


def average_age():
    """
    Computes the average age of users using the stream_user_ages generator
    without loading the entire dataset into memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average}")
    else:
        print("No users found.")
