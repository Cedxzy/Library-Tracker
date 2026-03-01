from src.borrower import Borrower
from src.item import Item

def test_borrower_creation():
    borrower = Borrower("456", "John Doe")
    assert borrower.borrower_id == "456"
    assert borrower.name == "John Doe"
    assert borrower.borrowed_items == []

def test_borrower_borrow_item(borrower, item):
    borrower.borrow_item(item)
    assert item in borrower.borrowed_items

def test_borrower_return_item(borrower, item):
    borrower.borrow_item(item)
    borrower.return_item(item)
    assert item not in borrower.borrowed_items

def test_borrower_get_borrowed_items(borrower, item):
    borrower.borrow_item(item)
    borrowed_items = borrower.get_borrowed_items()
    assert item in borrowed_items