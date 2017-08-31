# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, current_app, json, jsonify
from flask_login import login_required

from hms.blueprints.situation.models.popltn_mvmt import PopltnMvmt
from hms.blueprints.situation.models.hshold_stats import HsholdStats
from hms.blueprints.situation.models.popltn_stats import PopltnStats
from hms.blueprints.situation.models.trnstn_situtn import TrnstnSitutn
from hms.blueprints.situation.models.idnftn_bldng import IdnftnBldng
from hms.blueprints.situation.models.busins_situtn import BusinsSitutn
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
            'mv_reasn': item.my_reasn,
            'aplcnt_clsftn': item.aplcnt_clsftn,
            'aplcnt_age': item.aplcnt_age,
            'aplcnt_sex': item.aplcnt_sex,
            'fmly_num': item.fmly_num
        } for item in items]

    })

@situation.route('/srch_popltn_stats', methods=['POST'])
# 인구통계 검색
def srch_popltn_stats():
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

    return jsonify({
        'rows': [{
            'srvy_yyyymm': item.srvy_yyyymm,
            'sid': item.sid,
            'sgg': item.sgg,
            'emd': item.emd,
            'age_grp': item.age_grp,
            'man_num': item.man_num,
            'woman_num': item.woman_num,
            'total_num': item.total_num,
       } for item in items]
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

    # 지도 출력
    if request.form.get('req_type') == 'map':
        items = HsholdStats.find_by_filter_for_map(sid_cds, sgg_cds, rsdnc_clsftn_cds,
                                                   fmly_num_cds, room_num_cds, st_year, ed_year)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'hshold_sum': item.hshold_sum
        } for item in items])

    # 그리드 출력
    items = HsholdStats.find_by_filter_for_grid(sid_cds, sgg_cds, rsdnc_clsftn_cds,
                                               fmly_num_cds, room_num_cds, st_year, ed_year)

    # for item in items:
    #     print("*" * 100)
    #     print(item)
    #     print("*" * 100)

    return jsonify({
        'rows': [{
            'srvy_year': item.srvy_year,
            'sid': item.sid,
            'sgg': item.sgg,
            'rsdnc_clsftn': item.rsdnc_clsftn_cd,
            'fmly_num': item.fmly_num_cd,
            'room_num': item.room_num_cd,
            'hshold_num': item.hshold_num,
        } for item in items]
    })


