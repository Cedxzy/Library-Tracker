from src.item import Item
from src.borrower import Borrower
from src.Loan_Manager import LoanManager
from datetime import date

def main():
    # Initialize the LoanManager
    loan_manager = LoanManager()

    # Create some items
    item1 = Item("001", "The Great Gatsby", "Book")
    item2 = Item("002", "Inception", "DVD")
    item3 = Item("003", "1984", "Book")

    # Add items to LoanManager
    loan_manager.add_item(item1)
    loan_manager.add_item(item2)
    loan_manager.add_item(item3)

    # Create some borrowers
    borrower1 = Borrower("B001", "Alice")
    borrower2 = Borrower("B002", "Bob")

    # Add borrowers to LoanManager
    loan_manager.add_borrower(borrower1)
    loan_manager.add_borrower(borrower2)

    # Borrow an item
    print("Borrowing 'The Great Gatsby' by Alice...")
    success = loan_manager.borrow_item("001", "B001", "2024-12-31")
    if success:
        print("Borrowed successfully!")
    else:
        print("Failed to borrow.")

    # Borrow another item
    print("Borrowing 'Inception' by Bob...")
    success = loan_manager.borrow_item("002", "B002", "2024-12-15")
    if success:
        print("Borrowed successfully!")
    else:
        print("Failed to borrow.")

    # Display items and their status
    print("\nItems in system:")
    for item in [item1, item2, item3]:
        print(item)

    # Display borrowers and their borrowed items
    print("\nBorrowers and their borrowed items:")
    for borrower in [borrower1, borrower2]:
        print(f"\n{borrower}")
        for borrowed_item in borrower.get_borrowed_items():
            print(f" - {borrowed_item}")

    # Return an item
    print("\nReturning 'The Great Gatsby'...")
    success = loan_manager.return_item("001")
    if success:
        print("Returned successfully!")
    else:
        print("Failed to return.")

    # Display items again
    print("\nItems after return:")
    for item in [item1, item2, item3]:
        print(item)

if __name__ == "__main__":
    main()