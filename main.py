from fileinput import filename
from unicodedata import name
from flask import Flask, render_template, Blueprint, send_from_directory
from flask_cors import CORS
import firebase_admin



app = Flask(__name__)
app.config['SECRET_KEY']='asecretkey'
CORS(app,supports_credentials=True)
firebase_admin.initialize_app()

from api import angular



app.register_blueprint(angular)



@app.route('/assets/<path:filename>')
def custom_static_for_assets(filename):
    return send_from_directory('angular/dist/angular/assets', filename)


@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory('angular/dist/angular/', filename)


@app.route('/')
def index():
    return render_template('index.html',name=filename)

if __name__ == '__main__':
    CORS(app)
    app.run(host='127.0.0.1', port=8000, debug=True)