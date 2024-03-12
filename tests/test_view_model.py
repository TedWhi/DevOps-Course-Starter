from todo_app.view_model import ViewModel
from todo_app.models.item import Item, Status


def test_given_view_model_with_no_items_when_done_items_called_then_an_empty_list_is_returned():
    view_model = ViewModel(items=[])

    done_items = view_model.done_items

    assert done_items == []

def test_given_view_model_with_no_done_items_when_done_items_called_then_an_empty_list_is_returned():
    to_do_item_1 = Item(id="1", name="to do 1", status=Status.TODO)
    to_do_item_2 = Item(id="2", name="to do 2", status=Status.TODO)
    view_model = ViewModel(items=[to_do_item_1, to_do_item_2])

    done_items = view_model.done_items

    assert done_items == []

def test_given_view_model_with_only_done_items_when_done_items_called_then_all_items_returned():
    completed_item_1 = Item(id="1", name="to do 1", status=Status.COMPLETED)
    completed_item_2 = Item(id="2", name="to do 2", status=Status.COMPLETED)
    view_model = ViewModel(items=[completed_item_1, completed_item_2])

    done_items = view_model.done_items

    assert done_items == [completed_item_1, completed_item_2]

def test_given_view_model_with_variety_of_items_when_done_items_called_then_only_done_items_returned():
    to_do_item = Item(id="1", name="to do 1", status=Status.TODO)
    completed_item = Item(id="2", name="to do 2", status=Status.COMPLETED)
    view_model = ViewModel(items=[to_do_item, completed_item])

    done_items = view_model.done_items

    assert done_items == [completed_item]

def test_given_view_model_with_no_items_when_todo_items_called_then_an_empty_list_is_returned():
    view_model = ViewModel(items=[])

    done_items = view_model.todo_items

    assert done_items == []

def test_given_view_model_with_no_todo_items_when_todo_items_called_then_an_empty_list_is_returned():
    completed_item_1 = Item(id="1", name="to do 1", status=Status.COMPLETED)
    completed_item_2 = Item(id="2", name="to do 2", status=Status.COMPLETED)
    view_model = ViewModel(items=[completed_item_1, completed_item_2])

    done_items = view_model.todo_items

    assert done_items == []

def test_given_view_model_with_only_todo_items_when_todo_items_called_then_all_items_returned():
    todo_item_1 = Item(id="1", name="to do 1", status=Status.TODO)
    todo_item_2 = Item(id="2", name="to do 2", status=Status.TODO)
    view_model = ViewModel(items=[todo_item_1, todo_item_2])

    done_items = view_model.todo_items

    assert done_items == [todo_item_1, todo_item_2]

def test_given_view_model_with_variety_of_items_when_todo_items_called_then_only_done_items_returned():
    to_do_item = Item(id="1", name="to do 1", status=Status.TODO)
    completed_item = Item(id="2", name="to do 2", status=Status.COMPLETED)
    view_model = ViewModel(items=[to_do_item, completed_item])

    done_items = view_model.todo_items

    assert done_items == [to_do_item]