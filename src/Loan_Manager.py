from datetime import datetime, date
from src.item import Item
from src.borrower import Borrower

class LoanManager:
    """Manages borrowing and returning of items."""

    def __init__(self):
        """Initialize collections."""
        self.items = {}        # item_id -> Item
        self.borrowers = {}    # borrower_id -> Borrower

    def add_item(self, item):
        """Add an item to the collection."""
        self.items[item.item_id] = item

    def add_borrower(self, borrower):
        """Add a borrower."""
        self.borrowers[borrower.borrower_id] = borrower

    def borrow_item(self, item_id, borrower_id, due_date_str):
        """
        Borrow an item if available.

        Args:
            item_id (str): Item to borrow.
            borrower_id (str): Borrower.
            due_date_str (str): Due date in 'YYYY-MM-DD'.

        Returns:
            bool: Success or failure.
        """
        item = self.items.get(item_id)
        borrower = self.borrowers.get(borrower_id)

        if not item or not borrower:
            return False  # invalid IDs

        if item.status == "borrowed":
            return False  # already borrowed

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return False  # invalid date format

        # Update item and borrower
        item.borrow(due_date)
        borrower.borrow_item(item)
        return True

    def return_item(self, item_id):
        """Return an item."""
        item = self.items.get(item_id)
        if not item:
            return False

        # Find the borrower who borrowed this item
        for borrower in self.borrowers.values():
            if item in borrower.get_borrowed_items():
                borrower.return_item(item)
                break

        item.return_item()
        return True

    def get_overdue_items(self):
        """Return list of overdue items."""
        today = date.today()
        overdue_list = []
        for item in self.items.values():
            if item.status == "borrowed" and item.due_date and item.due_date < today:
                overdue_list.append(item)
        return overdue_list