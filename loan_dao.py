from daos.base_dao import BaseDAO
import datetime

class LoanDAO(BaseDAO):
    def create_loan(self, user_id, book_id, due_date):
        query = """
            INSERT INTO loans (user_id, book_id, due_date)
            VALUES (%s, %s, %s) RETURNING id
        """
        result = self.execute_query(query, (user_id, book_id, due_date), fetch_one=True)
        return result[0] if result else None

    def get_active_loans_by_user(self, user_id):
        query = """
            SELECT l.id, b.title, l.borrow_date, l.due_date 
            FROM loans l
            JOIN books b ON l.book_id = b.id
            WHERE l.user_id = %s AND l.status = 'borrowed'
        """
        return self.execute_query(query, (user_id,), fetch_all=True)

    def get_active_loan_count(self, user_id):
        query = "SELECT COUNT(*) FROM loans WHERE user_id = %s AND status = 'borrowed'"
        result = self.execute_query(query, (user_id,), fetch_one=True)
        return result[0] if result else 0

    def return_loan(self, loan_id):
        query = """
            UPDATE loans 
            SET status = 'returned', return_date = CURRENT_DATE 
            WHERE id = %s
        """
        self.execute_query(query, (loan_id,))

    def get_loan_by_id(self, loan_id):
         query = "SELECT user_id, book_id, status FROM loans WHERE id = %s"
         return self.execute_query(query, (loan_id,), fetch_one=True)

    def get_most_borrowed_books(self):
        query = """
            SELECT b.title, COUNT(l.id) as borrow_count
            FROM loans l
            JOIN books b ON l.book_id = b.id
            GROUP BY b.title
            ORDER BY borrow_count DESC
            LIMIT 5
        """
        return self.execute_query(query, fetch_all=True)
