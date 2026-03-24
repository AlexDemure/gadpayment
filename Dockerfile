FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv
RUN uv pip install --system --no-cache .

COPY . .

CMD ["python", "-m", "src.bootstrap.server"]
