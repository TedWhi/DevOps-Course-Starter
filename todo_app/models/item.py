from enum import Enum

class Status(Enum):
    COMPLETED = "Completed"
    TODO = "To-do"

class Item:
    """
    This class represent
    """
    def __init__(self, id: str, name: str, status: Status = Status.TODO):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card_and_list_name(cls, trello_card: dict, list_name: str):
        """
        Creates an item from a dictionary representing a trello card and list

        Args:
            trello_card: A dictionary representing a Card (as specified by the Trello API).
                         It must contain an id representing the trello id of the card, and 
                         a name.
            list_name: The name of the Trello list the card is contained within.
        """
        return cls(
            id=trello_card['id'],
            name=trello_card['name'],
            status=Status(list_name)
        )