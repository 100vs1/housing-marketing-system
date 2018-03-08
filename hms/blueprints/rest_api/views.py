# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, json

rest_api = Blueprint('rest_api', __name__, url_prefix='/rest_api')


@rest_api.before_request
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    pass
