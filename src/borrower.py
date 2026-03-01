class Borrower:
    """This represents the borrower."""

    def __init__(self, borrower_id, name):
        """Initializes a new borrower."""
        self.borrower_id = borrower_id
        self.name = name
        self.borrowed_items = []

    def __str__(self):
        """Returns a string representation of the borrower."""
        return f"{self.name} (ID: {self.borrower_id})"

    def borrow_item(self, item):
        """Adds an item to the borrower's borrowed_items list."""
        self.borrowed_items.append(item)

    def return_item(self, item):
        """Removes an item from the borrower's borrowed_items list."""
        self.borrowed_items.remove(item)

    def get_borrowed_items(self):
        """Returns the list of borrowed items."""
        return self.borrowed_items
