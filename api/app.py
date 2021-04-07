import os

from flask import Flask, request, flash, redirect, jsonify

from utils.dispatcher_aws import Dispatcher
from utils.database import DatabaseHandler
from utils.search import SearchItem

app = Flask(__name__)

path = os.getcwd()
app.secret_key = os.environ.get('SECRET_KEY')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = ['txt', 'csv']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/v1/file', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #Dispatcher('s3').upload_file_s3(file)
            file_id = DatabaseHandler().save_file(file)
            flash("Uploaded Successfully")
            constructor_batch(file, file_id)
            return jsonify(filename=file.filename, status_code=200)
        else:
            flash('Allowed file types are csv or txt')
            return redirect(request.url)
    if request.method == 'GET':
        item = request.args.get('item')
        search = SearchItem().search_item(item)
        if search:
            return jsonify(
                id=search.id, name=search.name, description=search.description,
                nickname=search.nickname, status_code=200)
        else:
            return jsonify(status_code=400, message="Item not Exist")


def constructor_batch(file, file_id):
    values = {
        'job_name': str(file.filename.replace('.', '-')) + '-Analyser-' + str(file_id),
        'parameter': str(file_id),
        'script': str('analyser.py')
    }
    Dispatcher('batch').aws_batch(**values)


if __name__ == '__main__':
    app.run(debug=True)
