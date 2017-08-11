# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, current_app, json, jsonify
from flask_login import login_required

from hms.blueprints.situation.models.popltn_mvmt import PopltnMvmt
from hms.blueprints.situation.models.hshold_stats import HsholdStats
from hms.blueprints.situation.models.popltn_stats import PopltnStats
from hms.blueprints.situation.models.trnstn_situtn import TrnstnSitutn
from lib.util_json import render_json

import datetime

situation = Blueprint('situation', __name__,
                      template_folder='templates', url_prefix='/situation')


@situation.before_request
@login_required
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    pass


@situation.route('', methods=['GET', 'POST'])
def index():
    return render_template('situation/index.html', now=datetime.datetime.now())


@situation.route('/srch_popltn_mvmt', methods=['POST'])
def srch_popltn_mvmt():
    # 인구이동 검색
    out_sid_cds = request.form.getlist('out_sid_cd')
    out_sgg_cds = request.form.getlist('out_sgg_cd')
    out_emd_cds = request.form.getlist('out_emd_cd')
    in_sid_cd = request.form.get('in_sid_cd')
    in_sgg_cd = request.form.get('in_sgg_cd')
    in_emd_cd = request.form.get('in_emd_cd')
    mv_reasn_cds = request.form.getlist('mv_reasn_cd')
    aplcnt_ages = request.form.getlist('aplcnt_age', type=int)
    aplcnt_sex_cds = request.form.getlist('aplcnt_sex_cd')
    fmly_nums = request.form.getlist('fmly_num', type=int)
    st_yyyymm = request.form.get('st_year') + request.form.get('st_month')
    ed_yyyymm = request.form.get('ed_year') + request.form.get('ed_month')

    # 지도 출력
    if request.form.get('req_type') == 'map':
        items = PopltnMvmt.find_by_filter_for_map(out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd,
                                                  in_emd_cd,
                                                  mv_reasn_cds, aplcnt_ages, aplcnt_sex_cds, fmly_nums, st_yyyymm,
                                                  ed_yyyymm)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'hshold_cnt': item.hshold_cnt,
            'fmly_sum': item.fmly_sum
        } for item in items])

    # 그리드 출력
    items = PopltnMvmt.find_by_filter_for_grid(out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd,
                                               in_emd_cd, mv_reasn_cds, aplcnt_ages, aplcnt_sex_cds, fmly_nums,
                                               st_yyyymm, ed_yyyymm)

    return jsonify({
        'rows': [{
            'in_yyyymm': item.in_yyyymm,
            'in_sid': item.in_sid,
            'in_sgg': item.in_sgg,
            'in_emd': item.in_emd,
            'out_sid': item.out_sid,
            'out_sgg': item.out_sgg,
            'out_emd': item.out_emd,
            'mv_reasn': item.mv_reasn,
            'aplcnt_clsftn': item.aplcnt_clsftn,
            'aplcnt_age': item.aplcnt_age,
            'aplcnt_sex': item.aplcnt_sex,
            'fmly_num': item.fmly_num
        } for item in items]
    })


@situation.route('/srch_hshold_stats', methods=['POST'])
def srch_hshold_stats():
    # 세대통계 검색
    sid_cds = request.form.getlist('sid_cd')
    sgg_cds = request.form.getlist('sgg_cd')
    rsdnc_clsftn_cds = request.form.getlist('rsdnc_clsftn_cd')
    fmly_num_cds = request.form.getlist('fmly_num_cd')
    room_num_cds = request.form.getlist('room_num_cd')
    st_year = request.form.get('st_year')
    ed_year = request.form.get('ed_year')

    # 지도 출력
    if request.form.get('req_type') == 'map':
        items = HsholdStats.find_by_filter_for_map(sid_cds, sgg_cds, rsdnc_clsftn_cds,
                                                   fmly_num_cds, room_num_cds, st_year, ed_year)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'hshold_sum': item.hshold_sum
        } for item in items])

    # 그리드 출력
    items = PopltnMvmt.find_by_filter_for_grid(sid_cds, sgg_cds, rsdnc_clsftn_cds,
                                               fmly_num_cds, room_num_cds, st_year, ed_year)

    return jsonify({
        'rows': [{
            'srvy_year': item.srvy_year,
            'sid': item.sid,
            'sgg': item.sgg,
            'rsdnc_clsftn': item.rsdnc_clsftn,
            'fmly_num': item.fmly_num,
            'room_num': item.room_num,
            'hshold_num': item.hshold_num
        } for item in items]
    })


@situation.route('/srch_popltn_stats', methods=['POST'])
def srch_popltn_stats():
    # 인구통계 검색
    sido_cds = request.form.getlist('ps-sido')
    sigu_cds = request.form.getlist('ps-sigu')
    emd_cds = request.form.getlist('ps-emd')
    age_cds = request.form.getlist('ps-age')
    sex_cds = request.form.getlist('ps-sex')
    syear = request.form.get('ps-syear')
    smonth = request.form.get('ps-smonth')
    eyear = request.form.get('ps-eyear')
    emonth = request.form.get('ps-emonth')

    rs = PopltnStats.select_all(sido_cds, sigu_cds, emd_cds, age_cds, syear, smonth, eyear, emonth)

    if rs is None:
        return render_json(401, {'msg': '검색 중 오류가 발생하였습니다.'})

    return render_json(200, items=[{
        'area_nm': item.area_nm,
        'man_sum': item.man_sum,
        'woman_sum': item.woman_sum,
        'total_sum': item.total_sum
    } for item in rs])


@situation.route('/srch_trnstn_situtn', methods=['POST'])
def srch_trnstn_situtn():
    # 실거래가 검색
    dong_cd = request.args.get('dong_cd')

    prices = TrnstnSitutn.query.filter(TrnstnSitutn.dong_cd == dong_cd)

    return render_json(200, items=[{
        'dong_cd': item.dong_cd,
        'zone_main': item.zone_main,
        'zone_sub': item.zone_sub,
        'dong_kor': item.dong_kor,
        'doro_addre': item.doro_addre,
        'building_k': item.building_k,
        'cl': item.cl,
        'year_build': item.year_build,
        'floor': item.floor,
        'issue': item.issue,
        'date_contr': item.date_contr,
        'using_area': item.using_area,
        'price': item.price
    } for item in prices])
