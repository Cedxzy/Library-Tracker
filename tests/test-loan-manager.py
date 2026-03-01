import datetime
import pytest
from src.item import Item
from src.borrower import Borrower
from src.loan_manager import LoanManager

def test_add_item(loan_manager, item):
    loan_manager.add_item(item)
    assert item.item_id in loan_manager.items

def test_add_borrower(loan_manager, borrower):
    loan_manager.add_borrower(borrower)
    assert borrower.borrower_id in loan_manager.borrowers

def test_borrow_item(loan_manager, item, borrower):
    loan_manager.add_item(item)
    loan_manager.add_borrower(borrower)
    success = loan_manager.borrow_item(item.item_id, borrower.borrower_id, "2024-01-01")
    assert success
    assert item.status == "borrowed"
    assert item in borrower.get_borrowed_items()

def test_borrow_item_invalid_item_id(loan_manager, borrower):
    loan_manager.add_borrower(borrower)
    success = loan_manager.borrow_item("invalid_id", borrower.borrower_id, "2024-01-01")
    assert not success

def test_borrow_item_invalid_borrower_id(loan_manager, item):
    loan_manager.add_item(item)
    success = loan_manager.borrow_item(item.item_id, "invalid_id", "2024-01-01")
    assert not success

def test_borrow_item_already_borrowed(loan_manager, item, borrower):
    loan_manager.add_item(item)
    loan_manager.add_borrower(borrower)
    loan_manager.borrow_item(item.item_id, borrower.borrower_id, "2024-01-01")
    success = loan_manager.borrow_item(item.item_id, borrower.borrower_id, "2024-01-01")
    assert not success

def test_return_item(loan_manager, item, borrower):
    loan_manager.add_item(item)
    loan_manager.add_borrower(borrower)
    loan_manager.borrow_item(item.item_id, borrower.borrower_id, "2024-01-01")
    success = loan_manager.return_item(item.item_id)
    assert success
    assert item.status == "available"
    assert item not in borrower.get_borrowed_items()

def test_get_overdue_items(loan_manager, item, borrower):
    loan_manager.add_item(item)
    loan_manager.add_borrower(borrower)
    loan_manager.borrow_item(item.item_id, borrower.borrower_id, "2023-01-01")  # Overdue
    overdue_items = loan_manager.get_overdue_items()
    assert item in overdue_items