import datetime


class DueDate:
    def __init__(self, date_value):
        self.value = self._validate(date_value)

    def _validate(self, date_value):
        if isinstance(date_value, datetime.date):
            return date_value
        elif isinstance(date_value, str):
            return datetime.datetime.strptime(date_value, "%Y-%m-%d").date()
        else:
            raise ValueError(f"Invalid date format: {date_value}")
