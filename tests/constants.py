from app.db.alembic.repos.company_repo import CompanyRepository
from app.schemas.users import UserSignUp, UserUpdate
from app.db.alembic.repos.user_repo import UserRepository


user_payload = [
    {
        "username": "owner",
        "password": "string",
        "email": "owner@test.com",
        "is_active": True,
    },
    {
        "username": "test_1",
        "password": "$2b$12$J/goObyrDDIHS0rYyuyHvOKKAdTbaPE5W9zPbY0fH7sFM87/kjOuy",
        "email": "test_1@test.com",
        "is_active": True,
    },
    {
        "username": "test_2",
        "password": "string",
        "email": "test_2@test.com",
        "is_active": True,
    },
    {
        "username": "test_3",
        "password": "string",
        "email": "test_3@test.com",
        "is_active": True,
    },
    {
        "username": "test_4",
        "password": "string",
        "email": "test_4@test.com",
        "is_active": True,
    },
]
company_payload = [
    {"name": "test_1", "description": "", "is_hidden": False},
    {"name": "test_2", "description": "", "is_hidden": False},
    {"name": "test_3", "description": "", "is_hidden": False},
]

quiz_payload = [
    {
        "name": "test_1",
        "description": "",
        "questions": [
            {"answers": ["", ""]},
            {"answers": ["", ""]},
            {"answers": ["", ""]},
        ],
    },
    {
        "name": "test_1",
        "description": "",
        "questions": [
            {"answers": ["", ""]},
            {"answers": ["", ""]},
            {"answers": ["", ""]},
        ],
    },
    {
        "name": "test_1",
        "description": "",
        "questions": [
            {"answers": ["", ""]},
            {"answers": ["", ""]},
            {"answers": ["", ""]},
        ],
    },
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
    "password": "<PASSWORD>",
}
company_update_data = {"name": "Updated", "description": "", "is_hidden": True}

pydentic_create_data = UserSignUp(
    username="Afanasiy", email="email@email.com", password="1234567"
)

pydentic_update_data = UserUpdate(username="Bruno", password="<PASSWORD>")

user_repo = UserRepository()
company_repo = CompanyRepository()

company_data = {"name": "Test", "description": "", "is_hidden": False}
quiz_data = {
    "name": "Test",
    "description": "",
    "questions": [
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]}],
}
quiz_update_data = {
    "name": "Test1",
    "description": "1",
    "questions": [
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]}
    ],
}
quiz_data_1_question = {
    "name": "Test",
    "description": "",
    "questions": [{"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]}],
}
quiz_data_1_answer = {
    "name": "Test",
    "description": "",
    "questions": [
        {"question": "1", "variants": ["1"], "answers": ["1"]},
        {"question": "1", "variants": ["1"], "answers": ["1"]},
        {"question": "1", "variants": ["1"], "answers": ["1"]}
    ],
}
