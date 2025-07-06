#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',          # 🔁 Replace with your MySQL username
            password='your_mysql_password',  # 🔁 Replace with your MySQL password
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error: {e}")
        return

def batch_processing(batch_size):
    """
    Generator that processes each batch of users and prints users over age 25
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
