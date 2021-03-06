import pytest
import pyscopg2


from flasktodo.db import get_db
from flasktodo import db
from flask import g, session


def test_todo_list(client):
    # View the home page and check to see the header and a to-do item
    response = client.get('/')
    assert b'<h1>A simple to-do application</h1>' in response.data
    assert b'clean room' in response.data

    # Mock data should show three to-do items, one of which is complete
    assert response.data.count(b'<li class="">') == 2
    assert response.data.count(b'<li class="completed">') == 1


def test_new_todo(client):
    response = client.post(
        '/',
        data={'task': "tie shoes"}
    )
    assert response.data.count(b'<li class="">') == 3


def test_completed(client):
    response = client.get('/completed')
    assert b'clean room' not in response.data

    assert response.data.count(b'<li class="completed">') == 1

def test_uncompleted(client):
    response = client.get('/uncompleted')
    assert b'clean room' not in response.data

    assert response.data.count(b'<li class="completed">') == 0


def test_marked(client):
    client.post(
        '/1/done',
    )
    response = client.get(
        '/',
    )
    #This checks the number of completed tasks
    assert response.data.count(b'<li class="">') == 1
    assert response.data.count(b'<li class="completed">') == 2


def test_delete(client):
    client.post(
        '/1/delete',
    )
    response = client.get(
        '/',
    )

    assert response.data.count(b'<li class="">') == 1
