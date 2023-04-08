import sqlalchemy
from sqlalchemy import UniqueConstraint

from db import metadata

rate = sqlalchemy.Table(
    "rates",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("date", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("from_cur", sqlalchemy.String(3), nullable=False),
    sqlalchemy.Column("to_cur", sqlalchemy.String(3), nullable=False),
    sqlalchemy.Column("rate", sqlalchemy.Float, nullable=False),
    UniqueConstraint("from_cur", "to_cur", "date", name="cur_pair_date")
)