from daos.base_dao import BaseDAO

class BookDAO(BaseDAO):
    def add_book(self, title, author, isbn, total_copies):
        query = """
            INSERT INTO books (title, author, isbn, available_copies, total_copies)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """
        result = self.execute_query(query, (title, author, isbn, total_copies, total_copies), fetch_one=True)
        return result[0] if result else None

    def get_all_books(self):
        query = "SELECT id, title, author, isbn, available_copies, total_copies FROM books ORDER BY title"
        return self.execute_query(query, fetch_all=True)

    def search_books(self, search_term):
        # Basic search by title or author
        query = """
            SELECT id, title, author, isbn, available_copies, total_copies 
            FROM books 
            WHERE title ILIKE %s OR author ILIKE %s
        """
        like_term = f"%{search_term}%"
        return self.execute_query(query, (like_term, like_term), fetch_all=True)

    def update_copies(self, book_id, delta):
        # Delta can be +1 (return) or -1 (borrow)
        query = "UPDATE books SET available_copies = available_copies + %s WHERE id = %s"
        self.execute_query(query, (delta, book_id))
    
    def get_book_by_id(self, book_id):
        query = "SELECT id, title, author, isbn, available_copies, total_copies FROM books WHERE id = %s"
        return self.execute_query(query, (book_id,), fetch_one=True)
    
    def delete_book(self, book_id):
        """Delete a book from the database"""
        query = "DELETE FROM books WHERE id = %s"
        self.execute_query(query, (book_id,))
        return True
