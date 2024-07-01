import flask
import flask_restful
import flask_restful.reqparse
import requests
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


app = flask.Flask(__name__)
api = flask_restful.Api(app)


class Full_exercise(flask_restful.Resource):
  def __init__(self):
    self.parser_get = flask_restful.reqparse.RequestParser()
    self.parser_post = flask_restful.reqparse.RequestParser()

    def validate_columns(value, field):
      valid_columns = [Exercises.id.column_name, Exercises.name.column_name, Exercises.description.column_name, Exercises.code.column_name, Exercises.last_modified_date.column_name]
      if value not in valid_columns:
        raise ValueError(f"Value '{value}' in '{field}' is not one of valid values: {', '.join(valid_columns)}")
      return value
    
    def validate_ids(value):
      return int(value)
    
    def validate_page_number(value, field):
      number = int(value)
      if number < 0:
        raise ValueError(f"Value '{value}' in '{field}' must be positive integer o Zero")
      return number
    
    def validate_items_per_page(value, field):
      limit = 100
      number = int(value)
      if not number > 0:
        raise ValueError(f"Value '{value}' in '{field}' must be positive integer")
      if number > limit:
        raise ValueError(f"Value '{value}' in '{field}' must be lower or equal to {limit}")
      return number

    self.parser_get.add_argument('columns', type=validate_columns, action='append', location='args', required=True)
    self.parser_get.add_argument('ids', type=validate_ids, action='append', location='args', required=False, default=[])
    self.parser_get.add_argument('page_number', type=validate_page_number, location='args', required=False, default=1)
    self.parser_get.add_argument('items_per_page', type=validate_items_per_page, location='args', required=False, default=100)
    self.parser_get.add_argument('query', type=str, location='args', required=False, default='')

    self.parser_post.add_argument(Exercises.name.column_name, type=str, location='json', required=True)
    self.parser_post.add_argument(Exercises.description.column_name, type=str, location='json', required=True)
    self.parser_post.add_argument(Exercises.code.column_name, type=str, location='json', required=True)

  def get(self):
    args = self.parser_get.parse_args()
    columns = list(set(args['columns']))
    ids = list(set(args['ids']))
    page_number = args['page_number']
    items_per_page = args['items_per_page']
    query = args['query']

    exercises = Exercises.select(*[getattr(Exercises, column) for column in columns]).order_by(Exercises.id).paginate(page_number + 1, items_per_page).where(Exercises.name.contains(query) | Exercises.description.contains(query))
    if len(ids) != 0:
      exercises = exercises.where(Exercises.id.in_(ids))

    total_exercises = Exercises.select(*[getattr(Exercises, column) for column in columns]).where(Exercises.name.contains(query) | Exercises.description.contains(query)).count()

    return flask.jsonify({
      'exercises': list(exercises.dicts()),
      'total': total_exercises
    })

  def post(self):
    args = self.parser_post.parse_args()
    new_user = Exercises.create(
        name=args[Exercises.name.column_name],
        description=args[Exercises.description.column_name],
        code=args[Exercises.code.column_name]
    )

    return {
        Exercises.id.column_name: new_user.id,
        Exercises.name.column_name: new_user.name,
        Exercises.description.column_name: new_user.description,
        Exercises.code.column_name: new_user.code
    }

api.add_resource(Full_exercise, '/api/exercises')


class Specific_exercise(flask_restful.Resource):
  def __init__(self):
    self.parser_get = flask_restful.reqparse.RequestParser()
    self.parser_put = flask_restful.reqparse.RequestParser()

    def validate_columns(value, field):
      valid_columns = [Exercises.id.column_name, Exercises.name.column_name, Exercises.description.column_name, Exercises.code.column_name, Exercises.last_modified_date.column_name]
      if value not in valid_columns:
        raise ValueError(f"Value '{value}' in '{field}' is not one of valid values: {', '.join(valid_columns)}")
      return value
    self.parser_get.add_argument('columns', type=validate_columns, action='append', location='args', required=True)

    self.parser_put.add_argument(Exercises.name.column_name, type=str, location='json', required=True)
    self.parser_put.add_argument(Exercises.description.column_name, type=str, location='json', required=True)
    self.parser_put.add_argument(Exercises.code.column_name, type=str, location='json', required=True)

  def get(self, id: int):
    args = self.parser_get.parse_args()
    columns = list(set(args['columns']))

    query = Exercises.select(*[getattr(Exercises, column) for column in columns]).where(Exercises.id == id).limit(1)
    results = list(query.dicts())
    if len(results) != 1:
      return flask.jsonify({}), 404
    return results[0]

  def put(self, id: int):
    args = self.parser_put.parse_args()
    Exercises \
      .update({
          Exercises.name: args[Exercises.name.column_name],
          Exercises.description: args[Exercises.description.column_name],
          Exercises.code: args[Exercises.code.column_name],
          Exercises.last_modified_date: datetime.datetime.now()
      }) \
        .where(Exercises.id == id) \
        .returning(Exercises) \
        .execute()

    return flask.jsonify({
        Exercises.id.name: id,
        Exercises.name.name: args[Exercises.name.column_name],
        Exercises.description.name: args[Exercises.description.column_name],
        Exercises.code.name: args[Exercises.code.column_name]
    })

api.add_resource(Specific_exercise, '/api/exercises/<int:id>')


@app.route('/api/pdf_url', methods=['POST'])
def pdf_url():
  request_data = flask.request.get_json()
  latex_code = request_data['latex_code']
  response = requests.post(
    'https://texlive.net/cgi-bin/latexcgi',
    files={
      'filecontents[]': ('document.tex', latex_code, 'text/plain'),
      'filename[]': 'document.tex',
      'engine': 'pdflatex',
      'return': 'pdf'
    })
  return response.url

@app.route('/api/classes', methods=['GET'])
def get_classes():
  with open('./src/classes/index.py', 'r') as file:
    contenido = file.read()
    return flask.Response(contenido, content_type='text/plain'), 200

@app.route('/api/health', methods=['GET'])
def health():
  return flask.Response(False, content_type='text/plain'), 200
