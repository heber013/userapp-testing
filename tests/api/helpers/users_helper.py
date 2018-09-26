import json


def get_user_from_json(user):
    with open('data/users.json', 'r') as users:
        try:
            return json.loads(users.read())[user]
        except KeyError:
            return json.loads(users.read())['user1']
