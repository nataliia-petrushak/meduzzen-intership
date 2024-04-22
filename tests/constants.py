from app.schemas.users import UserSignUp, UserUpdate
from app.db.alembic.repos.user_repo import UserRepository


payload = [
    {"username": "test_1", "password": "<PASSWORD>", "email": "test_1@test.com"},
    {"username": "test_2", "password": "<PASSWORD>", "email": "test_2@test.com"},
    {"username": "test_3", "password": "<PASSWORD>", "email": "test_3@test.com"},
]

user_bad_data = {
    "name": "test_user",
    "email": "test",
    "password": "test_password",
}


user_signup_data = {
    "username": "test_user",
    "email": "test@example.com",
    "password": "test_password",
}


user_update_data = {
    "username": "Updated",
    "email": "user@user.com",
    "password": "<PASSWORD>",
}

pydentic_create_data = UserSignUp(
    username="Afanasiy", email="email@email.com", password="1234567"
)

pydentic_update_data = UserUpdate(
    username="Bruno", email="email@bruno.com", password="<PASSWORD>"
)

user_repo = UserRepository()
