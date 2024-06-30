import flask
import flask_restful
import flask_restful.reqparse
import requests
import datetime
import db

server = flask.Flask(__name__)
api = flask_restful.Api(server)


class Full_exercise(flask_restful.Resource):
  def __init__(self):
    self.parser_get = flask_restful.reqparse.RequestParser()
    self.parser_post = flask_restful.reqparse.RequestParser()

    def validate_columns(value, field):
      valid_columns = [db.Exercises.id.column_name, db.Exercises.name.column_name, db.Exercises.description.column_name, db.Exercises.code.column_name, db.Exercises.last_modified_date.column_name]
      if value not in valid_columns:
        raise ValueError(f"Value '{value}' in '{field}' is not one of valid values: {', '.join(valid_columns)}")
      return value
    
    def validate_ids(value):
      return int(value)
    
    def validate_page_number(value, field):
      number = int(value)
      if number <= 0:
        raise ValueError(f"Value '{value}' in '{field}' must be positive integer")
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
    self.parser_get.add_argument('page_number', type=validate_page_number, action='append', location='args', required=False, default=1)
    self.parser_get.add_argument('items_per_page', type=validate_items_per_page, action='append', location='args', required=False, default=100)

    self.parser_post.add_argument(db.Exercises.name.column_name, type=str, location='json', required=True)
    self.parser_post.add_argument(db.Exercises.description.column_name, type=str, location='json', required=True)
    self.parser_post.add_argument(db.Exercises.code.column_name, type=str, location='json', required=True)

  def get(self):
    args = self.parser_get.parse_args()
    columns = list(set(args['columns']))
    ids = list(set(args['ids']))
    page_number = args['page_number']
    items_per_page = args['items_per_page']

    exercises = db.Exercises.select(*[getattr(db.Exercises, column) for column in columns]).order_by(db.Exercises.id).paginate(page_number, items_per_page)
    pages = db.Exercises.select(*[getattr(db.Exercises, column) for column in columns]).count()
    if len(ids) != 0:
      exercises = exercises.where(db.Exercises.id.in_(ids))

    print(exercises, flush=True)
    return flask.jsonify({
      'exercises': list(exercises.dicts()),
      'pages': pages
    })

  def post(self):
    args = self.parser_post.parse_args()
    new_user = db.Exercises.create(
        name=args[db.Exercises.name.column_name],
        description=args[db.Exercises.description.column_name],
        code=args[db.Exercises.code.column_name]
    )

    return {
        db.Exercises.id.column_name: new_user.id,
        db.Exercises.name.column_name: new_user.name,
        db.Exercises.description.column_name: new_user.description,
        db.Exercises.code.column_name: new_user.code
    }

api.add_resource(Full_exercise, '/api/exercises')


class Specific_exercise(flask_restful.Resource):
  def __init__(self):
    self.parser_get = flask_restful.reqparse.RequestParser()
    self.parser_put = flask_restful.reqparse.RequestParser()

    def validate_columns(value, field):
      valid_columns = [db.Exercises.id.column_name, db.Exercises.name.column_name, db.Exercises.description.column_name, db.Exercises.code.column_name, db.Exercises.last_modified_date.column_name]
      if value not in valid_columns:
        raise ValueError(f"Value '{value}' in '{field}' is not one of valid values: {', '.join(valid_columns)}")
      return value
    self.parser_get.add_argument('columns', type=validate_columns, action='append', location='args', required=True)

    self.parser_put.add_argument(db.Exercises.name.column_name, type=str, location='json', required=True)
    self.parser_put.add_argument(db.Exercises.description.column_name, type=str, location='json', required=True)
    self.parser_put.add_argument(db.Exercises.code.column_name, type=str, location='json', required=True)

  def get(self, id: int):
    args = self.parser_get.parse_args()
    columns = list(set(args['columns']))

    query = db.Exercises.select(*[getattr(db.Exercises, column) for column in columns]).where(db.Exercises.id == id).limit(1)
    results = list(query.dicts())
    if len(results) != 1:
      return flask.jsonify({}), 404
    return results[0]

  def put(self, id: int):
    args = self.parser_put.parse_args()
    db.Exercises \
      .update({
          db.Exercises.name: args[db.Exercises.name.column_name],
          db.Exercises.description: args[db.Exercises.description.column_name],
          db.Exercises.code: args[db.Exercises.code.column_name],
          db.Exercises.last_modified_date: datetime.datetime.now()
      }) \
        .where(db.Exercises.id == id) \
        .returning(db.Exercises) \
        .execute()

    return flask.jsonify({
        db.Exercises.id.name: id,
        db.Exercises.name.name: args[db.Exercises.name.column_name],
        db.Exercises.description.name: args[db.Exercises.description.column_name],
        db.Exercises.code.name: args[db.Exercises.code.column_name]
    })

api.add_resource(Specific_exercise, '/api/exercises/<int:id>')


@server.route('/api/pdf_url', methods=['POST'])
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
  # print(response.url, flush=True)
  return response.url

@server.route('/api/classes', methods=['GET'])
def get_classes():
  with open('./api/classes/index.py', 'r') as file:
    contenido = file.read()
    return flask.Response(contenido, content_type='text/plain'), 200
