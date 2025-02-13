from email_validator import validate_email, EmailNotValidError


class Email:
    def __init__(self, value: str):
        try:
            self.value = validate_email(value, check_deliverability=False).normalized
        except EmailNotValidError as error:
            raise ValueError(f"Invalid email address: ${error}")

    def __str__(self):
        return self.value
