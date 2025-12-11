"""
Test script to verify loan creation and return functionality
"""
from services.library_service import LibraryService
from daos.loan_dao import LoanDAO
from daos.book_dao import BookDAO

def test_borrow_and_return():
    print("=" * 50)
    print("Testing Borrow and Return Functionality")
    print("=" * 50)
    
    library_service = LibraryService()
    loan_dao = LoanDAO()
    book_dao = BookDAO()
    
    # Test user (assuming john with id=4 exists)
    test_user_id = 4
    
    # Get a book to test with
    books = book_dao.get_all_books()
    if not books:
        print("ERROR: No books available for testing")
        return
    
    test_book = books[0]
    book_id = test_book[0]
    book_title = test_book[1]
    available_before = test_book[4]
    
    print(f"\nTest Book: {book_title}")
    print(f"   Available copies before: {available_before}")
    
    # Check loans before
    loans_before = loan_dao.get_active_loans_by_user(test_user_id)
    print(f"\nActive loans before: {len(loans_before)}")
    
    # Test 1: Borrow a book
    print("\nTesting BORROW...")
    success, message = library_service.borrow_book(test_user_id, book_id)
    print(f"   Result: {message}")
    
    if success:
        # Check if loan was created
        loans_after = loan_dao.get_active_loans_by_user(test_user_id)
        print(f"   Active loans after borrow: {len(loans_after)}")
        
        # Check if book availability decreased
        book_after = book_dao.get_book_by_id(book_id)
        available_after = book_after[4]
        print(f"   Available copies after borrow: {available_after}")
        
        if len(loans_after) > len(loans_before):
            print("   SUCCESS: Loan record created!")
        else:
            print("   ERROR: Loan record NOT created!")
            
        if available_after == available_before - 1:
            print("   SUCCESS: Book availability updated!")
        else:
            print("   ERROR: Book availability NOT updated!")
        
        # Test 2: Return the book
        if loans_after:
            loan_id = loans_after[-1][0]  # Get the last loan ID
            print(f"\nTesting RETURN (Loan ID: {loan_id})...")
            success_return, message_return = library_service.return_book(loan_id)
            print(f"   Result: {message_return}")
            
            if success_return:
                # Check if loan was marked as returned
                loans_final = loan_dao.get_active_loans_by_user(test_user_id)
                print(f"   Active loans after return: {len(loans_final)}")
                
                # Check if book availability increased
                book_final = book_dao.get_book_by_id(book_id)
                available_final = book_final[4]
                print(f"   Available copies after return: {available_final}")
                
                if len(loans_final) < len(loans_after):
                    print("   SUCCESS: Loan marked as returned!")
                else:
                    print("   ERROR: Loan NOT marked as returned!")
                    
                if available_final == available_after + 1:
                    print("   SUCCESS: Book availability restored!")
                else:
                    print("   ERROR: Book availability NOT restored!")
    else:
        print(f"   ERROR: Borrow failed: {message}")
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_borrow_and_return()

