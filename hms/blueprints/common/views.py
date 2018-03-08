# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, json

from lib.util_json import render_json
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea, AdmSggArea, AdmEmdArea, \
    AdmSidArea, AdmAreaMaster, LawAreaMaster

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
            'name': code.name,
            'options': code.options,
        } for code in codes])

    return render_json(401, {'msg': '등록되지 않은 그룹코드입니다.'})


@common.route('/get_adm_areas', methods=['GET', 'POST'])
def get_adm_areas():
    sid_cd = request.args.get('sid_cd') or request.form.get('sid_cd')
    sgg_cd = request.args.get('sgg_cd') or request.form.get('sgg_cd')

    if sid_cd:
        items = AdmSggArea.find_by_sid_cd(sid_cd)

        return render_json(200, items=[{
            'sgg_cd': item.sgg_cd,
            'sgg_ko_nm': item.sgg_ko_nm,
            'coordinates': json.loads(item.geojson)['coordinates'],
        } for item in items])

    elif sgg_cd:
        items = AdmEmdArea.find_by_sgg_cd(sgg_cd)

        return render_json(200, items=[{
            'emd_cd': item.emd_cd,
            'emd_ko_nm': item.emd_ko_nm,
            'coordinates': json.loads(item.geojson)['coordinates'],
        } for item in items])

    else:
        items = AdmSidArea.find_all()

        return render_json(200, items=[{
            'sid_cd': item.sid_cd,
            'sid_ko_nm': item.sid_ko_nm,
            'coordinates': json.loads(item.geojson)['coordinates'],
        } for item in items])


@common.route('/get_adm_area_ko_names', methods=['GET', 'POST'])
def get_adm_area_ko_names():
    sid_cd = request.args.get('sid_cd') or request.form.get('sid_cd')
    sgg_cd = request.args.get('sgg_cd') or request.form.get('sgg_cd')
    emd_cd = request.args.get('emd_cd') or request.form.get('emd_cd')

    print(sid_cd)
    if sid_cd:
        items = AdmSidArea.finds_by_identity(sid_cd)

        return render_json(200, items=[{
            'cd': item.sid_cd,
            'ko_nm': item.sid_ko_nm
        } for item in items])
    elif sgg_cd:
        items = AdmSggArea.finds_by_identity(sgg_cd)
        return render_json(200, items=[{
            'cd': item.sgg_cd,
            'ko_nm': item.sgg_ko_nm
        } for item in items])
    elif emd_cd:
        items = AdmEmdArea.finds_by_identity(emd_cd)

        return render_json(200, items=[{
            'cd': item.emd_cd,
            'ko_nm': item.emd_ko_nm
        } for item in items])
    else:
        return {'error'}


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
        } for item in items])

    elif sgg_cd:
        items = LawEmdArea.find_by_sgg_cd(sgg_cd)

        return render_json(200, items=[{
            'emd_cd': item.emd_cd,
            'emd_ko_nm': item.emd_ko_nm,
            'coordinates': json.loads(item.geojson)['coordinates'],
        } for item in items])

    else:
        items = LawSidArea.find_all()

        return render_json(200, items=[{
            'sid_cd': item.sid_cd,
            'sid_ko_nm': item.sid_ko_nm,
            'coordinates': json.loads(item.geojson)['coordinates'],
        } for item in items])


@common.route('/get_law_area_ko_names', methods=['GET', 'POST'])
def get_law_area_ko_names():
    print('get_law_area_ko_names')
    sid_cd = request.args.get('sid_cd') or request.form.get('sid_cd')
    sgg_cd = request.args.get('sgg_cd') or request.form.get('sgg_cd')
    emd_cd = request.args.get('emd_cd') or request.form.get('emd_cd')

    print(sid_cd)
    if sid_cd:
        items = LawSidArea.finds_by_identity(sid_cd)

        return render_json(200, items=[{
            'cd': item.sid_cd,
            'ko_nm': item.sid_ko_nm
        } for item in items])
    elif sgg_cd:
        items = LawSggArea.finds_by_identity(sgg_cd)
        return render_json(200, items=[{
            'cd': item.sgg_cd,
            'ko_nm': item.sgg_ko_nm
        } for item in items])
    elif emd_cd:
        items = LawEmdArea.finds_by_identity(emd_cd)

        return render_json(200, items=[{
            'cd': item.emd_cd,
            'ko_nm': item.emd_ko_nm
        } for item in items])
    else:
        return {'error'}


