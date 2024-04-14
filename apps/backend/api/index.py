import flask
import requests
import datetime
import db

app = flask.Flask(__name__)


@app.route('/api/exercises', methods=['GET', 'POST', 'PUT'])
def getFullExercises():
  if (flask.request.method == 'GET'):
    # print('AYUDA', flask.request.args)
    query = db.Exercise.select(
        db.Exercise.id,
        db.Exercise.name,
        db.Exercise.description,
        db.Exercise.code,
        db.Exercise.last_modified_date
      ).order_by(
        db.Exercise.id)
    exercises = []
    for exercise in query:
      exercises.append({
          "id": exercise.id,
          "name": exercise.name,
          "description": exercise.description,
          "code": exercise.code,
          "last_modified_date": exercise.last_modified_date
      })
    return exercises

  elif (flask.request.method == 'POST'):
    request_data = flask.request.get_json()
    new_user = db.Exercise.create(
        name=request_data['name'],
        description=request_data['description'],
        code=request_data['code']
    )
    print(
        'AYUDA',
        type(
            db.Exercise.id.column_name),
        db.Exercise.id.column_name)
    return {
        db.Exercise.id.column_name: new_user.id,
        db.Exercise.name.column_name: new_user.name,
        db.Exercise.description.column_name: new_user.description,
        db.Exercise.code.column_name: new_user.code,
        db.Exercise.last_modified_date.column_name: new_user.last_modified_date
    }

  elif (flask.request.method == 'PUT'):
    request_data = flask.request.get_json()

    query = (db.Exercise.update({
        db.Exercise.name: request_data['name'],
        db.Exercise.description: request_data['description'],
        db.Exercise.code: request_data['code'],
        db.Exercise.last_modified_date: datetime.datetime.now()
    }).where(db.Exercise.id == request_data['id']))
    query.execute()
    return True

  return {}


@app.route('/api', methods=['GET'])
def api():
  return 'HOLA MUNDO DESDE /api'


@app.route('/api/home', methods=['GET'])
def api_home():
  return 'HOLA MUNDO DESDE /api/home'


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
