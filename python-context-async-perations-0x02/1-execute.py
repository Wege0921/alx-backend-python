#!/usr/bin/env python3
"""
1-execute.py
Reusable context manager that executes a query with parameters and returns results.
"""

import sqlite3
from typing import Optional, Tuple, List, Type


class ExecuteQuery:
    """Context manager that executes a parameterized SQL query and returns the result."""

    def __init__(self, query: str, params: Tuple = (), db_path: str = "users.db") -> None:
        self.query = query
        self.params = params
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.result: Optional[List[Tuple]] = None

    def __enter__(self) -> List[Tuple]:
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb,
    ) -> bool:
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
        return False  # Let exceptions propagate if any


# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params) as results:
        print(results)
