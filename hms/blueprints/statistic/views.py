# -*- coding: utf-8 -*-
import datetime
from operator import eq

import requests
from flask import Blueprint, render_template, request, current_app, json, jsonify
from flask_login import login_required

from hms.blueprints.statistic.models.stats_board_noori import StatsBoardNoori
from lib.util_json import render_json

statistic = Blueprint('statistic', __name__,
                      template_folder='templates', url_prefix='/statistic')


@statistic.before_request
@login_required
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    pass


@statistic.route('', methods=['GET', 'POST'])
def index():
    return render_template('statistic/index.html', now=datetime.datetime.now())


@statistic.route('/get_noori_data', methods=['GET'])
def get_noori_data():
    form_id = request.form.get("form_id") or request.args.get("form_id")
    style_num = request.form.get('style_num') or request.args.get('style_num')
    start_date = request.form.get('start_dt') or request.args.get('start_dt')
    end_date = request.form.get('end_dt') or request.args.get('end_dt')

    url = current_app.config.get('NOORI_URL') + "?key=" + current_app.config.get('NOORI_API_KEY')

    headers = {'Content-Type': 'application/json'}
    data = {
        "form_id": form_id,
        "style_num": style_num,
        "start_dt": start_date,
        "end_dt": end_date,
    }

    res = requests.get(url, params=data, headers=headers)
    res_json = res.json()
    status_code = res_json['result_status']['status_code']
    status = status_code.split("-")

    if eq(status[0], "INFO"):
        return render_json(200, result={
            "isSuccess": True,
            "data": res_json['result_data']
        })
    else:
        return render_json(200, result={
            "isSuccess": False,
            "err": res_json['result_status']['status_code'],
            "msg": res_json['result_status']['message']
        })

# @statistic.route('/get_tree_data', methods=['GET'])
# def get_tree_data():
#     req_type = request.form.get('req_type')
#
#     if req_type:
#         items = StatsBoardNoori.find_all_tree_data()
#
#         for item in items:
#             print(item)
#
#         return {
#             "isSuccess": True,
#             "data": "hihi"
#         }
#     else:
#         return {
#             "isSuccess" : False,
#             "err": u'에러 코드',
#             "msg": u'제공하지 않는 데이터 형태임',
#             "msgDetail": u'통계 보드에서 지원하지 않는 데이터 형태를 요청하였습니다.'
#         }
