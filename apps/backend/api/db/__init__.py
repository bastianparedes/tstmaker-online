import dotenv
import os
import peewee
import datetime

dotenv.load_dotenv()

DATABASE_PROTOCOL = os.environ.get('DATABASE_PROTOCOL')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = int(os.environ.get('DATABASE_PORT'))
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_SSL_MODE = os.environ.get('DATABASE_SSL_MODE', 'prefer')
URI = f'{DATABASE_PROTOCOL}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?sslmode={DATABASE_SSL_MODE}'

db = peewee.PostgresqlDatabase(
  DATABASE_NAME,
  host=DATABASE_HOST,
  port=DATABASE_PORT,
  user=DATABASE_USER,
  password=DATABASE_PASSWORD,  # windows 12345, mac 12345678
  sslmode=DATABASE_SSL_MODE
)

class Exercises(peewee.Model):
  id = peewee.AutoField()
  name = peewee.TextField()
  description = peewee.TextField()
  code = peewee.TextField()
  last_modified_date = peewee.DateField(default=datetime.datetime.now)

  class Meta:
    database = db


db.connect()
db.create_tables([Exercises])
