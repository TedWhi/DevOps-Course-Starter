from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config
from todo_app.data.trello_items import get_items, add_item, get_item, save_item 

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    sorted_items = sorted(items, key = lambda item: item.status, reverse = True)
    return render_template('index.html', items=sorted_items)

@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title')
    add_item(title)

    return redirect('/')

@app.route('/<string:id>/complete/', methods=['POST'])
def complete(id):
    item = get_item(id)
    item.status = "Completed"
    save_item(item)
    
    return redirect('/') 