FROM python:3.9-buster

RUN mkdir -p /usr/src/sibdev/
WORKDIR /usr/src/sibdev/

# WORKDIR sibdev

COPY requirements.txt ./

EXPOSE 8000

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
