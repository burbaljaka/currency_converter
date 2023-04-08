from asyncpg import UniqueViolationError
from fastapi import HTTPException

from db import database
from models import rate
from resources.df import parse_data
from schemas.rates import RateIn


class RateManager:
    @staticmethod
    async def create_base_rates():
        objs = parse_data()
        await database.execute_many(query=rate.insert(), values=objs)

    @staticmethod
    async def create_rate(rate_data: dict):
        try:
            id_ = await database.execute(rate.insert().values(**rate_data))
        except UniqueViolationError as e:
            raise HTTPException(400, f"{e}")

        rate_data["from_cur"], rate_data["to_cur"] = rate_data["to_cur"], rate_data["from_cur"]
        rate_data["rate"] = round(1/rate_data["rate"], 4)

        try:
            await database.execute(rate.insert().values(**rate_data))
        except UniqueViolationError as e:
            raise HTTPException(400, f"{e}")

        return await database.fetch_one(rate.select().where(rate.c.id == id_))

    @staticmethod
    async def get_historical_rates(rate_data: dict):
        return await database.fetch_all(rate.select().where(
            rate.c.from_cur == rate_data["from_cur"],
            rate.c.to_cur == rate_data["to_cur"]
        ))

    @staticmethod
    async def get_one_rate(id_: int):
        obj = await database.fetch_one(rate.select().where(rate.c.id == id_))
        if not obj:
            raise HTTPException(404, "Objects cannot be found")
        return obj

    @staticmethod
    async def update_one_rate(id_: int, rate_data: dict):
        obj = await database.fetch_one(rate.select().where(rate.c.id == id_))
        if not obj:
            raise HTTPException(404, "Objects cannot be found")
        await database.execute(rate.update().where(rate.c.id == id_).values(**rate_data))
        return await database.fetch_one(rate.select().where(rate.c.id == id_))

    @staticmethod
    async def delete_one_rate(id_: int):
        obj = await database.fetch_one(rate.select().where(rate.c.id == id_))
        if not obj:
            raise HTTPException(404, "Objects cannot be found")
        await database.execute(rate.delete().where(rate.c.id == id_))

    @staticmethod
    async def convert(data: dict):
        obj = await database.fetch_one(rate.select().where(
            rate.c.date == data["date"],
            rate.c.from_cur == data["from_cur"],
            rate.c.to_cur == data["to_cur"],
        ))

        if not obj:
            raise HTTPException(400, "No such rate")

        result = data["amount"] * obj.rate

        return result



