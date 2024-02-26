import os
import json

import requests

from todo_app.models.item import Item

BOARD_ID = os.getenv("TRELLO_BOARD_ID")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")
TO_DO_LIST_NAME = "To-do"
COMPLETED_LIST_NAME = "Completed"

def get_items() -> list[Item]:
    """
    Fetches all saved items from trello.

    Returns:
        list: The list of saved items.
    """
    items = []
    for trello_list in _get_lists():
        list_name = trello_list["name"]

        cards = trello_list['cards']
        items += [Item.from_trello_card_and_list_name(card, list_name) for card in cards]

    return items


def add_item(title: str) -> Item:
    """
    Adds a new item with the specified title to trello.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    to_do_list = [trello_list for trello_list in _get_lists() if trello_list.get("name") == "To-do"][0]

    url = "https://api.trello.com/1/cards"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'idList': to_do_list["id"],
        'name': title,
        'key': TRELLO_API_KEY,
        'token': TRELLO_API_TOKEN
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query
    )

    return Item.from_trello_card_and_list_name(json.loads(response.text), to_do_list["name"])

def get_item(id: str) -> Item:
    """
    Fetches the saved item with the specified ID from trello.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.id == id), None)

def save_item(item: Item):
    """
    Updates an existing item in trello. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    updated_list_id = [trello_list for trello_list in _get_lists() if trello_list.get("name") == item.status][0]['id']
    
    url = f"https://api.trello.com/1/cards/{item.id}"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_API_TOKEN,
        'name': item.name,
        'idList': updated_list_id
    }

    requests.request(
        "PUT",
        url,
        headers=headers,
        params=query
    )
    
    return item


def _get_lists() -> list[dict]:
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_API_TOKEN,
        'fields': 'name',
        'cards': 'open',
        'card_fields': 'id,name'
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )

    return json.loads(response.text)
