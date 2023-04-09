from fastapi import APIRouter

from managers.rate import RateManager
from schemas.rates import RateBase, RateConvert

router = APIRouter(tags=["Actions"])


@router.post("/base_rates_upload/", status_code=200)
async def base_rates_upload():
    try:
        await RateManager.create_base_rates()
    except Exception as e:
        raise e


@router.post("/convert/")
async def convert(data: RateConvert):
    result = await RateManager.convert(data.dict())
    return {"result": result} if result else {"error": "Cannot convert by requested conditions"}
