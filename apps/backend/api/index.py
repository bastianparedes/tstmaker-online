import flask
import requests
import datetime
import db

server = flask.Flask(__name__)


@server.route('/api/exercises', methods=['GET', 'POST'])
def getFullExercises():
  if (flask.request.method == 'GET'):
    columns = flask.request.args.getlist('columns')
    if (len(columns) == 0): return flask.jsonify({}), 400

    query = db.Exercise.select(*[getattr(db.Exercise, column) for column in columns]).order_by(db.Exercise.id)
    results = list(query.dicts())
    return flask.jsonify(results)

  elif (flask.request.method == 'POST'):
    request_data = flask.request.get_json()
    new_user = db.Exercise.create(
        name=request_data['name'],
        description=request_data['description'],
        code=request_data['code']
    )

    return {
        db.Exercise.id.column_name: new_user.id,
        db.Exercise.name.column_name: new_user.name,
        db.Exercise.description.column_name: new_user.description,
        db.Exercise.code.column_name: new_user.code,
        db.Exercise.last_modified_date.column_name: new_user.last_modified_date
    }
  return None


@server.route('/api/exercises/<int:id>', methods=['GET', 'PUT'])
def getSpecificExercise(id: int):
  if (flask.request.method == 'GET'):
    columns = flask.request.args.getlist('columns')
    if (len(columns) == 0): return flask.jsonify({}), 400

    query = db.Exercise.select(*[getattr(db.Exercise, column) for column in columns]).where(db.Exercise.id == id).limit(1)
    results = list(query.dicts())
    if len(results) != 1: return flask.jsonify({}), 404
    return results[0]

  elif (flask.request.method == 'PUT'):
    request_data = flask.request.get_json()

    db.Exercise \
      .update({
          db.Exercise.name: request_data['name'],
          db.Exercise.description: request_data['description'],
          db.Exercise.code: request_data['code'],
          db.Exercise.last_modified_date: datetime.datetime.now()
      }) \
      .where(db.Exercise.id == id) \
      .returning(db.Exercise) \
      .execute()

    return flask.jsonify({
      db.Exercise.id.name: int(id),
      db.Exercise.name.name: request_data['name'],
      db.Exercise.description.name: request_data['description'],
      db.Exercise.code.name: request_data['code'],
      db.Exercise.last_modified_date.name: datetime.datetime.now()
    }
)
  return None


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
