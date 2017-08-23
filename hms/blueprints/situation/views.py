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
# 인구이동 검색
def srch_popltn_mvmt():
    out_sid_cds = request.form.getlist('out_sid_cd')
    out_sgg_cds = request.form.getlist('out_sgg_cd')
    out_emd_cds = request.form.getlist('out_emd_cd')
    in_sid_cd = request.form.get('in_sid_cd')
    in_sgg_cd = request.form.get('in_sgg_cd')
    in_emd_cd = request.form.get('in_emd_cd')
    mv_reasn_cds = request.form.getlist('mv_reasn_cd')
    aplcnt_age_cds = request.form.getlist('aplcnt_age_cd', type=int)
    aplcnt_sex_cds = request.form.getlist('aplcnt_sex_cd')
    fmly_nums = request.form.getlist('fmly_num', type=int)
    st_yyyymm = request.form.get('st_year') + request.form.get('st_month')
    ed_yyyymm = request.form.get('ed_year') + request.form.get('ed_month')

    # 지도 출력
    if request.form.get('req_type') == 'map':
        items = PopltnMvmt.find_by_filter_for_map(out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd,
                                                  in_emd_cd,
                                                  mv_reasn_cds, aplcnt_age_cds, aplcnt_sex_cds, fmly_nums, st_yyyymm,
                                                  ed_yyyymm)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'hshold_cnt': item.hshold_cnt,
            'fmly_sum': item.fmly_sum
        } for item in items])

    # 그리드 출력
    items = PopltnMvmt.find_by_filter_for_grid(out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd,
                                           in_emd_cd, mv_reasn_cds, aplcnt_age_cds, aplcnt_sex_cds, fmly_nums,
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

@situation.route('/srch_popltn_stats', methods=['POST'])
# 인구통계 검색
def srch_popltn_stats():
    print("*" * 100)
    print(request.form.get('sid_cd'))
    print(request.form.get('sgg_cd'))
    print(request.form.get('emd_cd'))
    print(request.form.getlist('age_grp_cd'))
    print(request.form.get('ps_syear'))
    print(request.form.get('ps_smonth'))
    print(request.form.get('ps_eyear'))
    print(request.form.get('ps_emonth'))
    print("*" * 100)

    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')
    age_grp_cds = request.form.getlist('age_grp_cd')
    # ps_sex_cds = request.form.getlist('ps-sex', type=int)
    # total_num = request.form.get('total_num', type=int)
    st_yyyymm = request.form.get('ps_syear') + request.form.get('ps_smonth')
    ed_yyyymm = request.form.get('ps_eyear') + request.form.get('ps_emonth')

    # 지도 출력
    if request.form.get('req_type') == 'map':
        items = PopltnStats.find_by_filter_for_map(sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm,
                                                   ed_yyyymm)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            # 'local_name': item.local_name,
            # 'man_num': item.man_num,
            # 'woman_num': item.woman_num,
            'total_num': item.total_num
        } for item in items])

    # 그리드 출력

    items = PopltnStats.find_by_filter_for_grid(sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm,
                                                ed_yyyymm)
    print("*" * 100)
    print(items)
    print("*" * 100)

    return jsonify({
        'data': [[
            item.srvy_yyyymm,
            item.sid,
            item.sgg,
            item.emd,
            item.age_grp,
            item.man_num,
            item.woman_num,
            item.total_num,
        ] for item in items]
    })

    # rs = PopltnStats.select_all(sido_cds, sigu_cds, emd_cds, age_cds, syear, smonth, eyear, emonth)
    #
    # if rs is None:
    #     return render_json(401, {'msg': '검색 중 오류가 발생하였습니다.'})

    # return render_json(200, items=[{
    #     'area_nm': item.area_nm,
    #     'man_num': item.man_num,
    #     'woman_num': item.woman_num,
    #     'total_num': item.total_num
    # } for item in rs])

