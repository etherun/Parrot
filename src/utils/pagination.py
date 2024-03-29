from __future__ import annotations

__all__ = [
    "Params",
    "OptionalParams",
    "Page",
]

from math import ceil
from typing import Any, Generic, Optional, Sequence, TypeVar
from typing_extensions import Self
from fastapi import Query
from pydantic import BaseModel

from fastapi_pagination.bases import AbstractParams, RawParams, AbstractPage
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from fastapi_pagination.utils import create_pydantic_model

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(20, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class OptionalParams(Params):
    page: Optional[int] = Query(None, ge=1, description="Page number")
    size: Optional[int] = Query(None, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size if self.size is not None else None,
            offset=self.size * (self.page - 1)
            if self.page is not None and self.size is not None
            else None,
        )


class Page(AbstractPage[T], Generic[T]):
    status: str
    data: Sequence[T]
    page: Optional[GreaterEqualOne]
    size: Optional[GreaterEqualOne]
    pages: Optional[GreaterEqualZero] = None
    total: GreaterEqualZero

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        status: str = "success",
        **kwargs: Any,
    ) -> Self:
        if not isinstance(params, Params):
            raise TypeError("Page should be used with Params")

        size = params.size if params.size is not None else total
        page = params.page if params.page is not None else 1
        pages = ceil(total / size) if total is not None else None

        return create_pydantic_model(
            cls,
            total=total,
            data=items,
            page=page,
            size=size,
            pages=pages,
            status=status,
            **kwargs,
        )