@situation.route('/srch_trnstn_situtn', methods=['POST'])
# 실거래가 검색
def srch_trnstn_situtn():
    # TODO : 이거 네임 값이랑 변수 이름이랑 웬만하면 맞춰주자.!

    sid_cd = request.form.get('sid_cd')                        #시도 코드
    sgg_cd = request.form.get('sgg_cd')                         #시군구 코드
    emd_cd = request.form.get('emd_cd')                        #읍면동 코드
    mp_trans_type = request.form.get('mp-trans-type')           #전월세 매매 구분
    mp_house_kind = request.form.get('mp-house-kind')           # 건물 종류

    mp_ssale = ''
    mp_esale = ''
    mp_sexarea = ''
    mp_eexarea = ''
    mp_sdecrepit = ''
    mp_edecrepit = ''
    mp_sdeposit = ''
    mp_edeposit = ''
    mp_srent = ''
    mp_erent = ''

    #매매
    if mp_trans_type == "1":
        mp_ssale = request.form.get('mp-ssale')  # 매매가 시작
        mp_esale = request.form.get('mp-esale')  # 매매가 종료
        mp_sexarea = request.form.get('mp-sexarea')  # 면적 시작
        mp_eexarea = request.form.get('mp-eexarea')  # 면적 종료
        mp_sdecrepit = request.form.get('mp-sdecrepit')  # 노후도 시작
        mp_edecrepit = request.form.get('mp-edecrepit')  # 노후도 종료
    # 전월세
    elif mp_trans_type == "2":
        mp_sdeposit = request.form.get('mp-sdeposit')  # 보증금 시작
        mp_edeposit = request.form.get('mp-edeposit')  # 보증금 종료
        mp_srent = request.form.get('mp-srent')  # 월세 시작
        mp_erent = request.form.get('mp-erent')  # 월세 종료
        mp_sexarea = request.form.get('mp-sexarea')  # 면적 시작
        mp_eexarea = request.form.get('mp-eexarea')  # 면적 종료
        mp_sdecrepit = request.form.get('mp-sdecrepit')  # 노후도 시작
        mp_edecrepit = request.form.get('mp-edecrepit')  # 노후도 종료

    st_yyyymm = request.form.get('mp-syear') + request.form.get('mp-smonth')    #시작년,월
    ed_yyyymm = request.form.get('mp-eyear') + request.form.get('mp-emonth')    #종료년, 월

    # mp_ss = request.form.get('mp-ss')                        #매매가 시작       selectBox 값
    # mp_es = request.form.get('mp-es')                        #매매가 종료       selectBox 값
    # mp_sdep = request.form.get('mp-sdep')                     #보증금 시작      selectBox 값
    # mp_edep = request.form.get('mp-edep')                     #보증금 종료      selectBox 값
    # mp_sre = request.form.get('mp-sre')                         #월세 시작      selectBox 값
    # mp_ere = request.form.get('mp-ere')                         #월세 종료      selectBox 값
    # mp_sarea = request.form.get('mp-sarea')                     #면적 시작      selectBox 값
    # mp_earea = request.form.get('mp-earea')                     #면적 종료      selectBox 값
    # mp_sdec = request.form.get('mp-sdec')                       #노후도 시작 selectBox 값
    # mp_edec = request.form.get('mp-edec')                       #노후도 종료 selectBox 값

    # house_clsftn_cd = request.form.get('mp-house-kind')
    # st_sale_price = request.form.get('mp-ssale')
    # ed_sale_price = request.form.get('mp-esale')
    # st_deposit = request.form.get('mp-sdeposit')
    # ed_deposit = request.form.get('mp-edeposit')
    # st_mnthly_rent = request.form.get('mp-srent')
    # ed_mnthly_rent = request.form.get('mp-erent')
    # st_exclsv_area = request.form.get('mp-sarea')
    # ed_exclsv_area = request.form.get('mp-earea')
    # st_decrepit = request.form.get('mp-sdecrepit')
    # ed_decrepit = request.form.get('mp-edecrepit')
    # st_yyyymm = request.form.get('mp-syear')+request.form.get('mp-smonth')
    # ed_yyyymm = request.form.get('mp-eyear')+request.form.get('mp-emonth')

    # 지도 출력
    if request.form.get('req_type') == 'map':

        if mp_trans_type == "1":
            print('buy')
            items = TrnstnSitutn.find_by_filter_for_buy_map(sid_cd, sgg_cd, emd_cd, mp_trans_type, mp_house_kind, mp_ssale, mp_esale,
                                                            mp_sexarea, mp_eexarea, mp_sdecrepit, mp_edecrepit, st_yyyymm, ed_yyyymm)
        else:
            print('monthy_rent')
            items = TrnstnSitutn.find_by_filter_for_rent_map(sid_cd, sgg_cd, emd_cd, mp_trans_type, mp_house_kind, mp_sdeposit, mp_edeposit,
                                                             mp_srent, mp_erent, mp_sexarea, mp_eexarea, mp_sdecrepit, mp_edecrepit,
                                                             st_yyyymm, ed_yyyymm)

        return render_json(200, rows=[{
            'trnstn_clsftn_cd': item.trnstn_clsftn_cd,
            'sid_cd': item.sid_cd,
            'sgg_cd': item.sgg_cd,
            'emd_cd': item.emd_cd,
            'lat': item.x,
            'lan': item.y,
        } for item in items])

    # 그리드 출력
    else:
        if mp_trans_type == "1":
            print('buy')
            items = TrnstnSitutn.find_by_filter_for_buy_grid(sid_cd, sgg_cd, emd_cd, mp_trans_type, mp_house_kind,
                                                            mp_ssale, mp_esale,
                                                            mp_sexarea, mp_eexarea, mp_sdecrepit, mp_edecrepit,
                                                            st_yyyymm, ed_yyyymm)
        else:
            items = TrnstnSitutn.find_by_filter_for_rent_grid(sid_cd, sgg_cd, emd_cd, mp_trans_type, mp_house_kind,
                                                             mp_sdeposit, mp_edeposit,
                                                             mp_srent, mp_erent, mp_sexarea, mp_eexarea, mp_sdecrepit,
                                                             mp_edecrepit,
                                                             st_yyyymm, ed_yyyymm)
        for item in items:
            print(item)

        return render_json(200, rows=[{
            'trnstn_clsftn_cd': item.trnstn_clsftn_cd,
            'sid': item.sid,
            'sgg': item.sgg,
            'emd': item.emd,
            'lat': item.x,
            'lan': item.y,
        } for item in items])

