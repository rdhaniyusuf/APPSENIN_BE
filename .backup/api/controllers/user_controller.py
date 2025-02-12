from flask import request, jsonify
from api.services.user_service import UserService

user_service = UserService()

def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = user_service.create_user(username, password)
    return jsonify({'id': user.id, 'username': user.username})

def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = user_service.login_user(username, password)
    if user:
        token = user_service.generate_jwt(user)
        return jsonify({'id': user.id, 'username': user.username, 'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401
