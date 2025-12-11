"""
Add test book and verify borrow/return functionality
"""
from services.library_service import LibraryService
from daos.loan_dao import LoanDAO
from daos.book_dao import BookDAO

def test_complete_flow():
    print("=" * 60)
    print("COMPLETE BORROW/RETURN TEST")
    print("=" * 60)
    
    library_service = LibraryService()
    loan_dao = LoanDAO()
    book_dao = BookDAO()
    
    # Test user (john with id=4)
    test_user_id = 4
    
    # Step 1: Add a test book
    print("\n[1] Adding test book...")
    test_book_id = library_service.add_book("Test Book for Loans", "Test Author", "TEST123", 5)
    if test_book_id:
        print(f"    SUCCESS: Book added with ID {test_book_id}")
    else:
        print("    ERROR: Failed to add book")
        return
    
    # Step 2: Verify book was added
    book = book_dao.get_book_by_id(test_book_id)
    print(f"    Book: {book[1]}, Available: {book[4]}/{book[5]}")
    
    # Step 3: Check initial loan count
    loans_before = loan_dao.get_active_loans_by_user(test_user_id)
    print(f"\n[2] Initial active loans: {len(loans_before)}")
    
    # Step 4: Borrow the book
    print("\n[3] Borrowing book...")
    success, message = library_service.borrow_book(test_user_id, test_book_id)
    print(f"    Result: {message}")
    
    if not success:
        print("    ERROR: Borrow failed!")
        return
    
    # Step 5: Verify loan was created
    loans_after_borrow = loan_dao.get_active_loans_by_user(test_user_id)
    print(f"\n[4] Active loans after borrow: {len(loans_after_borrow)}")
    
    if len(loans_after_borrow) > len(loans_before):
        print("    SUCCESS: Loan record created in database!")
        loan_details = loans_after_borrow[-1]
        print(f"    Loan ID: {loan_details[0]}, Book: {loan_details[1]}")
        print(f"    Borrowed: {loan_details[2]}, Due: {loan_details[3]}")
    else:
        print("    ERROR: Loan record NOT found in database!")
        print("    This means the INSERT was not committed!")
        return
    
    # Step 6: Verify book availability decreased
    book_after_borrow = book_dao.get_book_by_id(test_book_id)
    print(f"\n[5] Book availability after borrow: {book_after_borrow[4]}/{book_after_borrow[5]}")
    
    if book_after_borrow[4] == book[4] - 1:
        print("    SUCCESS: Book availability decreased correctly!")
    else:
        print("    ERROR: Book availability not updated!")
    
    # Step 7: Return the book
    loan_id = loans_after_borrow[-1][0]
    print(f"\n[6] Returning book (Loan ID: {loan_id})...")
    success_return, message_return = library_service.return_book(loan_id)
    print(f"    Result: {message_return}")
    
    if not success_return:
        print("    ERROR: Return failed!")
        return
    
    # Step 8: Verify loan was marked as returned
    loans_after_return = loan_dao.get_active_loans_by_user(test_user_id)
    print(f"\n[7] Active loans after return: {len(loans_after_return)}")
    
    if len(loans_after_return) < len(loans_after_borrow):
        print("    SUCCESS: Loan marked as returned!")
    else:
        print("    ERROR: Loan still shows as active!")
        return
    
    # Step 9: Verify book availability restored
    book_after_return = book_dao.get_book_by_id(test_book_id)
    print(f"\n[8] Book availability after return: {book_after_return[4]}/{book_after_return[5]}")
    
    if book_after_return[4] == book[4]:
        print("    SUCCESS: Book availability restored!")
    else:
        print("    ERROR: Book availability not restored!")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED - BORROW/RETURN WORKING CORRECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_complete_flow()
