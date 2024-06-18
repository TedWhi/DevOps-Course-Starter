# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.


### Trello

This app uses the Trello API to track the state of To-Do items. To do this, we must specify a Trello API Key, API token, and Board ID in the `.env` file.

To get a API Key and API token, [sign up to Trello](https://trello.com/signup), [create a free workspace](https://support.atlassian.com/trello/docs/creating-a-new-workspace/), and follow the instructions under "Managing your API Key" and "Authentication and Authorization" on the [Trello API Introduction](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#your-first-api-call).

Once you've done this, create a board for your dev environment To-do list, and get its ID ([see here for instructions](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#your-first-api-call)).

Now you have an API Key, API Token, and your board ID, replace the template values in your `.env` file.

Finally, you should ensure that the values specified in the `Status` enum in `models/item.py` match the names of the lists in your Trello board.

## Running the App locally

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App on a VM using Ansible

To run the To-Do App as a service on a managed node from a control node using Ansible, first, you should set up and copy the necessary files from the `ansible` folder on the control node.

Edit `ansible/inventory` to include the IP address of your managed none, then use the following command to copy the files to your control node.
```sh
scp -r ./ansible <control-node-user>@<control-node-host>:<path-to-directory-you-would-like-to-copy-to>
```

Once this is done, `ssh` into that control node, `cd` to the directory you copied the ansible files to, and run the following command:
```sh
ansible-playbook ansible/playbook.yaml -i ansible/inventory
```

This will then prompt you to enter a Trello API Token, Trello API Key, and Trello Board ID (see the *Trello* section of the README for how to get these values), once these have been enterred, the playbook will run.

When the playbook has completed, you will then be able to access the app at port 5000 on the IP address of your managed node.

## Running the App in a Docker container

The app can be run in both a production and a development docker container.

To run the app in development mode you must build the development image and then spin up a container from it as follows:

```bash
docker build --target development --tag todo-app:dev .
docker run --env-file ./.env -p 5000:5000 --mount "type=bind,source=$(pwd)/todo_app,target=/opt/todo_app/todo_app" --detach todo-app:dev
```

The app can then be accessed at `localhost:5000`.

Note that we pass in the source code as a bind mount. This (alongside enabling `FLASK_DEBUG`, which is done for you in the Dockerfile) means that any source code changes will be picked up by the application and immediately take effect on the application server.

To run the app in production, you must build the production image and spin up the container from it:

```bash
docker build --target production --tag todo-app:prod .
docker run --env-file ./.env -p 5001:5000 todo-app:prod
```
The app can then be accessed at `localhost:5001`.

Changes made to the source code will not affect the production application server.

## Unit Tests

The repo uses [pytest](https://docs.pytest.org/en/8.0.x/) to implement its unit tests. Any new test files added to the `tests`
should mirror the directory structure of the `todo_app` folder. All test files name's must be prefixed with `test`.

To run the unit tests, simply run:
```bash
poetry run pytest
```