from typing import List, Optional

from fastapi import APIRouter

from managers.rate import RateManager
from schemas.rates import RateOut, RateIn, RateFilter

router = APIRouter(tags=["Rates"])


@router.post("/rates/", response_model=RateOut, status_code=201)
async def create_rate(rate: RateIn):
    return await RateManager.create_rate(rate.dict())


@router.post("/rates/historical/", response_model=List[RateOut])
async def get_rates(rate: RateFilter):
    return await RateManager.get_historical_rates(rate.dict())


@router.get("/rates/{rate_id}", response_model=Optional[RateOut])
async def get_one_rate(rate_id: int):
    return await RateManager.get_one_rate(rate_id)


@router.patch("/rates/{rate_id}/", response_model=RateOut)
async def update_rate(rate_id: int, rate_data: RateIn):
    return await RateManager.update_one_rate(rate_id, rate_data.dict())


@router.delete("/rates/{rate_id}/", status_code=204)
async def delete_rate(rate_id: int):
    await RateManager.delete_one_rate(rate_id)



