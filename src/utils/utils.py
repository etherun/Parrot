import logging
from typing import ClassVar
import httpx
from fastapi import status
from src.utils.exceptions import CustomException


class HttpxClient:
    client: ClassVar[httpx.AsyncClient] = httpx.AsyncClient()

    @staticmethod
    async def fetch(
        method,
        url,
        *,
        headers=None,
        data=None,
        body=None,
        timeout=10,
        ingore_response=False,
        follow_redirects=False,
    ):
        try:
            resp = await HttpxClient.client.request(
                method=method,
                url=url,
                data=data,
                json=body,
                timeout=timeout,
                headers=headers,
                follow_redirects=follow_redirects,
            )
        except httpx.TimeoutException as _error:
            logging.error("Request TIMEOUT-%s", url)
            raise CustomException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, status="TIMEOUT"
            ) from _error
        except Exception as _error:  # pylint: disable=broad-exception-caught
            logging.exception(_error)
            raise CustomException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status="REQUEST_ERROR",
            ) from _error

        if resp.status_code // 100 == 2:
            if ingore_response:
                return

            try:
                return resp.json()
            except Exception as _error:  # pylint: disable=broad-exception-caught
                raise CustomException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    status="DECODE_ERROR",
                    data=resp.content,
                ) from _error
        elif resp.status_code == status.HTTP_404_NOT_FOUND:
            raise CustomException(
                status_code=resp.status_code, status="NOT_FOUND", data=resp.content
            )
        elif resp.status_code == status.HTTP_401_UNAUTHORIZED:
            raise CustomException(
                status_code=resp.status_code, status="UNAUTHORIZED", data=resp.content
            )
        elif resp.status_code == status.HTTP_409_CONFLICT:
            raise CustomException(
                status_code=resp.status_code, status="CONFLICT", data=resp.content
            )
        elif resp.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            raise CustomException(
                status_code=resp.status_code,
                status="SERVICE_UNAVAILABLE",
                data=resp.content,
            )

        raise CustomException(status_code=resp.status_code, data=resp.content)
