from src.item import Item

def test_item_creation():
    item = Item("123", "The Lord of the Rings", "book")
    assert item.item_id == "123"
    assert item.title == "The Lord of the Rings"
    assert item.item_type == "book"
    assert item.status == "available"
    assert item.due_date is None

def test_item_borrowing():
    item = Item("123", "The Lord of the Rings", "book")
    item.borrow("2024-01-01")
    assert item.status == "borrowed"
    assert item.due_date == "2024-01-01"

def test_item_returning():
    item = Item("123", "The Lord of the Rings", "book")
    item.borrow("2024-01-01")
    item.return_item()
    assert item.status == "available"
    assert item.due_date is None