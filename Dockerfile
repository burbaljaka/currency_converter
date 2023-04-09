FROM python:3.9 as base

ENV PYTHONUNBUFFERED=True

COPY requirements.txt /tmp/requirements.txt

RUN \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir restricted_pkg && \
    pip install --force-reinstall --no-cache-dir -r /tmp/requirements.txt

FROM base

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]