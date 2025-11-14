import pytest
import allure
from helpers.api_client import StellarBurgersAPI
from data.expected_responses import AuthResponses


@allure.epic("API Тесты")
@allure.feature("Авторизация и регистрация")
class TestAuth:

    @allure.title("Регистрация нового пользователя")
    @allure.description("Проверка успешной регистрации уникального пользователя.")
    def test_register_new_user(self, unique_user_data, created_user_cleanup):
        with allure.step("Отправить POST-запрос на /auth/register с валидными данными"):
            resp = StellarBurgersAPI.register(
                unique_user_data["email"],
                unique_user_data["password"],
                unique_user_data["name"],
            )
        with allure.step("Проверить успешный ответ (200) и наличие токена"):
            assert resp.status_code == 200
            assert resp.json()["success"] is True
            data = resp.json()
            assert data["user"]["email"] == unique_user_data["email"]
            assert "accessToken" in data

            token = data["accessToken"].split(" ")[-1]
            created_user_cleanup(token)

    @allure.title("Регистрация существующего пользователя")
    @allure.description("Попытка регистрации пользователя с уже занятым email.")
    def test_register_existing_user(self, registered_user):
        with allure.step(
            "Отправить POST-запрос на /auth/register с уже существующими данными"
        ):
            resp = StellarBurgersAPI.register(
                registered_user["email"], "newpass123", "New Name"
            )
        with allure.step("Проверить ответ с кодом 403 и сообщением об ошибке"):
            assert resp.status_code == 403
            assert resp.json() == AuthResponses.user_already_exists()

    @allure.title("Регистрация пользователя с пропущеными полями.")
    @allure.description("Проверка ошибки при отсутствии пароля.")
    def test_register_missing_field(self, unique_user_data):
        with allure.step("Отправить запрос на регистрацию с пустым паролем"):
            resp = StellarBurgersAPI.register(
                unique_user_data["email"], "", unique_user_data["name"]
            )
        with allure.step("Проверить ошибку (403) и сообщение о required fields"):
            assert resp.status_code == 403
            assert resp.json()["success"] is False
            assert "required fields" in resp.json()["message"]

    @allure.title("Успешный логин существующего пользователя")
    @allure.description("Проверка входа по корректным email и паролю.")
    def test_login_valid_user(self, registered_user):
        with allure.step("Отправить POST /auth/login с валидными данными"):
            resp = StellarBurgersAPI.login(
                registered_user["email"], registered_user["password"]
            )
        with allure.step("Проверить успешный ответ (200) и наличие токена"):
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert "accessToken" in data
            assert data["user"]["email"] == registered_user["email"]

    @allure.title("Логин с неверными данными")
    @allure.description("Попытка входа с несуществующим email и паролем.")
    def test_login_invalid_credentials(self):
        with allure.step("Отправить POST /auth/login с неверными данными"):
            resp = StellarBurgersAPI.login("wrong@yandex.ru", "badpass")
        with allure.step(
            "Проверить ошибку (401) и сообщение 'email or password are incorrect'"
        ):
            assert resp.status_code == 401
            assert resp.json() == AuthResponses.email_or_password_incorrect()
