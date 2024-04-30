import flask
import flask_restful
import flask_restful.reqparse
import requests
import datetime
import db

server = flask.Flask(__name__)
api = flask_restful.Api(server)


class Full_Exercise(flask_restful.Resource):
  def __init__(self):
    self.parser_get = flask_restful.reqparse.RequestParser()
    self.parser_post = flask_restful.reqparse.RequestParser()

    def validate_columns(value, field):
      valid_columns = [db.Exercise.id.column_name, db.Exercise.name.column_name, db.Exercise.description.column_name, db.Exercise.code.column_name, db.Exercise.last_modified_date.column_name]
      if value not in valid_columns:
        raise ValueError(f"Value '{value}' in '{field}' is not one of valid values: {', '.join(valid_columns)}")
      return value
    self.parser_get.add_argument('columns', type=validate_columns, action='append', location='args', required=True)

    self.parser_post.add_argument(db.Exercise.name.column_name, type=str, location='json', required=True)
    self.parser_post.add_argument(db.Exercise.description.column_name, type=str, location='json', required=True)
    self.parser_post.add_argument(db.Exercise.code.column_name, type=str, location='json', required=True)

  def get(self):
    args = self.parser_get.parse_args()
    columns = list(set(args['columns']))
    query = db.Exercise.select(*[getattr(db.Exercise, column) for column in columns]).order_by(db.Exercise.id)
    results = list(query.dicts())
    return flask.jsonify(results)

  def post(self):
    args = self.parser_post.parse_args()
    new_user = db.Exercise.create(
        name=args[db.Exercise.name.column_name],
        description=args[db.Exercise.description.column_name],
        code=args[db.Exercise.code.column_name]
    )

    return {
        db.Exercise.id.column_name: new_user.id,
        db.Exercise.name.column_name: new_user.name,
        db.Exercise.description.column_name: new_user.description,
        db.Exercise.code.column_name: new_user.code
    }


api.add_resource(Full_Exercise, '/api/exercises')


class Specific_Exercise(flask_restful.Resource):
  def __init__(self):
    self.parser_get = flask_restful.reqparse.RequestParser()
    self.parser_put = flask_restful.reqparse.RequestParser()

    def validate_columns(value, field):
      valid_columns = [db.Exercise.id.column_name, db.Exercise.name.column_name, db.Exercise.description.column_name, db.Exercise.code.column_name, db.Exercise.last_modified_date.column_name]
      if value not in valid_columns:
        raise ValueError(f"Value '{value}' in '{field}' is not one of valid values: {', '.join(valid_columns)}")
      return value
    self.parser_get.add_argument('columns', type=validate_columns, action='append', location='args', required=True)

    self.parser_put.add_argument(db.Exercise.name.column_name, type=str, location='json', required=True)
    self.parser_put.add_argument(db.Exercise.description.column_name, type=str, location='json', required=True)
    self.parser_put.add_argument(db.Exercise.code.column_name, type=str, location='json', required=True)

  def get(self, id: int):
    args = self.parser_get.parse_args()
    columns = list(set(args['columns']))

    query = db.Exercise.select(*[getattr(db.Exercise, column) for column in columns]).where(db.Exercise.id == id).limit(1)
    results = list(query.dicts())
    if len(results) != 1:
      return flask.jsonify({}), 404
    return results[0]

  def put(self, id: int):
    args = self.parser_put.parse_args()
    db.Exercise \
      .update({
          db.Exercise.name: args[db.Exercise.name.column_name],
          db.Exercise.description: args[db.Exercise.description.column_name],
          db.Exercise.code: args[db.Exercise.code.column_name],
          db.Exercise.last_modified_date: datetime.datetime.now()
      }) \
        .where(db.Exercise.id == id) \
        .returning(db.Exercise) \
        .execute()

    return flask.jsonify({
        db.Exercise.id.name: id,
        db.Exercise.name.name: args[db.Exercise.name.column_name],
        db.Exercise.description.name: args[db.Exercise.description.column_name],
        db.Exercise.code.name: args[db.Exercise.code.column_name]
    })


api.add_resource(Specific_Exercise, '/api/exercises/<int:id>')


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
  return response.url
