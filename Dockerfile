FROM python:3.7-slim-stretch

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /testfront

COPY . /testfront/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /testfront/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]