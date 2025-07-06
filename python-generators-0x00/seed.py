#!/usr/bin/python3
import mysql.connector
import csv
import uuid
from mysql.connector import Error


def connect_db():
    """Connect to MySQL server (not a specific DB yet)"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev DB: {e}")
        return None


def create_table(connection):
    """Create user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,2) NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, filename):
    """Insert data from a CSV file into the user_data table"""
    try:
        cursor = connection.cursor()
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute("""
                    SELECT * FROM user_data WHERE user_id = %s;
                """, (row['user_id'],))
                exists = cursor.fetchone()
                if not exists:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s);
                    """, (row['user_id'], row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file '{filename}' not found.")
