FROM python:3.7-slim-stretch

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /testfront

COPY requirements.txt /testfront/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /testfront/

EXPOSE 1000

CMD ["uvicorn", "main:app", "--reload"]