from api.models.user_model import User
from api.auth.auth_service import AuthService

class UserService:
    def create_user(self, username, password):
        password_hash = AuthService.hash_password(password)
        new_user = User(username=username, password_hash=password_hash)
        # Add user to the database
        return new_user
    
    def login_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and AuthService.check_password(user.password_hash, password):
            return user
        return None
    
    def generate_jwt(self, user):
        if user and AuthService.generate_jwt(user):
            return AuthService.generate_jwt(user)
        return None