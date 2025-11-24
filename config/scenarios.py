def update_email_only(user):
    return {"email": f"updated_{user['email']}", "name": user["name"]}


def update_name_only(user):
    return {"email": user["email"], "name": "Updated Name"}


def update_both(user):
    return {"email": f"updated_{user['email']}", "name": "Updated Full Name"}


class UserUpdateScenarios:
    SCENARIOS = [
        ("update_email_only", update_email_only),
        ("update_name_only", update_name_only),
        ("update_both", update_both),
    ]
