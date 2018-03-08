# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, url_for, json

from hms.blueprints.util.models.file_info import FileInfo

util = Blueprint('util', __name__, url_prefix='/util')


@util.before_request
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    pass


@util.route('/get_marker_img_list', methods=['GET', 'POST'])
def get_marker_img_list():
    file_path = url_for('static', filename='images/marker/icon_64')

    return json.dumps(FileInfo.get_file_list(file_path))
