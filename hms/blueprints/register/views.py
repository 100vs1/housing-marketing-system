# -*- coding: utf-8 -*-
import datetime

from flask import Blueprint, render_template, request, current_app, json, jsonify
from flask_login import login_required

register = Blueprint('register', __name__,
                     template_folder='templates', url_prefix='/register')


@register.before_request
@login_required
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    pass


@register.route('', methods=['GET', 'POST'])
def index():
    return render_template('register/index.html', now=datetime.datetime.now())
