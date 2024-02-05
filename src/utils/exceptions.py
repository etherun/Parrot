import json
from typing import Any
from fastapi import status as HTTP_STATUS


class CustomException(Exception):
    def __init__(
        self,
        status_code: int = HTTP_STATUS.HTTP_403_FORBIDDEN,
        status: str = "ERROR",
        data: Any = None,
    ):
        self.status_code = status_code
        self.status = status
        self.data = CustomException.load_content(data)

    @staticmethod
    def load_content(data):
        try:
            return json.loads(data)
        except Exception:  # pylint: disable=broad-exception-caught
            if isinstance(data, bytes):
                return data.decode("utf-8")
            return data

    def __str__(self):
        return f"""\n    status_code={self.status_code}\n    status={self.status}\n    data={self.data}"""
