from datetime import date

class Item:
    """Represents a library item."""

    def __init__(self, item_id, title, item_type):
        """
        Initialize a new Item.

        Args:
            item_id (str): Unique identifier.
            title (str): Item title.
            item_type (str): Type of item (e.g., book, DVD).
        """
        self.item_id = item_id
        self.title = title
        self.item_type = item_type
        self.status = "available"  # default status
        self.due_date = None

    def __str__(self):
        """Return a string description of the item."""
        return f"{self.title} ({self.item_type}) - Status: {self.status}"

    def borrow(self, due_date):
        """
        Mark item as borrowed and set due date.

        Args:
            due_date (date): Due date for returning.
        """
        self.status = "borrowed"
        self.due_date = due_date

    def return_item(self):
        """Mark item as available and reset due date."""
        self.status = "available"
        self.due_date = None