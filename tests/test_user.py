import pytest
import allure
from helpers.api_client import StellarBurgersAPI
from config.scenarios import UserUpdateScenarios


@allure.epic("API Тесты")
@allure.feature("Работа с профилем пользователя")
class TestUser:

    @pytest.mark.parametrize(
        "desc, payload_builder",
        UserUpdateScenarios.SCENARIOS,
        ids=[s[0] for s in UserUpdateScenarios.SCENARIOS],
    )
    @allure.title("Изменение данных пользователя с авторизацией: {desc}")
    @allure.description(
        "Проверка обновления email, name или обоих полей авторизованным пользователем."
    )
    def test_update_user_authorized(self, registered_user, desc, payload_builder):
        payload = payload_builder(registered_user)
        with allure.step(f"Отправить PATCH /auth/user с данными: {payload}"):
            resp = StellarBurgersAPI.update_user(
                payload, registered_user["access_token"]
            )
        with allure.step("Проверить успешное обновление (200) и корректность ответа"):
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert data["user"]["email"] == payload["email"]
            assert data["user"]["name"] == payload["name"]

    @pytest.mark.parametrize(
        "desc, payload_builder",
        UserUpdateScenarios.SCENARIOS,
        ids=[s[0] for s in UserUpdateScenarios.SCENARIOS],
    )
    @allure.title("Попытка изменения данных без авторизации: {desc}")
    @allure.description("Попытка обновить данные без токена авторизации.")
    def test_update_user_unauthorized(self, desc, payload_builder):
        fake_user = {"email": f"test_{desc}@example.com", "name": f"Test {desc}"}
        payload = payload_builder(fake_user)
        with allure.step(f"Отправить PATCH /auth/user без токена с данными: {payload}"):
            resp = StellarBurgersAPI.update_user(payload, token=None)
        with allure.step("Проверить ошибку авторизации (401)"):
            assert resp.status_code == 401
            assert resp.json()["success"] is False
            assert resp.json()["message"] == "You should be authorised"
