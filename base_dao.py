from database.db_connection import get_connection, release_connection
import psycopg2

class BaseDAO:
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        conn = None
        result = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, params)
            
            if fetch_one:
                result = cur.fetchone()
            elif fetch_all:
                result = cur.fetchall()
            
            # CRITICAL FIX: Always commit for INSERT/UPDATE/DELETE queries
            # Even if we're fetching results (e.g., RETURNING clause)
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
            elif not fetch_one and not fetch_all:
                # Commit other non-SELECT queries
                conn.commit()
                
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Database Error: {error}")
            if conn:
                conn.rollback()
            raise error
        finally:
            if conn:
                release_connection(conn)
        return result

