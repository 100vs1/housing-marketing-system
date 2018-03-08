# -*- coding: utf-8 -*-
import datetime

from flask import Blueprint, render_template, request, current_app, json, jsonify, send_file
from flask_login import login_required


ai = Blueprint('ai', __name__,
               template_folder='templates', url_prefix='/ai')


@ai.before_request
@login_required
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    pass


@ai.route('', methods=['GET', 'POST'])
def index():
    return render_template('ai/index.html', now=datetime.datetime.now())