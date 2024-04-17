import dotenv
import os
import peewee
import datetime

dotenv.load_dotenv()

db = peewee.PostgresqlDatabase(
    os.environ.get('DATABASE_DB', 'postgres'),
    host=os.environ.get('DATABASE_HOST', 'localhost'),
    port=os.environ.get('DATABASE_PORT', 5432),
    user=os.environ.get('DATABASE_USER', 'postgres'),
    password=os.environ.get('DATABASE_PASSWORD', '12345'), # windows 12345, mac 12345678
)


class Exercise(peewee.Model):
  id = peewee.AutoField()
  name = peewee.TextField()
  description = peewee.TextField()
  code = peewee.TextField()
  last_modified_date = peewee.DateField(default=datetime.datetime.now)

  class Meta:
    database = db


db.connect()
db.create_tables([Exercise])