# 세대통계 검색
@situation.route('/srch_hshold_stats', methods=['POST'])
def srch_hshold_stats():
    sid_cds = request.form.getlist('sid_cd')
    sgg_cds = request.form.getlist('sgg_cd')
    rsdnc_clsftn_cds = request.form.getlist('rsdnc_clsftn_cd')
    fmly_num_cds = request.form.getlist('fmly_num_cd')
    room_num_cds = request.form.getlist('room_num_cd')
    st_year = request.form.get('st_year')
    ed_year = request.form.get('ed_year')

    print("*" * 100)
    print(sid_cds)
    print(sgg_cds)
    print(rsdnc_clsftn_cds)
    print(fmly_num_cds)
    print(room_num_cds)
    print(st_year)
    print(ed_year)
    print("*" * 100)

    # 지도 출력
    if request.form.get('req_type') == 'map':
        items = HsholdStats.find_by_filter_for_map(sid_cds, sgg_cds, rsdnc_clsftn_cds,
                                                   fmly_num_cds, room_num_cds, st_year, ed_year)

        for item in items:
            print("*" * 100)
            print('ssssssssssssssssssssssssss')
            print(item)
            print("*" * 100)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'hshold_sum': item.hshold_sum
        } for item in items])

    # 그리드 출력
    items = HsholdStats.find_by_filter_for_grid(sid_cds, sgg_cds, rsdnc_clsftn_cds,
                                               fmly_num_cds, room_num_cds, st_year, ed_year)

    for item in items:
        print("*" * 100)
        print(item)
        print("*" * 100)

    return jsonify({
        'data': [{
            'srvy_year': item.srvy_year,
            'sid': item.sid_cd,
            'sgg': item.sgg_cd,
            'rsdnc_clsftn': item.rsdnc_clsftn_cd,
            'fmly_num': item.fmly_num_cd,
            'room_num': item.room_num_cd,
        } for item in items]
    })


@situation.route('/srch_trnstn_situtn', methods=['POST'])
# 실거래가 검색
def srch_trnstn_situtn():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')
    trnstn_clsftn_cd = request.form.get('mp-trans-type')
    house_clsftn_cd = request.form.get('mp-house-kind')
    st_sale_price = request.form.get('mp-ssale')
    ed_sale_price = request.form.get('mp-esale')
    st_deposit = request.form.get('mp-sdeposit')
    ed_deposit = request.form.get('mp-edeposit')
    st_mnthly_rent = request.form.get('mp-srent')
    ed_mnthly_rent = request.form.get('mp-erent')
    st_exclsv_area = request.form.get('mp-sexarea')
    ed_exclsv_area = request.form.get('mp-eexarea')
    st_decrepit = request.form.get('mp-sdecrepit')
    ed_decrepit = request.form.get('mp-edecrepit')
    st_yyyymm = request.form.get('mp-syear')+request.form.get('mp-smonth')
    ed_yyyymm = request.form.get('mp-eyear')+request.form.get('mp-emonth')

    # 지도 출력
    if request.form.get('req_type') == 'map':


        items = TrnstnSitutn.find_by_filter_for_map(sid_cd, sgg_cd, emd_cd, trnstn_clsftn_cd, house_clsftn_cd,
                                                    st_sale_price, ed_sale_price, st_deposit, ed_deposit,
                                                    st_mnthly_rent, ed_mnthly_rent,st_exclsv_area, ed_exclsv_area,
                                                    st_decrepit, ed_decrepit, st_yyyymm, ed_yyyymm)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojsonForBuild)['coordinates'],
            'id': item.id
        } for item in items])

    # 그리드 출력

    # items = TrnstnSitutn.find_by_filter_for_grid(sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm,
    #                                             ed_yyyymm)
    #
    # return jsonify({
    #     'rows': [{
    #         'srvy_yyyymm': item.srvy_yyyymm,
    #         'sid': item.sid,
    #         'sgg': item.sgg,
    #         'emd': item.emd,
    #         'age_grp': item.age_grp,
    #         'man_num': item.man_num,
    #         'woman_num': item.woman_num,
    #         'total_num': item.total_num,
    #     } for item in items]
    #
    # })

@situation.route('/srch_busins_situtn', methods=['POST'])
def srch_busins_situtn():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')
    busins_clsftn_cd = request.form.getlist('busins_clsftn_cd')

    print("8" * 20)
    print(sid_cd)
    print(sgg_cd)
    print(emd_cd)
    print(busins_clsftn_cd)
    print("8" * 20)

