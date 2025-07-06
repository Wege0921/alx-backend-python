#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that yields user_data rows one by one as dictionaries"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',         # 🔁 Replace with your MySQL username
            password='your_mysql_password', # 🔁 Replace with your MySQL password
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error: {e}")
        return
