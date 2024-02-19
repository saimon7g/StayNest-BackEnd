FROM python:3.12.0


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /APIGateWay

COPY requirements.txt /APIGateWay/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /APIGateWay/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]