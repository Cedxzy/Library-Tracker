class Item:
    """This represents a library item."""

    def __init__(self, item_id, title, item_type):
        """Initializes a new item."""
        self.item_id = item_id
        self.title = title
        self.item_type = item_type
        self.status = "available"
        self.due_date = None

    def __str__(self):
        """Returns a string representation of the item."""
        return f"{self.title} ({self.item_type}) - Status: {self.status}"

    def borrow(self, due_date):
        """Sets the item's status to 'borrowed' and sets the due date."""
        self.status = "borrowed"
        self.due_date = due_date

    def return_item(self):
        """Sets the item's status to 'available' and resets the due date."""
        self.status = "available"
        self.due_date = None
