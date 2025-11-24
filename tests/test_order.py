import allure
from helpers.api_client import StellarBurgersAPI
from data.expected_responses import OrderResponses, AuthResponses


@allure.epic("API Тесты")
@allure.feature("Работа с заказами")
class TestOrders:

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверка успешного создания заказа с валидными ингредиентами.")
    def test_create_order_authorized(self, registered_user, valid_ingredient_ids):
        ingredients = valid_ingredient_ids[:2]
        with allure.step(f"Отправить POST /orders с ингредиентами: {ingredients}"):
            resp = StellarBurgersAPI.create_order(
                ingredients, registered_user["access_token"]
            )
        with allure.step("Проверить успешное создание (200) и наличие номера заказа"):
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert "order" in data
            assert "number" in data["order"]
            assert isinstance(data["order"]["number"], int)
            assert data["order"]["number"] > 0

    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверка, что гость может создать заказ (API разрешает).")
    def test_create_order_unauthorized(self, valid_ingredient_ids):
        """
         Неавторизованный пользователь МОЖЕТ создавать заказы через API.
        Это особенность реализации: гости могут оформлять заказы, но не видят их в истории.
        """
        ingredients = valid_ingredient_ids[:2]
        with allure.step(
            f"Отправить POST /orders без токена с ингредиентами: {ingredients}"
        ):
            resp = StellarBurgersAPI.create_order(ingredients)
        with allure.step("Проверить успешный ответ (200)"):
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert "order" in data
            assert "number" in data["order"]

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Попытка создания заказа с пустым списком ингредиентов.")
    def test_create_order_with_no_ingredients(self, registered_user):
        with allure.step("Отправить POST /orders с пустым списком ингредиентов"):
            resp = StellarBurgersAPI.create_order([], registered_user["access_token"])
        with allure.step(
            "Проверить ошибку (400) и сообщение 'Ingredient ids must be provided'"
        ):
            assert resp.status_code == 400
            assert resp.json() == OrderResponses.ingredient_ids_required()

    @allure.title("Создание заказа с неверным хешем ингредиента")
    @allure.description("Попытка создания заказа с несуществующим ID ингредиента.")
    def test_create_order_with_invalid_ingredient(self, registered_user):
        with allure.step("Отправить POST /orders с неверным ID ингредиента"):
            resp = StellarBurgersAPI.create_order(
                ["invalid_hash_123"], registered_user["access_token"]
            )
        with allure.step("Проверить ошибку сервера (500)"):
            assert resp.status_code == 500

    @allure.title("Получение заказов авторизованным пользователем")
    @allure.description(
        "Проверка получения списка заказов для авторизованного пользователя."
    )
    def test_get_user_orders_authorized(self, registered_user):
        with allure.step("Отправить GET /orders с токеном"):
            resp = StellarBurgersAPI.get_user_orders(registered_user["access_token"])
        with allure.step("Проверить успешный ответ (200) и структуру данных"):
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert "orders" in data
            assert "total" in data
            assert "totalToday" in data

    @allure.title("Попытка получения заказов без авторизации")
    @allure.description("Попытка получить заказы без передачи токена.")
    def test_get_user_orders_unauthorized(self):
        with allure.step("Отправить GET /orders без токена"):
            resp = StellarBurgersAPI.get_user_orders(token=None)
        with allure.step("Проверить ошибку авторизации (401)"):
            assert resp.status_code == 401
            assert resp.json() == AuthResponses.you_should_be_authorised()
