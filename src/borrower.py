class Borrower:
    """Represents a library user."""

    def __init__(self, borrower_id, name):
        """
        Initialize a borrower.

        Args:
            borrower_id (str): Unique ID.
            name (str): User's name.
        """
        self.borrower_id = borrower_id
        self.name = name
        self.borrowed_items = []

    def __str__(self):
        """Return string info."""
        return f"{self.name} (ID: {self.borrower_id})"

    def borrow_item(self, item):
        """Add item to borrowed list."""
        self.borrowed_items.append(item)

    def return_item(self, item):
        """Remove item from borrowed list."""
        if item in self.borrowed_items:
            self.borrowed_items.remove(item)

    def get_borrowed_items(self):
        """Return list of borrowed items."""
        return self.borrowed_items