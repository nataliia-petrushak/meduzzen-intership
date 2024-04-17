import uuid

import pytest
from httpx import AsyncClient
from starlette import status

from schemas.users import UserSignUp, UserUpdate
from services.users import user_services

from tests.conftest import AsyncSessionLocal


class TestUserEndpoints:

    @pytest.fixture
    def user_signup_data(self):
        return {
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password",
        }

    @pytest.fixture
    def user_update_data(self):
        return {
            "username": "Updated",
            "email": "user@user.com",
            "password": "<PASSWORD>",
        }

    @pytest.mark.asyncio(scope="session")
    async def test_create_user_endpoint(
        self, ac: AsyncClient, user_signup_data
    ) -> None:
        response = await ac.post("/users/", json=user_signup_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == user_signup_data["username"]

    @pytest.mark.asyncio(scope="session")
    async def test_can_not_create_user_with_bad_data(
        self, ac: AsyncClient, user_signup_data
    ) -> None:
        response = await ac.post(
            "/users/", json=user_signup_data.update({"name": "Ilona"})
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio(scope="session")
    async def test_get_user_list_endpoint(self, ac: AsyncClient) -> None:
        response = await ac.get("/users/")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio(scope="session")
    async def test_get_user_by_id_endpoint(self, ac: AsyncClient) -> None:
        users = await ac.get("/users/")
        user_id = users.json()[0]["id"]
        response = await ac.get(f"/users/{user_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == user_id

        key_2 = uuid.uuid4()
        response_2 = await ac.get(f"/users/{key_2}/")
        assert response_2.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio(scope="session")
    async def test_update_user_endpoint(
        self, ac: AsyncClient, user_update_data
    ) -> None:
        users = await ac.get("/users/")
        user_id = users.json()[0]["id"]
        response = await ac.patch(f"/users/{user_id}/", json=user_update_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == user_update_data["username"]
        assert response.json()["email"] == user_update_data["email"]

    @pytest.mark.asyncio(scope="session")
    async def test_delete_user_endpoint(self, ac: AsyncClient) -> None:
        users = await ac.get("/users/")
        user_id = users.json()[0]["id"]
        response = await ac.delete(f"/users/{user_id}/")

        assert response.status_code == status.HTTP_200_OK

        response_2 = await ac.get(f"/users/{user_id}/")

        assert response_2.status_code == status.HTTP_404_NOT_FOUND


class TestUserCRUD:
    @pytest.fixture
    def pydentic_create_data(self):
        return UserSignUp(
            username="Afanasiy", email="email@email.com", password="1234567"
        )

    @pytest.fixture
    def pydentic_update_data(self):
        return UserUpdate(
            username="Bruno", email="email@bruno.com", password="<PASSWORD>"
        )

    @pytest.mark.asyncio(scope="function")
    async def test_add_user_func(self, pydentic_create_data):
        async with AsyncSessionLocal() as db:
            result = await user_services.create_model(
                db=db, model_data=pydentic_create_data
            )
            assert result["username"] == pydentic_create_data.username
            assert result["email"] == pydentic_create_data.email

    @pytest.mark.asyncio(scope="function")
    async def test_get_user_list_func(self):
        async with AsyncSessionLocal() as db:
            await user_services.create_model(
                db=db,
                model_data=UserSignUp(
                    username="Test", email="user1@user.com", password="123"
                ),
            )
            await user_services.create_model(
                db=db,
                model_data=UserSignUp(
                    username="Test1", email="user2@user.com", password="123"
                ),
            )
            await user_services.create_model(
                db=db,
                model_data=UserSignUp(
                    username="Test2", email="user3@user.com", password="123"
                ),
            )

            result = await user_services.get_model_list(db=db, limit=10, offset=0)

            assert len(result) == 4
            assert result[1].username == "Test"
            assert result[2].username == "Test1"
            assert result[3].username == "Test2"

    @pytest.mark.asyncio(scope="function")
    async def test_get_user_by_id_func(self):
        async with AsyncSessionLocal() as db:
            user = await user_services.get_model_list(db=db, limit=1, offset=0)
            user_id = user[0].id
            result = await user_services.get_model_by_id(db=db, model_id=user_id)

            assert result.id == user_id
            assert result.username == user[0].username
            assert result.email == user[0].email

    @pytest.mark.asyncio(scope="function")
    async def test_update_user(self, pydentic_update_data):
        async with AsyncSessionLocal() as db:
            user = await user_services.get_model_list(db=db, limit=1, offset=0)
            user_id = user[0].id
            result = await user_services.update_model(
                db=db, model_id=user_id, model_data=pydentic_update_data
            )

            assert result.id == user_id
            assert result.username == pydentic_update_data.username
            assert result.email == pydentic_update_data.email

    @pytest.mark.asyncio(scope="function")
    async def test_delete_user(self):
        async with AsyncSessionLocal() as db:
            user = await user_services.get_model_list(db=db, limit=1, offset=0)
            user_id = user[0].id
            await user_services.delete_model(db=db, model_id=user_id)

            result = await user_services.get_model_list(db=db, limit=10, offset=0)

            assert user not in result
