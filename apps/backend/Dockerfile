FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD [ "python", "api/dev.py", "dev" ]
