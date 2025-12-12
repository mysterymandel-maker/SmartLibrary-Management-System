from daos.book_dao import BookDAO
from daos.loan_dao import LoanDAO
import datetime

class LibraryService:
    def __init__(self):
        self.book_dao = BookDAO()
        self.loan_dao = LoanDAO()
        self.MAX_LOANS = 3
        self.LOAN_PERIOD_DAYS = 7

    def borrow_book(self, user_id, book_id):
        # 1. Check max loans
        active_loans = self.loan_dao.get_active_loan_count(user_id)
        if active_loans >= self.MAX_LOANS:
            return False, "Max loan limit (3) reached."

        # 2. Check book availability
        book = self.book_dao.get_book_by_id(book_id)
        if not book or book[4] <= 0: # available_copies is index 4
            return False, "Book is not available."

        # 3. Create Loan
        due_date = datetime.date.today() + datetime.timedelta(days=self.LOAN_PERIOD_DAYS)
        self.loan_dao.create_loan(user_id, book_id, due_date)
        
        # 4. Update book copies
        self.book_dao.update_copies(book_id, -1)
        
        return True, "Book borrowed successfully."

    def return_book(self, loan_id):
        loan = self.loan_dao.get_loan_by_id(loan_id)
        if not loan or loan[2] != 'borrowed':
            return False, "Invalid loan or already returned."
            
        self.loan_dao.return_loan(loan_id)
        self.book_dao.update_copies(loan[1], 1) # loan[1] is book_id
        return True, "Book returned successfully."

    def search_books(self, query):
        return self.book_dao.search_books(query)
        
    def get_all_books(self):
        return self.book_dao.get_all_books()
        
    def get_user_loans(self, user_id):
        return self.loan_dao.get_active_loans_by_user(user_id)

    def get_dashboard_stats(self):
        most_borrowed = self.loan_dao.get_most_borrowed_books()
        return {
            "most_borrowed": most_borrowed
        }
    
    def add_book(self, title, author, isbn, count):
        return self.book_dao.add_book(title, author, isbn, count)
    
    def delete_book(self, book_id):
        """Delete a book - only if no active loans exist"""
        # Check if book has active loans
        book = self.book_dao.get_book_by_id(book_id)
        if not book:
            return False, "Book not found."
        
        # Check if there are any active loans for this book
        # We'll check if available_copies equals total_copies (no books borrowed)
        if book[4] < book[5]:  # available < total means some are borrowed
            return False, "Cannot delete book with active loans."
        
        try:
            self.book_dao.delete_book(book_id)
            return True, "Book deleted successfully."
        except Exception as e:
            return False, f"Error deleting book: {str(e)}"
