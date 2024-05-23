from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.alembic.repos.quiz_result_repo import QuizResultRepository
from app.db.alembic.repos.request_repo import RequestRepository
from app.schemas.users import UserSignUp, UserUpdate
from app.db.alembic.repos.user_repo import UserRepository


user_payload = [
    {
        "username": "owner",
        "password": "string12",
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
        "password": "string12",
        "email": "test_2@test.com",
        "is_active": True,
    },
    {
        "username": "test_3",
        "password": "string12",
        "email": "test_3@test.com",
        "is_active": True,
    },
    {
        "username": "test_4",
        "password": "string12",
        "email": "test_4@test.com",
        "is_active": True,
    },
]
company_payload = [
    {"name": "test_1", "description": ""},
    {"name": "test_2", "description": ""},
    {"name": "test_3", "description": ""},
]

quiz_payload = [
    {
        "name": "Test_1",
        "description": "",
        "questions": [
            {"question": "1", "variants": ["1", "2"], "answers": ["1"]},
            {"question": "2", "variants": ["1", "2"], "answers": ["2"]},
            {"question": "3", "variants": ["1", "3"], "answers": ["1", "3"]},
        ],
    },
    {
        "name": "Test_2",
        "description": "",
        "questions": [
            {"question": "1", "variants": ["1", "2"], "answers": ["1"]},
            {"question": "2", "variants": ["1", "2"], "answers": ["2"]},
            {"question": "3", "variants": ["1", "3"], "answers": ["1", "3"]},
        ],
    },
    {
        "name": "Test_3",
        "description": "",
        "questions": [
            {"question": "1", "variants": ["1", "2"], "answers": ["1"]},
            {"question": "2", "variants": ["1", "2"], "answers": ["2"]},
            {"question": "3", "variants": ["1", "3"], "answers": ["1", "3"]},
        ],
    },
]


answers = [
    {"question": "1", "answers": ["2"], "is_correct": False},
    {"question": "2", "answers": ["2"], "is_correct": True},
    {"question": "3", "answers": ["3", "1"], "is_correct": True},
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
    username="Afanasiy", email="email@email.com", password="12345678"
)

pydentic_update_data = UserUpdate(username="Bruno", password="<PASSWORD>")

user_repo = UserRepository()
company_repo = CompanyRepository()
quiz_result_repo = QuizResultRepository()
request_repo = RequestRepository()

company_data = {"name": "test_1", "description": ""}
quiz_data = {
    "name": "Test",
    "description": "",
    "questions": [
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
    ],
}
quiz_update_data = {
    "name": "Test1",
    "description": "1",
    "questions": [
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
        {"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]},
    ],
}
quiz_data_1_question = {
    "name": "Test4",
    "description": "",
    "questions": [{"question": "1", "variants": ["1", "1"], "answers": ["1", "1"]}],
}
quiz_data_1_answer = {
    "name": "Test5",
    "description": "",
    "questions": [
        {"question": "1", "variants": ["1"], "answers": ["1"]},
        {"question": "1", "variants": ["1"], "answers": ["1"]},
        {"question": "1", "variants": ["1"], "answers": ["1"]},
    ],
}
