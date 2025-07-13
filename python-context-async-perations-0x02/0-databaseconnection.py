#!/usr/bin/env python3
"""
0-databaseconnection.py
Custom context manager for handling SQLite connections.
"""

import sqlite3
from typing import Optional, Type


class DatabaseConnection:
    """Context manager that opens and closes an SQLite connection."""

    def __init__(self, db_path: str = "users.db") -> None:
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    # Enter-method: open the connection and return it
    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    # Exit-method: commit or roll back, then close connection
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb,
    ) -> bool:
        if self.conn is None:  # Safety check
            return False
        try:
            # If an exception occurred, roll back; otherwise commit.
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
        finally:
            self.conn.close()
        # Returning False lets any exception propagate after cleanup
        return False


# Example usage
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
