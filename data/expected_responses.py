class AuthResponses:

    @staticmethod
    def user_already_exists():
        return {"success": False, "message": "User already exists"}

    @staticmethod
    def email_or_password_incorrect():
        return {"success": False, "message": "email or password are incorrect"}

    @staticmethod
    def you_should_be_authorised():
        return {"success": False, "message": "You should be authorised"}


class OrderResponses:

    @staticmethod
    def ingredient_ids_required():
        return {"success": False, "message": "Ingredient ids must be provided"}
