import psycopg2
from psycopg2 import pool
import os

# Simple connection pool
# ==========================================
# TODO: USER CONFIGURATION
# UPDATE THESE VALUES TO MATCH YOUR POSTGRESQL INSTALLATION
# ==========================================
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
# The error "password authentication failed" means this password is wrong.
# If you installed Postgres recently, you probably set a password during setup.
# Replace "postgres" below with your actual password.
DB_PASS = os.getenv("DB_PASS", "1234")
# ==========================================

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port="5432",
        database=DB_NAME
    )

    if connection_pool:
        print("Connection pool created successfully")

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error while connecting to PostgreSQL: {error}")
    connection_pool = None

def get_connection():
    if connection_pool:
        return connection_pool.getconn()
    else:
        raise Exception("Connection pool is not initialized.")

def release_connection(conn):
    if connection_pool and conn:
        connection_pool.putconn(conn)
