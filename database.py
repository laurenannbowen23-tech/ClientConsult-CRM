# database.py
# This module will handle all database operations.

import sqlite3
from datetime import datetime

def get_db_connection():
    """Creates and returns a database connection."""
    conn = sqlite3.connect("clients.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Creates the clients table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            business_name TEXT,
            business_type TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            needs TEXT,
            status TEXT,
            notes TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    # Create the interactions table as well
    create_interactions_table()

def create_interactions_table():
    """Creates the interactions table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            interaction_date TEXT NOT NULL,
            interaction_type TEXT NOT NULL,
            summary TEXT,
            next_steps TEXT,
            created_at TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def add_interaction(client_id, interaction_date, interaction_type, summary, next_steps=""):
    """Adds a new interaction for a client."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interactions (client_id, interaction_date, interaction_type, summary, next_steps, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (client_id, interaction_date, interaction_type, summary, next_steps, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_interactions(client_id):
    """Retrieves all interactions for a client, ordered by date descending."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM interactions WHERE client_id = ? ORDER BY interaction_date DESC
    """, (client_id,))
    interactions = cursor.fetchall()
    conn.close()
    return interactions

def delete_interaction(interaction_id):
    """Deletes an interaction by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM interactions WHERE id = ?", (interaction_id,))
    conn.commit()
    conn.close()

def add_client(client_data):
    """Adds a new client to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (client_name, business_name, business_type, email, phone, address, needs, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        client_data['client_name'],
        client_data['business_name'],
        client_data['business_type'],
        client_data['email'],
        client_data['phone'],
        client_data['address'],
        client_data['needs'],
        client_data['status'],
        client_data['notes']
    ))
    conn.commit()
    conn.close()

def get_all_clients():
    """Retrieves all clients from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients ORDER BY client_name")
    clients = cursor.fetchall()
    conn.close()
    return clients

def update_client(client_id, client_data):
    """Updates an existing client in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients SET
            client_name = ?,
            business_name = ?,
            business_type = ?,
            email = ?,
            phone = ?,
            address = ?,
            needs = ?,
            status = ?,
            notes = ?
        WHERE id = ?
    """, (
        client_data['client_name'],
        client_data['business_name'],
        client_data['business_type'],
        client_data['email'],
        client_data['phone'],
        client_data['address'],
        client_data['needs'],
        client_data['status'],
        client_data['notes'],
        client_id
    ))
    conn.commit()
    conn.close()

def delete_client(client_id):
    """Deletes a client from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

def search_clients(search_term):
    """Searches for clients by name or business name."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE client_name LIKE ? OR business_name LIKE ?", 
                   ('%' + search_term + '%', '%' + search_term + '%'))
    clients = cursor.fetchall()
    conn.close()
    return clients

def get_client_by_id(client_id):
    """Retrieves a single client by their ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = cursor.fetchone()
    conn.close()
    return client
