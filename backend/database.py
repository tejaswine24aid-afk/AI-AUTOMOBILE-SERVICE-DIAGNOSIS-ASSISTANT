"""
Database module for Automobile Service Diagnosis Assistant.
Manages SQLite database storage for diagnosis history records.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

# Ensure the database directory exists
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "automobile.db")


def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes the database schema if tables do not exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnosis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                vehicle TEXT NOT NULL,
                symptom TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                severity TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_diagnosis(vehicle: str, symptom: str, diagnosis: str, severity: str) -> int:
    """
    Saves a diagnosis record into the SQLite database.
    Returns the newly inserted record ID.
    """
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO diagnosis_history (date, vehicle, symptom, diagnosis, severity)
            VALUES (?, ?, ?, ?, ?)
            """,
            (current_date, vehicle, symptom, diagnosis, severity)
        )
        conn.commit()
        return cursor.lastrowid


def get_history() -> List[Dict[str, Any]]:
    """
    Retrieves all past diagnosis history records ordered by newest first.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, date, vehicle, symptom, diagnosis, severity
            FROM diagnosis_history
            ORDER BY id DESC
            """
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
