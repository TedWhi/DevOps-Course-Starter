import os
import json
import functools

import requests

from todo_app.models.item import Item, Status

class TrelloService():
    
    def __init__(self):
        self.BOARD_ID = os.getenv("TRELLO_BOARD_ID")
        self.TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
        self.TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")
        self.lists = None
    
    @functools.cached_property
    def _lists(self) ->  list[dict]:
        return self._get_lists()
    
    def get_items(self) -> list[Item]:
        """
        Fetches all saved items from trello.

        Returns:
            list: The list of saved items.
        """
        items = []
        for trello_list in self._get_lists():
            list_name = trello_list["name"]

            cards = trello_list['cards']
            items += [Item.from_trello_card_and_list_name(card, list_name) for card in cards]

        return items


    def add_item(self, title: str) -> Item:
        """
        Adds a new item with the specified title to trello.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        to_do_list = [trello_list for trello_list in self._lists if trello_list.get("name") == Status.TODO.value][0]

        url = "https://api.trello.com/1/cards"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'idList': to_do_list["id"],
            'name': title,
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_API_TOKEN
        }

        response = requests.post(
            url,
            headers=headers,
            params=query
        )

        return Item.from_trello_card_and_list_name(response.json(), to_do_list["name"])

    def get_item(self, id: str) -> Item:
        """
        Fetches the saved item with the specified ID from trello.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item.id == id), None)

    def save_item(self, item: Item):
        """
        Updates an existing item in trello. If no existing item matches the ID of the specified item, nothing is saved.

        Args:
            item: The item to save.
        """
        updated_list_id = [trello_list for trello_list in self._lists if trello_list.get("name") == item.status.value][0]['id']
        
        url = f"https://api.trello.com/1/cards/{item.id}"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_API_TOKEN,
            'name': item.name,
            'idList': updated_list_id
        }

        requests.put(
            url,
            headers=headers,
            params=query
        )
        
        return item


    def _get_lists(self) -> list[dict]:
        url = f"https://api.trello.com/1/boards/{self.BOARD_ID}/lists"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_API_TOKEN,
            'fields': 'name',
            'cards': 'open',
            'card_fields': 'id,name'
        }

        response = requests.get(
            url,
            headers=headers,
            params=query
        )

        return response.json()
