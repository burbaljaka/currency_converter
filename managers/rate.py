import copy

import loguru
from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy import func, select

from db import database
from models import rate
from resources.df import parse_data


class RateManager:
    @staticmethod
    @database.transaction()
    async def create_base_rates():
        objs = parse_data()
        await database.execute_many(query=rate.insert(), values=objs)

    @staticmethod
    @database.transaction()
    async def create_rate(rate_data: dict):
        try:
            id_ = await database.execute(rate.insert().values(**rate_data))
        except UniqueViolationError as e:
            raise HTTPException(400, f"{e}")

        rate_data["from_cur"], rate_data["to_cur"] = rate_data["to_cur"], rate_data["from_cur"]
        rate_data["rate"] = round(1 / rate_data["rate"], 4)

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
    @database.transaction()
    async def update_one_rate(id_: int, rate_data: dict):
        obj = await database.fetch_one(rate.select().where(rate.c.id == id_))
        if not obj:
            raise HTTPException(404, "Objects cannot be found")
        await database.execute(rate.update().where(rate.c.id == id_).values(**rate_data))
        return await database.fetch_one(rate.select().where(rate.c.id == id_))

    @staticmethod
    @database.transaction()
    async def delete_one_rate(id_: int):
        obj = await database.fetch_one(rate.select().where(rate.c.id == id_))
        if not obj:
            raise HTTPException(404, "Objects cannot be found")
        await database.execute(rate.delete().where(rate.c.id == id_))

    @staticmethod
    async def convert(data: dict):
        if obj := await database.fetch_one(rate.select().where(
            rate.c.date == data["date"],
            rate.c.from_cur == data["from_cur"],
            rate.c.to_cur == data["to_cur"],
        )):
            result = data["amount"] * obj.rate

        else:
            cur_count = await database.execute(select(func.count(rate.c.from_cur.distinct())))
            all_rates = await database.fetch_all(rate.select().where(rate.c.date == data["date"]))

            from_curs = set()
            from_curs.add(data["from_cur"])
            paths_struct = dict()
            initial_struct = {data["from_cur"]: 1}
            current_paths = list()
            min_rate = None
            checked = set()
            checked.add(data["from_cur"])

            while len(checked) <= cur_count and initial_struct:
                near_curs = [x for x in all_rates if x.from_cur in from_curs]
                founds = [x for x in near_curs if x.to_cur == data["to_cur"]]
                if not paths_struct:
                    paths_struct = {f"{x.from_cur},{x.to_cur}": x.rate for x in near_curs}

                else:
                    for key in current_paths:
                        for x in near_curs:
                            if key.endswith(x.from_cur) and x.to_cur not in key:
                                paths_struct[f"{key},{x.to_cur}"] = paths_struct[key] * x.rate

                        paths_struct.pop(key)
                current_paths = list(paths_struct.keys())

                if founds:
                    for key in current_paths:
                        for found in founds:
                            if key.endswith(found.to_cur):
                                # paths_struct[f"{key},{found.to_cur}"] = value * found.rate
                                if min_rate is not None:
                                    min_rate = min(min_rate, paths_struct[key] * found.rate)
                                else:
                                    min_rate = paths_struct[key] * found.rate

                    [paths_struct.pop(key) for key in current_paths if key.endswith(data["to_cur"])]
                    current_paths = list(paths_struct.keys())

                checked.update([x.from_cur for x in near_curs])
                from_curs = set([x.to_cur for x in near_curs if x.to_cur != data['to_cur']])
                initial_struct = paths_struct
            if not min_rate:
                return None

            result = data["amount"] * min_rate
        return result
