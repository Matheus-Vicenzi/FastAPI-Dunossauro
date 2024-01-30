import factory.fuzzy

from fast_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


def test_list_todos(session, client, user, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_list_todo_pagination(session, user, client, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 2


def test_list_todos_filter_title(session, user, client, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_list_todos_filter_description(session, user, token, client):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description='description')
    )
    session.commit()

    response = client.get(
        '/todos/?description=description',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_list_todos_filter_state(session, user, token, client):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state='draft')
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_list_todos_filter_combined(session, user, token, client):
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='description',
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['todos']) == 5


def test_patch_todo_not_found(client, token):
    response = client.patch(
        '/todos/10',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo(session, user, client, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'teste!'},
    )

    assert response.status_code == 200
    assert response.json()['title'] == 'teste!'


def test_delete_todo(session, client, user, token):
    Todo = TodoFactory(user_id=user.id)

    session.add(Todo)
    session.commit()

    response = client.delete(
        f'/todos/{Todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'detail': 'Task has been deleted successfully.'}


def test_delete_todo_not_found(client, token):
    response = client.delete(
        '/todos/10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}
