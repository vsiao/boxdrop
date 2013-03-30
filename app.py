#!/usr/bin/python

from flask import Flask, render_template, redirect, url_for
from flask.ext.dropbox import Dropbox
import settings

app = Flask(__name__, static_folder='public', template_folder='views')
app.config.from_object(settings)

dropbox = Dropbox(app)
dropbox.register_blueprint(url_prefix='/dropbox')

@app.route('/')
def index():
    return render_template('index.html',
        dropbox_login_url=dropbox.login_url)

@app.route('/app')
def home():
    root_meta = dropbox.client.metadata('/')
    return render_template('app.html',
        dropbox_logout_url=dropbox.logout_url,
        root_data=root_meta)

@app.route('/drop')
def drop():
    root_meta = dropbox.client.metadata('/')
    for f in root_meta['contents']:
        dropbox.client.file_delete(f['path'])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
