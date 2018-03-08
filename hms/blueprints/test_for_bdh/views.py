# -*- coding: utf-8 -*-
import datetime
from operator import eq

import requests
from flask import Blueprint, render_template, request, current_app, json, jsonify
from flask_login import login_required

test = Blueprint('test', __name__,template_folder='templates', url_prefix='/test')


@test.before_request
@login_required
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    current_app.logger.debug('URL: %s', request)
    pass


@test.route('/', methods=['GET', 'POST'])
def index():
    return render_template('test/index.html', now=datetime.datetime.now())