# 건물 현황 검색
@situation.route('/srch_idnfln_bldng', methods=['POST'])
def srch_idnfln_bldng():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')
    ib_use = request.form.getlist('ib-use')
    ib_common = request.form.getlist('ib-common')
    ib_sarea = request.form.get('ib-sarea')
    ib_sexarea = request.form.get('ib-sexarea')
    ib_earea = request.form.get('ib-earea')
    ib_eexarea = request.form.get('ib-eexarea')
    ib_sdec = request.form.get('ib-sdec')
    ib_sdecrepit = request.form.get('ib-sdecrepit')
    ib_edec = request.form.get('ib-edec')
    ib_edecrepit = request.form.get('ib-edecrepit')
    st_yyyymm = request.form.get('ib-syear') + request.form.get('ib-smonth')
    ed_yyyymm = request.form.get('ib-eyear') + request.form.get('ib-emonth')

    # 지도 출력
    if request.form.get('req_type') == 'map':
        items = IdnftnBldng.find_by_filter_for_map(sid_cd, sgg_cd, emd_cd, ib_use, ib_common, ib_sarea, ib_sexarea, ib_earea,
                                                       ib_eexarea, ib_sdec, ib_sdecrepit, ib_edec, ib_edecrepit,
                                                       st_yyyymm, ed_yyyymm)
        for item in items :
            print(item)

        return render_json(200, rows=[{
            'main_num': item.main_num,
            'sid_cd': item.sid_cd,
            'sgg_cd': item.sgg_cd,
            'emd_cd': item.emd_cd,
            'lat': item.x,
            'lan': item.y,
        } for item in items])

    items = IdnftnBldng.find_by_filter_for_grid(sid_cd, sgg_cd, emd_cd, ib_use, ib_common, ib_sarea, ib_sexarea, ib_earea,
                                                       ib_eexarea, ib_sdec, ib_sdecrepit, ib_edec, ib_edecrepit,
                                                       st_yyyymm, ed_yyyymm)
    return render_json(200, rows=[{
        'sid_cd': item.sid_cd,
        'sgg_cd': item.sgg_cd,
        'emd_cd': item.emd_cd,
        'prcl_addrs': item.prcl_addrs,
        'road_addrs': item.road_addrs,
    } for item in items])


@situation.route('/srch_busins_situtn', methods=['POST'])
def srch_busins_situtn():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')
    busins_clsftn_cd = request.form.getlist('busins_clsftn_cd')

    if request.form.get('req_type') == 'map':
        items = BusinsSitutn.find_by_filter_for_map(sid_cd, sgg_cd, emd_cd, busins_clsftn_cd)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'busins_clsftn_cd': item.busins_clsftn_cd
        } for item in items])

    items = BusinsSitutn.find_by_filter_for_grid(sid_cd, sgg_cd, emd_cd, busins_clsftn_cd)

    return render_json(200, rows=[{
        'sid': item.sid,
        'sgg': item.sgg,
        'emd': item.emd,
        'lcnsng_dt': item.lcnsng_dt,
        'busins_clsftn_cd': item.busins_clsftn_cd,
        'busins_condtn': item.busins_condtn,
        'loctn_area': item.loctn_area,
        'compny_nm': item.compny_nm,
        'prcl_zipcd': item.prcl_zipcd,
        'prcl_addrs': item.prcl_addrs,
        'road_zipcd': item.road_zipcd,
        'road_addrs': item.road_addrs,
        'loctn_phone': item.loctn_phone
    } for item in items])


