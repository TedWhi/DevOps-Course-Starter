from todo_app.models.item import Item, Status

class ViewModel:
    def __init__(self, items):
        self._items : list[Item] = items
 
    @property
    def items(self):
        return self._items
    
    @property
    def done_items(self):
        return [item for item in self._items if item.status if item.status == Status.COMPLETED]