"""
SQL Utilities

Helper functions for executing SQL files and managing database operations.
"""

from pathlib import Path
from snowflake.snowpark import Session


def execute_sql_file(session: Session, sql_file_path: Path) -> None:
    """
    Execute SQL commands from a file.
    
    Args:
        session: Snowflake session object
        sql_file_path: Path to the SQL file to execute
        
    Raises:
        FileNotFoundError: If the SQL file doesn't exist
        Exception: If SQL execution fails
    """
    if not sql_file_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")
    
    sql_content = sql_file_path.read_text()
    
    # Execute the SQL content
    # Note: For files with multiple statements, we execute as a single block
    session.sql(sql_content).collect()


def execute_sql_statements(session: Session, sql_file_path: Path) -> list:
    """
    Execute multiple SQL statements from a file (split by semicolons).
    
    Args:
        session: Snowflake session object
        sql_file_path: Path to the SQL file containing multiple statements
        
    Returns:
        List of results from each statement
        
    Raises:
        FileNotFoundError: If the SQL file doesn't exist
    """
    if not sql_file_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")
    
    sql_content = sql_file_path.read_text()
    
    # Split by semicolons and filter out empty statements
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    
    results = []
    for statement in statements:
        # Skip comment-only lines
        if statement.startswith('--') or not statement:
            continue
        result = session.sql(statement).collect()
        results.append(result)
    
    return results
