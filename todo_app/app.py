from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config
from todo_app.data.trello_items import TrelloService
from todo_app.view_model import ViewModel

app = Flask(__name__)
app.config.from_object(Config())
trello_service = TrelloService()


@app.route('/')
def index():
    items = trello_service.get_items()
    sorted_items = sorted(items, key = lambda item: item.status, reverse = True)
    item_view_model = ViewModel(sorted_items)
    return render_template('index.html', view_model=item_view_model)

@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title')
    trello_service.add_item(title)

    return redirect('/')

@app.route('/<string:id>/complete/', methods=['POST'])
def complete(id):
    item = trello_service.get_item(id)
    item.status = trello_service.COMPLETED_LIST_NAME
    trello_service.save_item(item)
    
    return redirect('/') 