@common.route('/get_law_polygon', methods=['GET', 'POST'])
def get_law_polygon():
    print('get_law_polygon')
    location_depth = request.form.get('locationDepth')
    location_code = request.form.get('locationCode')

    centroidValue = []
    polygon = []
    if location_depth == 'sid':
        centroidValue = LawSidArea.find_centroid_by_sid_cd(location_code)
        polygon = LawSggArea.find_polygons_by_sid_cd(location_code)
    elif location_depth == 'sgg':
        centroidValue = LawSggArea.find_centroid_by_sgg_cd(location_code)
        polygon = LawSggArea.find_polygons_by_sid_cd(location_code)
    elif location_depth == 'emd':
        centroidValue = LawEmdArea.find_centroid_by_emd_cd(location_code)
        polygon = LawEmdArea.find_polygons_by_sgg_cd(location_code)
    else:
        return render_json(200, {
            "msg": 'This is unsupported code.'
        })

    return render_json(200, {
        "centroid": json.loads(centroidValue[0][0]),
        "polygon": json.loads(polygon[0][0])
    })


@common.route('/get_adm_polygon', methods=['GET', 'POST'])
def get_adm_polygon():
    location_depth = request.form.get('locationDepth')
    location_code = request.form.get('locationCode')

    if location_depth == 'sid':
        centroidValue = AdmSidArea.find_centroid_by_sid_cd(location_code)
        polygon = AdmSggArea.find_polygons_by_sid_cd(location_code)
    elif location_depth == 'sgg':
        centroidValue = AdmSggArea.find_centroid_by_sgg_cd(location_code)
        polygon = AdmSggArea.find_polygons_by_sid_cd(location_code)
    elif location_depth == 'emd':
        centroidValue = AdmEmdArea.find_centroid_by_emd_cd(location_code)
        polygon = AdmEmdArea.find_polygons_by_sgg_cd(location_code)
    else:
        return render_json(200, {
            "msg": 'This is unsupported code.'
        })

    return render_json(200, {
        "centroid": json.loads(centroidValue[0][0]),
        "polygon": json.loads(polygon[0][0])
    })


@common.route('/get_low_law_cds', methods=['GET', 'POST'])
def get_low_law_cds():
    location_depth = request.form.get('locationDepth')
    location_code = request.form.get('locationCode')

    if location_depth == 'sid':
        codes = LawAreaMaster.find_sggs_by_sid_cd(location_code)

        result = []
        for location_code in codes:
            result.append(location_code[0])

        return render_json(200, rows=result)

    elif location_depth == 'sgg':
        codes = LawAreaMaster.find_emds_by_sgg_cd(location_code)

        result = []
        for location_code in codes:
            result.append(location_code[0])

        return render_json(200, rows=result)

    elif location_depth == 'emd':
        return render_json(200, rows=[location_code])
    else:
        return 'something wrong'


@common.route('/get_low_adm_cds', methods=['GET', 'POST'])
def get_low_adm_cds():
    print('get_low_adm_cds')
    location_depth = request.form.get('locationDepth')
    location_code = request.form.get('locationCode')

    if location_depth == 'sid':
        codes = AdmAreaMaster.find_sggs_by_sid_cd(location_code)

        result = []
        for location_code in codes:
            result.append(location_code[0])

        return render_json(200, rows=result)

    elif location_depth == 'sgg':
        codes = AdmAreaMaster.find_emds_by_sgg_cd(location_code)

        result = []
        for location_code in codes:
            result.append(location_code[0])

        return render_json(200, rows=result)

    elif location_depth == 'emd':
        return render_json(200, rows=[location_code])
    else:
        return 'something wrong'