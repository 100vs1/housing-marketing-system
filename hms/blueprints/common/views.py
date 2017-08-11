# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, json

from lib.util_json import render_json
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea

common = Blueprint('common', __name__,
                   url_prefix='/common')


@common.before_request
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    pass


@common.route('/get_codes', methods=['GET', 'POST'])
def get_codes():
    # 그룹코드로 코드 목록을 조회한다.
    group_code = request.args.get('group_code') or request.form.get('group_code')

    if group_code:
        codes = Code.find_by_group_code(group_code)

        return render_json(200, codes=[{
            'code': code.code,
            'name': code.name
        } for code in codes])

    return render_json(401, {'msg': '등록되지 않은 그룹코드입니다.'})


@common.route('/get_law_areas', methods=['GET', 'POST'])
def get_law_areas():
    # 법정 구역 목록을 조회한다.
    sid_cd = request.args.get('sid_cd') or request.form.get('sid_cd')
    sgg_cd = request.args.get('sgg_cd') or request.form.get('sgg_cd')

    if sid_cd:
        items = LawSggArea.find_by_sid_cd(sid_cd)

        return render_json(200, items=[{
            'sgg_cd': item.sgg_cd,
            'sgg_ko_nm': item.sgg_ko_nm,
            'coordinates': json.loads(item.geojson)['coordinates'],
            'layers': 'hms:law_sgg_area',
            'featureid': 'law_sgg_area.' + item.sgg_cd
        } for item in items])

    elif sgg_cd:
        items = LawEmdArea.find_by_sgg_cd(sgg_cd)

        return render_json(200, items=[{
            'emd_cd': item.emd_cd,
            'emd_ko_nm': item.emd_ko_nm,
            'coordinates': json.loads(item.geojson)['coordinates'],
            'layers': 'hms:law_emd_area',
            'featureid': 'law_emd_area.' + item.emd_cd
        } for item in items])

    else:
        items = LawSidArea.find_all()

        return render_json(200, items=[{
            'sid_cd': item.sid_cd,
            'sid_ko_nm': item.sid_ko_nm,
            'coordinates': json.loads(item.geojson)['coordinates'],
            'layers': 'hms:law_sid_area',
            'featureid': 'law_sid_area.' + item.sid_cd
        } for item in items])
