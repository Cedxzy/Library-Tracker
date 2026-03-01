import datetime
from item import Item
from borrower import Borrower

class LoanManager:
    """Manages the borrowing and returning of items."""

    def __init__(self):
        """Initializes the LoanManager."""
        self.items = {}
        self.borrowers = {}

    def add_item(self, item):
        """Adds an item to the items dictionary."""
        self.items[item.item_id] = item

    def add_borrower(self, borrower):
        """Adds a borrower to the borrowers dictionary."""
        self.borrowers[borrower.borrower_id] = borrower

    def borrow_item(self, item_id, borrower_id, due_date_str):
        """Allows a borrower to borrow an item."""
        item = self.items.get(item_id)
        borrower = self.borrowers.get(borrower_id)

        if not item or not borrower:
            return False  # Item or borrower not found

        if item.status == "borrowed":
            return False  # Item already borrowed
        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return False #invalid date format

        item.borrow(due_date)
        borrower.borrow_item(item)
        return True

    def return_item(self, item_id):
        """Allows a borrower to return an item."""
        item = self.items.get(item_id)
        if not item:
            return False

        item.return_item()
        #remove item from borrower's list
        for borrower in self.borrowers.values():
            if item in borrower.borrowed_items:
                borrower.return_item(item)
                break
        return True

    def get_overdue_items(self):
        """Returns a list of overdue items."""
        today = datetime.date.today()
        overdue_items = []
        for item in self.items.values():
            if item.status == "borrowed" and item.due_date < today:
                overdue_items.append(item)
        return overdue_items
