import re

P_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class FieldValidators:
    @staticmethod
    def email(value: str):
        if not re.match(P_EMAIL, value):
            raise ValueError("Invalid email address input.")
        return value
