import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class RateFilter(BaseModel):
    from_cur: str = Field(..., max_length=3)
    to_cur: str = Field(..., max_length=3)
    date: Optional[datetime.date]

    @validator("from_cur", "to_cur")
    def to_upper(cls, v):
        return v.upper()


class RateConvert(RateFilter):
    amount: float


class RateBase(RateFilter):
    rate: float = Field(gt=0)


class RateIn(RateBase):
    pass


class RateOut(RateBase):
    id: int
