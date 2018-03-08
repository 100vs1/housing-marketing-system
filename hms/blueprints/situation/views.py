# -*- coding: utf-8 -*-

import datetime

from flask import Blueprint, render_template, request, current_app, json, jsonify
from flask_login import login_required, current_user
from hms.blueprints.common.models.area import AdmSidArea, AdmSggArea, AdmEmdArea, LawSidArea, LawSggArea, LawEmdArea

from hms.blueprints.rest_api.models.livyAPI import LivyAPI
from hms.blueprints.rest_api.models.vWordlAPI import VWorldAPI
from hms.blueprints.situation.models.busins_situtn import BusinsSitutn
from hms.blueprints.situation.models.hshold_imgrat import HsholdImgrat
from hms.blueprints.situation.models.hshold_stats import HsholdStats
from hms.blueprints.situation.models.idnftn_bldng import IdnftnBldng
from hms.blueprints.situation.models.income_situtn_company import IncomeSitutnCompany
from hms.blueprints.situation.models.pivot_busins_situtn import PivotBusinsSitutn
from hms.blueprints.situation.models.popltn_mvmt import PopltnMvmt
from hms.blueprints.situation.models.popltn_stats import PopltnStats
from hms.blueprints.situation.models.presto_db import PrestoTest
from hms.blueprints.situation.models.supply_present import SupplyPresent
from hms.blueprints.situation.models.supply_present_new import SupplyPresentNew
from hms.blueprints.situation.models.trnstn_situtn import TrnstnSitutn
from hms.blueprints.situation.models.trnstn_situtn_supply import TrnstnSitutnSupply
from hms.blueprints.situation.models.user_marker import UserMarkers
# from ctree.blueprints.common.models.file import Files
from lib.util_json import render_json

situation = Blueprint('situation', __name__,
                      template_folder='templates', url_prefix='/situation')


@situation.before_request
@login_required
def before_request():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data())
    current_app.logger.debug('URL: %s', request)
    pass


@situation.route('', methods=['GET', 'POST'])
def index():
    # return render_template('situation/index.html', now=datetime.datetime.now())
    return render_template('situation/index_obsolate.html', now=datetime.datetime.now())


@situation.route('/srch_popltn_stats', methods=['POST'])
# 인구통계 검색
def srch_popltn_stats():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')
    age_grp_cds = request.form.getlist('ps_age_grp_cd')
    st_yyyymm = request.form.get('ps_syear') + request.form.get('ps_smonth')
    ed_yyyymm = request.form.get('ps_eyear') + request.form.get('ps_emonth')
    req_type = request.form.get('req_type')

    # 데이터 체크
    if req_type == 'check':
        items = PopltnStats.find_by_filter_for_check(sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm, ed_yyyymm)

        return render_json(200, count=items)

    # 지도 출력
    if req_type == 'map':
        items = PopltnStats.find_by_filter_for_map(sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm, ed_yyyymm)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'total_num': item.total_num
        } for item in items])

    # 버블 맵
    if req_type == 'bubble':
        start_items = PopltnStats.find_by_filter_for_bubble(sid_cd, sgg_cd, emd_cd, st_yyyymm, age_grp_cds)

        end_items = PopltnStats.find_by_filter_for_bubble(sid_cd, sgg_cd, emd_cd, ed_yyyymm, age_grp_cds)

        start_result = []
        for item in start_items:
            if item.geojson:
                start_result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })

        end_result = []
        for item in end_items:
            if item.geojson:
                end_result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })

        return render_json(200, rows={"start_result": start_result, "end_result": end_result})

    if req_type == 'grid':
        items = PrestoTest.find_for_popltn_stats_pivot(sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm, ed_yyyymm)

        ret = []
        col = items.get('cols').split(", ")

        for idx, row in enumerate(items.get('rows')):
            temp_dict = {}
            for idxx, item in enumerate(row):
                temp_dict[col[idxx]] = item

            ret.append(temp_dict)

        return render_json(200, {'rows': ret, 'cols': col})


# 인구주택총조사 검색
@situation.route('/srch_hshold_stats', methods=['POST'])
def srch_hshold_stats():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    fmly_num_cds = request.form.getlist('hs_fmly_num_cd')
    rsdnc_clsftn_cds = request.form.getlist('hs_rsdnc_clsftn_cd')
    room_num_cds = request.form.getlist('hs_room_num_cd')
    hs_syear = request.form.get('hs_syear')
    hs_eyear = request.form.get('hs_eyear')
    req_type = request.form.get('req_type')

    # 데이터 체크
    if req_type == 'check':
        items = HsholdStats.find_by_filter_for_check(sid_cd, sgg_cd, rsdnc_clsftn_cds, fmly_num_cds, room_num_cds,
                                                     hs_syear, hs_eyear)

        return render_json(200, count=items)

    # 지도 출력
    if req_type == 'map':
        items = HsholdStats.find_by_filter_for_map(sid_cd, sgg_cd, rsdnc_clsftn_cds,
                                                   fmly_num_cds, room_num_cds, hs_syear, hs_eyear)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'hshold_sum': item.hshold_sum,
        } for item in items])

    # 버블 맵
    if req_type == 'bubble':
        items = HsholdStats.find_by_filter_for_bubble(sid_cd, sgg_cd, rsdnc_clsftn_cds,
                                                      fmly_num_cds, room_num_cds, hs_syear, hs_eyear)

        result = []
        for item in items:
            if item.geojson is not None:
                result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })

        return render_json(200, rows=result)

    # 피벗 테이블
    if req_type == 'grid':
        rsdnc_clsftn = [];
        for cd in rsdnc_clsftn_cds:
            rsdnc_clsftn.append(int(cd))

        fmly_num = [];
        for cd in fmly_num_cds:
            fmly_num.append(int(cd))

        room_num = [];
        for cd in room_num_cds:
            room_num.append(int(cd))

        items = PrestoTest.find_for_hshold_stats_pivot(sid_cd, sgg_cd,
                                                       rsdnc_clsftn, fmly_num, room_num,
                                                       hs_syear, hs_eyear)
        ret = []
        col = items.get('cols').split(", ")
        for idx, item in enumerate(items.get('rows')):
            hehe = {}
            for idxx, hoho in enumerate(item):
                hehe[col[idxx]] = hoho

            ret.append(hehe)

        return render_json(200, {'rows': ret, 'cols': col})


@situation.route('/srch_popltn_mvmt', methods=['POST'])
# 인구이동 검색
def srch_popltn_mvmt():
    # 전출 시도 코드
    out_sid_cds = request.form.get('out_sid_cd')
    # 전출 시군구 코드
    out_sgg_cds = request.form.get('out_sgg_cd')
    # 전출 읍면동 코드
    out_emd_cds = request.form.get('out_emd_cd')
    # 전입 시도 코드
    in_sid_cd = request.form.get('in_sid_cd')
    # 전입 시군구 코드
    in_sgg_cd = request.form.get('in_sgg_cd')
    # 전입 읍면동 코드
    in_emd_cd = request.form.get('in_emd_cd')

    # 연령대
    aplcnt_age_cds = request.form.getlist('pm_aplcnt_age_cd')
    # 이동사유
    mv_reasn_cds = request.form.getlist('pm_mv_reasn_cd')
    # 세대수
    fmly_nums = request.form.getlist('pm_fmly_num_cd', type=int)

    # 시작 년월
    pm_syyyymm = request.form.get('pm_syear') + request.form.get('pm_smonth')
    # 종료 년월
    pm_eyyyymm = request.form.get('pm_eyear') + request.form.get('pm_emonth')
    req_type = request.form.get('req_type')

    # 데이터 체크
    if req_type == 'check':
        items = PopltnMvmt.find_by_filter_for_check(out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd,
                                                    in_emd_cd, mv_reasn_cds, aplcnt_age_cds, fmly_nums, pm_syyyymm,
                                                    pm_eyyyymm)
        return render_json(200, count=items)

    # 지도 출력
    if req_type == 'map':
        items = PopltnMvmt.find_by_filter_for_map(out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd,
                                                  in_emd_cd, mv_reasn_cds, aplcnt_age_cds, fmly_nums, pm_syyyymm,
                                                  pm_eyyyymm)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'hshold_cnt': item.hshold_cnt,
            'fmly_sum': item.fmly_sum
        } for item in items])

    # 버블 맵
    if req_type == 'bubble':
        items = PopltnMvmt.find_by_filter_for_bubble(out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd, in_emd_cd,

                                                     mv_reasn_cds, aplcnt_age_cds, fmly_nums, pm_syyyymm, pm_eyyyymm)

        result = []
        for item in items:
            if item.geojson is not None:
                result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })

        return render_json(200, rows=result)

    # 그리드 출력
    if req_type == 'grid':
        # mv_reasn = []
        # for cd in mv_reasn_cds:
        #     mv_reasn.append(int(cd))

        dt = datetime.datetime.now()
        print(dt.microsecond)

        items = PrestoTest.find_for_popltn_mvmt(out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd,
                                                in_emd_cd, mv_reasn_cds, aplcnt_age_cds, fmly_nums,
                                                pm_syyyymm, pm_eyyyymm)

        ret = []
        col = items.get('cols').split(", ")
        for idx, row in enumerate(items.get('rows')):
            temp_dict = {}
            for idxx, item in enumerate(row):
                temp_dict[col[idxx]] = item

            ret.append(temp_dict)

        return render_json(200, {'rows': ret, 'cols': col})

# 수요분석 - 거래량
@situation.route('/srch_trnstn_situtn_trans', methods=['POST'])
def srch_trnstn_situtn_trans():
    # 시도 코드
    sid_cd = request.form.get('sid_cd')
    # 시군구 코드
    sgg_cd = request.form.get('sgg_cd')
    # 읍면동 코드
    emd_cd = request.form.get('emd_cd')

    # 매물종류(거래구분)
    tst_trans_type = request.form.get('tst_trans_type')
    # 주택구분(건물구분)
    tst_house_kind = request.form.get('tst_house_kind')
    # 매매가 시작
    tst_ssale = request.form.get('tst_ssale')
    # 매매가 종료
    tst_esale = request.form.get('tst_esale')
    # 보증금 시작
    tst_sdeposit = request.form.get('tst_sdeposit')
    # 보증금 종료
    tst_edeposit = request.form.get('tst_edeposit')
    # 월세 시작
    tst_srent = request.form.get('tst_srent')
    # 월세 종료
    tst_erent = request.form.get('tst_erent')
    # 면적 시작
    tst_sexarea = request.form.get('tst_sexarea')
    # 면적 종료
    tst_eexarea = request.form.get('tst_eexarea')
    # 노후도 시작
    tst_sdecrepit = request.form.get('tst_sdecrepit')
    # 노후도 종료
    tst_edecrepit = request.form.get('tst_edecrepit')

    # 시작년월
    # tst_syyyymm = request.form.get('tst_syear') + request.form.get('tst_smonth') + '00'
    tst_syyyymm = request.form.get('tst_syear') + request.form.get('tst_smonth')
    # 종료년월
    # tst_eyyyymm = request.form.get('tst_eyear') + request.form.get('tst_emonth') + '99'
    tst_eyyyymm = request.form.get('tst_eyear') + request.form.get('tst_emonth')

    req_type = request.form.get('req_type')

    if req_type == 'check':
        if tst_trans_type != '4':
            check = TrnstnSitutn.find_by_filter_for_check(
                sid_cd, sgg_cd, emd_cd,
                tst_trans_type, tst_house_kind,
                tst_ssale, tst_esale,
                tst_sdeposit, tst_edeposit,
                tst_srent, tst_erent,
                tst_sexarea, tst_eexarea,
                tst_sdecrepit, tst_edecrepit,
                tst_syyyymm, tst_eyyyymm
            )

            return render_json(200, hasData=check)

        else:
            check = TrnstnSitutnSupply.find_by_filter_for_check(
                sid_cd, sgg_cd, emd_cd,
                tst_ssale, tst_esale,
                tst_sexarea, tst_eexarea,
                tst_syyyymm, tst_eyyyymm)

            return render_json(200, hasData=check)

    if req_type == 'list':
        if tst_trans_type != '4':
            items = TrnstnSitutn.find_by_filter_for_list(
                sid_cd, sgg_cd, emd_cd,
                tst_trans_type, tst_house_kind,
                tst_ssale, tst_esale,
                tst_sdeposit, tst_edeposit,
                tst_srent, tst_erent,
                tst_sexarea, tst_eexarea,
                tst_sdecrepit, tst_edecrepit,
                tst_syyyymm, tst_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'address': item.address,
                        'bldng_ko_nm': item.bldng_ko_nm,
                        'geom': json.loads(item.geojson)['coordinates'],
                    })

            return render_json(200, rows=result)
        else:
            items = TrnstnSitutnSupply.find_by_filter_for_list(
                sid_cd, sgg_cd, emd_cd,
                tst_ssale, tst_esale,
                tst_sexarea, tst_eexarea,
                tst_syyyymm, tst_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'address': item.address,
                        'bldng_ko_nm': item.bldng_ko_nm,
                        'geom': json.loads(item.geojson)['coordinates'],
                    })
            return render_json(200, rows=result)

    # 지도 출력
    if req_type == 'map':
        if tst_trans_type != '4':
            items = TrnstnSitutn.find_by_filter_for_map(
                sid_cd, sgg_cd, emd_cd,
                tst_trans_type, tst_house_kind,
                tst_ssale, tst_esale,
                tst_sdeposit, tst_edeposit,
                tst_srent, tst_erent,
                tst_sexarea, tst_eexarea,
                tst_sdecrepit, tst_edecrepit,
                tst_syyyymm, tst_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'geom': json.loads(item.geojson)['coordinates'],
                        'trnstn_yyyymm_start': item.trnstn_yyyymm_start,
                        'trnstn_yyyymm_end': item.trnstn_yyyymm_end,
                        'house_clsftn_code': item.house_clsftn_code,
                        'trnstn_clsftn_code': item.trnstn_clsftn_code,
                        'build_year': item.build_year,
                        'sale_price': item.sale_price,
                        'cnstrtn_area': item.cnstrtn_area,
                        'mnthly_rent': item.mnthly_rent,
                        'converted_rent': item.converted_rent,
                        'deposit': item.deposit,
                        'trnstn_count': item.trnstn_count,
                        'trnstn_count_per_exclsv': item.trnstn_count_per_exclsv,
                        'house_count': item.house_count,
                        'floor': item.floor,
                        'house_count_per_exclsv': item.house_count_per_exclsv,
                        'sale_price_avg': item.sale_price_avg,
                        'price_avg_per_cnstrtn_area': item.price_avg_per_cnstrtn_area,
                        'junse_avg_per_cnstrtn_area': item.junse_avg_per_cnstrtn_area,
                        'exclsv_area': item.exclsv_area,
                        'mnthly_rent_avg': item.mnthly_rent_avg,
                        'deposit_avg': item.deposit_avg,
                        'junse_avg': item.junse_avg,
                        'earnings_rate': item.earnings_rate,
                        'bldng_ko_name': item.bldng_ko_name,
                        'address': item.address,
                        'road_address': item.road_address
                    })

            return render_json(200, rows=result)
        else:
            items = TrnstnSitutnSupply.find_by_filter_for_map(
                sid_cd, sgg_cd, emd_cd,
                tst_ssale, tst_esale,
                tst_sexarea, tst_eexarea,
                tst_syyyymm, tst_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'geom': json.loads(item.geojson)['coordinates'],
                        'trnstn_yyyymm_start': item.trnstn_yyyymm_start,
                        'trnstn_yyyymm_end': item.trnstn_yyyymm_end,
                        'supply_price': item.supply_price,
                        'cnstrtn_area': item.cnstrtn_area,
                        'exclsv_area': item.exclsv_area,
                        'trnstn_count': item.trnstn_count,
                        'trnstn_count_per_exclsv': item.trnstn_count_per_exclsv,
                        'house_count': item.house_count,
                        'house_count_per_exclsv': item.house_count_per_exclsv,
                        'floor': item.floor,
                        'supply_price_avg': item.supply_price_avg,
                        'supply_price_avg_per_cnstrtn_area': item.supply_price_avg_per_cnstrtn_area,
                        'bldng_ko_name': item.bldng_ko_name,
                        'address': item.address,
                    })
            return render_json(200, rows=result)

    if req_type == 'bubble':
        if tst_trans_type != '4':
            items = TrnstnSitutn.find_by_filter_for_trans_bubble(
                sid_cd, sgg_cd, emd_cd,
                tst_trans_type, tst_house_kind,
                tst_ssale, tst_esale,
                tst_sdeposit, tst_edeposit,
                tst_srent, tst_erent,
                tst_sexarea, tst_eexarea,
                tst_sdecrepit, tst_edecrepit,
                tst_syyyymm, tst_eyyyymm)

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'area_ko_nm': item.area_ko_nm,
                        'coordinates': json.loads(item.geojson)['coordinates'],
                        'total_sum': int(item.total_sum)
                    })

            return render_json(200, rows=result)

        else:
            items = TrnstnSitutnSupply.find_by_filter_for_trans_bubble(
                sid_cd, sgg_cd, emd_cd,
                tst_ssale, tst_esale,
                tst_sexarea, tst_eexarea,
                tst_syyyymm, tst_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'area_ko_nm': item.area_ko_nm,
                        'coordinates': json.loads(item.geojson)['coordinates'],
                        'total_sum': int(item.total_sum)
                    })

            return render_json(200, rows=result)
    if req_type == 'grid':
        if tst_trans_type != '4':
            items = PrestoTest.find_for_trnstn_situtn_count(
                sid_cd, sgg_cd, emd_cd,
                tst_ssale, tst_esale,
                tst_trans_type, tst_house_kind,
                tst_sexarea, tst_eexarea,
                tst_syyyymm, tst_eyyyymm)

            ret = []
            col = items.get('cols').split(", ")

            for idx, row in enumerate(items.get('rows')):
                temp_dict = {}
                for idxx, item in enumerate(row):
                    temp_dict[col[idxx]] = item

                ret.append(temp_dict)

            return render_json(200, {'rows': ret, 'cols': col})
        else:
            items = PrestoTest.find_for_supply_count_pivot(
                sid_cd, sgg_cd, emd_cd,
                tst_ssale, tst_esale,
                tst_trans_type, tst_house_kind,
                tst_sexarea, tst_eexarea,
                tst_syyyymm, tst_eyyyymm)

            ret = []
            col = items.get('cols').split(", ")
            for idx, row in enumerate(items.get('rows')):
                temp_dict = {}
                for idxx, item in enumerate(row):
                    temp_dict[col[idxx]] = item

                ret.append(temp_dict)

            return render_json(200, {'rows': ret, 'cols': col})


# 수요분석 - 가격
@situation.route('/srch_trnstn_situtn_price', methods=['POST'])
def srch_trnstn_situtn_price():
    # 시도 코드
    sid_cd = request.form.get('sid_cd')
    # 시군구 코드
    sgg_cd = request.form.get('sgg_cd')
    # 읍면동 코드
    emd_cd = request.form.get('emd_cd')

    # 매물종류(거래구분)
    tsp_trans_type = request.form.get('tsp_trans_type')
    # 주택구분(건물구분)
    tsp_house_kind = request.form.get('tsp_house_kind')
    # 매매가 시작
    tsp_ssale = request.form.get('tsp_ssale')
    # 매매가 종료
    tsp_esale = request.form.get('tsp_esale')
    # 보증금 시작
    tsp_sdeposit = request.form.get('tsp_sdeposit')
    # 보증금 종료
    tsp_edeposit = request.form.get('tsp_edeposit')
    # 월세 시작
    tsp_srent = request.form.get('tsp_srent')
    # 월세 종료
    tsp_erent = request.form.get('tsp_erent')
    # 면적 시작
    tsp_sexarea = request.form.get('tsp_sexarea')
    # 면적 종료
    tsp_eexarea = request.form.get('tsp_eexarea')
    # 노후도 시작
    tsp_sdecrepit = request.form.get('tsp_sdecrepit')
    # 노후도 종료
    tsp_edecrepit = request.form.get('tsp_edecrepit')

    # 디비 상에는 일자까지 포함하고 있어 각 수치에 00과 99를 더함
    # 시작년월
    tsp_syyyymm = request.form.get('tsp_syear') + request.form.get('tsp_smonth')
    # 종료년월
    tsp_eyyyymm = request.form.get('tsp_eyear') + request.form.get('tsp_emonth')

    req_type = request.form.get('req_type')

    if req_type == 'check':
        if tsp_trans_type != '4':
            check = TrnstnSitutn.find_by_filter_for_check(
                sid_cd, sgg_cd, emd_cd,
                tsp_trans_type, tsp_house_kind,
                tsp_ssale, tsp_esale,
                tsp_sdeposit, tsp_edeposit,
                tsp_srent, tsp_erent,
                tsp_sexarea, tsp_eexarea,
                tsp_sdecrepit, tsp_edecrepit,
                tsp_syyyymm, tsp_eyyyymm
            )
            return render_json(200, hasData=check)
        else:
            check = TrnstnSitutnSupply.find_by_filter_for_check(
                sid_cd, sgg_cd, emd_cd,
                tsp_ssale, tsp_esale,
                tsp_sexarea, tsp_eexarea,
                tsp_syyyymm, tsp_eyyyymm)

            return render_json(200, hasData=check)

    if req_type == 'list':
        if tsp_trans_type != '4':
            items = TrnstnSitutn.find_by_filter_for_list(
                sid_cd, sgg_cd, emd_cd,
                tsp_trans_type, tsp_house_kind,
                tsp_ssale, tsp_esale,
                tsp_sdeposit, tsp_edeposit,
                tsp_srent, tsp_erent,
                tsp_sexarea, tsp_eexarea,
                tsp_sdecrepit, tsp_edecrepit,
                tsp_syyyymm, tsp_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'address': item.address,
                        'bldng_ko_nm': item.bldng_ko_nm,
                        'geom': json.loads(item.geojson)['coordinates'],
                    })

            return render_json(200, rows=result)
        else:
            items = TrnstnSitutnSupply.find_by_filter_for_list(
                sid_cd, sgg_cd, emd_cd,
                tsp_ssale, tsp_esale,
                tsp_sexarea, tsp_eexarea,
                tsp_syyyymm, tsp_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'address': item.address,
                        'bldng_ko_nm': item.bldng_ko_nm,
                        'geom': json.loads(item.geojson)['coordinates'],
                    })
            return render_json(200, rows=result)

    # 지도 출력
    if req_type == 'map':
        if tsp_trans_type != '4':
            items = TrnstnSitutn.find_by_filter_for_map(
                sid_cd, sgg_cd, emd_cd,
                tsp_trans_type, tsp_house_kind,
                tsp_ssale, tsp_esale,
                tsp_sdeposit, tsp_edeposit,
                tsp_srent, tsp_erent,
                tsp_sexarea, tsp_eexarea,
                tsp_sdecrepit, tsp_edecrepit,
                tsp_syyyymm, tsp_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'geom': json.loads(item.geojson)['coordinates'],
                        'trnstn_yyyymm_start': item.trnstn_yyyymm_start,
                        'trnstn_yyyymm_end': item.trnstn_yyyymm_end,
                        'house_clsftn_code': item.house_clsftn_code,
                        'trnstn_clsftn_code': item.trnstn_clsftn_code,
                        'build_year': item.build_year,
                        'sale_price': item.sale_price,
                        'cnstrtn_area': item.cnstrtn_area,
                        'mnthly_rent': item.mnthly_rent,
                        'converted_rent': item.converted_rent,
                        'deposit': item.deposit,
                        'trnstn_count': item.trnstn_count,
                        'trnstn_count_per_exclsv': item.trnstn_count_per_exclsv,
                        'house_count': item.house_count,
                        'floor': item.floor,
                        'house_count_per_exclsv': item.house_count_per_exclsv,
                        'sale_price_avg': item.sale_price_avg,
                        'price_avg_per_cnstrtn_area': item.price_avg_per_cnstrtn_area,
                        'junse_avg_per_cnstrtn_area': item.junse_avg_per_cnstrtn_area,
                        'exclsv_area': item.exclsv_area,
                        'mnthly_rent_avg': item.mnthly_rent_avg,
                        'deposit_avg': item.deposit_avg,
                        'junse_avg': item.junse_avg,
                        'earnings_rate': item.earnings_rate,
                        'bldng_ko_name': item.bldng_ko_name,
                        'address': item.address,
                        'road_address': item.road_address
                    })

            return render_json(200, rows=result)
        else:
            items = TrnstnSitutnSupply.find_by_filter_for_map(
                sid_cd, sgg_cd, emd_cd,
                tsp_ssale, tsp_esale,
                tsp_sexarea, tsp_eexarea,
                tsp_syyyymm, tsp_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'geom': json.loads(item.geojson)['coordinates'],
                        'trnstn_yyyymm_start': item.trnstn_yyyymm_start,
                        'trnstn_yyyymm_end': item.trnstn_yyyymm_end,
                        'supply_price': item.supply_price,
                        'cnstrtn_area': item.cnstrtn_area,
                        'exclsv_area': item.exclsv_area,
                        'trnstn_count': item.trnstn_count,
                        'trnstn_count_per_exclsv': item.trnstn_count_per_exclsv,
                        'house_count': item.house_count,
                        'house_count_per_exclsv': item.house_count_per_exclsv,
                        'floor': item.floor,
                        'supply_price_avg': item.supply_price_avg,
                        'supply_price_avg_per_cnstrtn_area': item.supply_price_avg_per_cnstrtn_area,
                        'bldng_ko_name': item.bldng_ko_name,
                        'address': item.address,
                    })
            return render_json(200, rows=result)

    if req_type == 'bubble':
        if tsp_trans_type != '4':
            items = TrnstnSitutn.find_by_filter_for_price_bubble(
                sid_cd, sgg_cd, emd_cd,
                tsp_trans_type, tsp_house_kind,
                tsp_ssale, tsp_esale,
                tsp_sdeposit, tsp_edeposit,
                tsp_srent, tsp_erent,
                tsp_sexarea, tsp_eexarea,
                tsp_sdecrepit, tsp_edecrepit,
                tsp_syyyymm, tsp_eyyyymm)

            result = []

            for item in items:
                if item.geojson is not None:
                    total_sum = 0
                    if item.total_sum is not None:
                        total_sum = int(item.total_sum)

                    result.append({
                        'area_ko_nm': item.area_ko_nm,
                        'coordinates': json.loads(item.geojson)['coordinates'],
                        'total_sum': total_sum
                    })

            return render_json(200, rows=result)
        else:
            items = TrnstnSitutnSupply.find_by_filter_for_price_bubble(
                sid_cd, sgg_cd, emd_cd,
                tsp_ssale, tsp_esale,
                tsp_sexarea, tsp_eexarea,
                tsp_syyyymm, tsp_eyyyymm
            )

            result = []
            for item in items:
                if item.geojson is not None:
                    result.append({
                        'area_ko_nm': item.area_ko_nm,
                        'coordinates': json.loads(item.geojson)['coordinates'],
                        'total_sum': item.total_sum
                    })

            return render_json(200, rows=result)

    if req_type == 'grid':
        if tsp_trans_type == '1':
            items = PrestoTest.find_for_trnstn_sale_pivot(
                sid_cd, sgg_cd, emd_cd,
                tsp_ssale, tsp_esale,
                tsp_trans_type, tsp_house_kind,
                tsp_sexarea, tsp_eexarea,
                tsp_syyyymm, tsp_eyyyymm)

            ret = []
            col = items.get('cols').split(", ")
            for idx, row in enumerate(items.get('rows')):
                temp_dict = {}
                for idxx, item in enumerate(row):
                    temp_dict[col[idxx]] = item

                ret.append(temp_dict)

            return render_json(200, {'rows': ret, 'cols': col})
        if tsp_trans_type == '2':
            items = PrestoTest.find_for_trnstn_junse_pivot(
                sid_cd, sgg_cd, emd_cd,
                tsp_ssale, tsp_esale,
                tsp_trans_type, tsp_house_kind,
                tsp_sexarea, tsp_eexarea,
                tsp_syyyymm, tsp_eyyyymm)

            ret = []
            col = items.get('cols').split(", ")
            for idx, row in enumerate(items.get('rows')):
                temp_dict = {}
                for idxx, item in enumerate(row):
                    temp_dict[col[idxx]] = item

                ret.append(temp_dict)

            return render_json(200, {'rows': ret, 'cols': col})

        if tsp_trans_type == '3':
            items = PrestoTest.find_for_trnstn_mnthly_rent_pivot(
                sid_cd, sgg_cd, emd_cd,
                tsp_ssale, tsp_esale,
                tsp_trans_type, tsp_house_kind,
                tsp_sexarea, tsp_eexarea,
                tsp_syyyymm, tsp_eyyyymm)

            ret = []
            col = items.get('cols').split(", ")
            for idx, row in enumerate(items.get('rows')):
                temp_dict = {}
                for idxx, item in enumerate(row):
                    temp_dict[col[idxx]] = item

                ret.append(temp_dict)

            return render_json(200, {'rows': ret, 'cols': col})

        if tsp_trans_type == '4':
            items = PrestoTest.find_for_trnstn_supply_price_pivot(
                sid_cd, sgg_cd, emd_cd,
                tsp_ssale, tsp_esale,
                tsp_trans_type, tsp_house_kind,
                tsp_sexarea, tsp_eexarea,
                tsp_syyyymm, tsp_eyyyymm)

            ret = []
            col = items.get('cols').split(", ")
            for idx, row in enumerate(items.get('rows')):
                temp_dict = {}
                for idxx, item in enumerate(row):
                    temp_dict[col[idxx]] = item

                ret.append(temp_dict)

            return render_json(200, {'rows': ret, 'cols': col})


# 입주물량 검색
@situation.route('/srch_idnfln_bldng', methods=['POST'])
def srch_idnfln_bldng():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')

    # 주택 구분 코드
    ib_house_kind = request.form.get('ib_house_kind')
    # 면적 시작
    ib_sexarea = request.form.get('ib_sexarea')
    # 면적 종료
    ib_eexarea = request.form.get('ib_eexarea')

    # 입주 시작 년월
    ib_syyyymm = request.form.get('ib_syear') + request.form.get('ib_smonth')
    # 입주 종료 년월
    ib_eyyyymm = request.form.get('ib_eyear') + request.form.get('ib_emonth')

    req_type = request.form.get('req_type')

    if req_type == 'check':
        check = IdnftnBldng.find_by_filter_for_check(
            sid_cd, sgg_cd, emd_cd,
            ib_house_kind, ib_sexarea, ib_eexarea,
            ib_syyyymm, ib_eyyyymm)

        return render_json(200, hasData=check)

    if req_type == 'list':
        items = IdnftnBldng.find_by_filter_for_list(
            sid_cd, sgg_cd, emd_cd,
            ib_house_kind, ib_sexarea, ib_eexarea,
            ib_syyyymm, ib_eyyyymm)

        result = []

        for item in items:
            if item.geojson is not None:
                result.append({
                    'geom': json.loads(item.geojson)['coordinates'],
                    'building_kor': item.building_kor,
                    'address': item.area_location_kor
                })

        return render_json(200, rows=result)

    if req_type == 'map':
        items = IdnftnBldng.find_by_filter_for_map(
            sid_cd, sgg_cd, emd_cd,
            ib_house_kind, ib_sexarea, ib_eexarea,
            ib_syyyymm, ib_eyyyymm)

        result = []
        for item in items:
            if item.geojson is not None:
                result.append({
                    'geom': json.loads(item.geojson)['coordinates'],
                    'area_location_kor': item.area_location_kor,
                    'building_kor': item.building_kor,
                    'area_wide': item.area_wide,
                    'build_wide': item.build_wide,
                    'building_exist': item.building_exist,
                    'area_ratio': item.area_ratio,
                    'a_floor': item.a_floor,
                    'b_floor': item.b_floor,
                    'permission_using_date': item.permission_using_date,
                    'parking_sum': item.parking_sum,
                    'height': item.height,
                    'exclsv_area': item.exclsv_area,
                    'count_family': item.count_family,
                })

        return render_json(200, rows=result)

    if req_type == 'bubble':
        items = IdnftnBldng.find_by_filter_for_bubble(
            sid_cd, sgg_cd, emd_cd,
            ib_house_kind, ib_sexarea, ib_eexarea,
            ib_syyyymm, ib_eyyyymm)

        result = []
        for item in items:
            if item.geojson is not None:
                result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })
        return render_json(200, rows=result)

    if req_type == 'grid':
        items = PrestoTest.find_for_idnftn_bldng_pivot(
            sid_cd, sgg_cd, emd_cd,
            ib_house_kind, ib_sexarea, ib_eexarea,
            ib_syyyymm, ib_eyyyymm)

        ret = []
        col = items.get('cols').split(", ")
        for idx, row in enumerate(items.get('rows')):
            temp_dict = {}
            for idxx, item in enumerate(row):
                temp_dict[col[idxx]] = item

            ret.append(temp_dict)

        return render_json(200, {'rows': ret, 'cols': col})


# 자영업 현황
@situation.route('/srch_busins_situtn', methods=['POST'])
def srch_busins_situtn():
    req_type = request.form.get('req_type')

    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')
    busins_wide_cds = request.form.getlist('busins_wide_cd')
    busins_narrow_cds = request.form.getlist('busins_narr_cd')

    if req_type == 'map':
        items = BusinsSitutn.find_by_filter_for_map(sid_cd, sgg_cd, emd_cd, busins_wide_cds, busins_narrow_cds)

        # return render_json(200, rows=[{'hoho':'hihi'}])
        return render_json(200, rows=[{
            'sid_cd': item.sid_cd,
            'sgg_cd': item.sgg_cd,
            'emd_cd': item.emd_cd,
            'brand_nm': item.brand_nm,
            'prcl_addrs': item.prcl_addrs,
            'busins_wide_cds': item.busins_wide_cd,
            'busins_narrow_cds': item.busins_narrow_cd,
            'geom': json.loads(item.geojson)['coordinates']
        } for item in items])

    if req_type == 'bubble':
        items = BusinsSitutn.find_by_filter_for_bubble(sid_cd, sgg_cd, emd_cd, busins_wide_cds, busins_narrow_cds)

        result = []
        for item in items:
            if item.geojson is not None:
                result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })

        return render_json(200, rows=result)

    if req_type == 'grid':
        items = BusinsSitutn.find_by_filter_for_grid(sid_cd, sgg_cd, emd_cd, busins_wide_cds, busins_narrow_cds)

        return render_json(200, {'rows': items.get('rows'), 'cols': items.get('cols')})

@situation.route('/srch_hshold_imgrat', methods=['POST'])
# 세대통계 검색
def srch_hshold_imgrat():
    # 시도 코드
    sid_cd = request.form.get('sid_cd')
    # 시군구 코드
    sgg_cd = request.form.get('sgg_cd')
    # 읍면동 코드
    emd_cd = request.form.get('emd_cd')

    # 세대수
    hi_fmly_num_cd = request.form.getlist('hi_fmly_num_cd')
    # 시작년월
    st_yyyymm = request.form.get('hi_syear') + request.form.get('hi_smonth')
    # 종료년월
    ed_yyyymm = request.form.get('hi_eyear') + request.form.get('hi_emonth')

    if request.form.get('req_type') == 'map':
        items = HsholdImgrat.find_by_filter_for_map(sid_cd, sgg_cd, emd_cd, hi_fmly_num_cd, st_yyyymm, ed_yyyymm)

        return render_json(200, rows=[{
            'coordinates': json.loads(item.geojson)['coordinates'],
            'hshold_num': item.hshold_num
        } for item in items])

    if request.form.get('req_type') == 'bubble':
        items = HsholdImgrat.find_by_filter_for_bubble(sid_cd, sgg_cd, emd_cd, hi_fmly_num_cd, st_yyyymm, ed_yyyymm)

        result = []
        for item in items:

            if item.geojson is not None:
                result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })
        return render_json(200, rows=result)

    if request.form.get('req_type') == 'grid':
        items = PrestoTest.find_for_hshold_imgrat_pivot(sid_cd, sgg_cd, emd_cd, hi_fmly_num_cd, st_yyyymm, ed_yyyymm)

        ret = []
        col = items.get('cols').split(", ")
        for idx, item in enumerate(items.get('rows')):
            hehe = {}
            for idxx, hoho in enumerate(item):
                hehe[col[idxx]] = hoho

            ret.append(hehe)

        return render_json(200, {'rows': ret, 'cols': col})


# 분양현황 검색
@situation.route('/srch_supply_present', methods=['GET', 'POST'])
def srch_supply_present():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')
    req_type = request.form.get('req_type')

    # 분양현황 구분
    sp_type = request.form.get('sp_type')
    # 면적 시작
    sp_sexarea = request.form.get('sp_sexarea')
    # 면적 종료
    sp_eexarea = request.form.get('sp_eexarea')

    # 모집공고일 시작
    st_yyyymm = request.form.get('sp_syear') + request.form.get('sp_smonth')
    # 모집공고일 종료
    ed_yyyymm = request.form.get('sp_eyear') + request.form.get('sp_emonth')

    if req_type == 'check':
        check = SupplyPresentNew.find_by_filter_for_check(sid_cd, sgg_cd, emd_cd,
                                                          sp_sexarea, sp_eexarea,
                                                          st_yyyymm, ed_yyyymm)

        return render_json(200, hasData=check)

    if req_type == 'list':
        items = SupplyPresentNew.find_by_filter_for_list(sid_cd, sgg_cd, emd_cd,
                                                         sp_sexarea, sp_eexarea,
                                                         st_yyyymm, ed_yyyymm)

        result = []
        for item in items:
            if item.geojson is not None:
                result.append({
                    'geom': json.loads(item.geojson)['coordinates'],
                    'bldng_ko_name': item.bldng_ko_name,
                    'address': item.address
                })

        return render_json(200, rows=result)

    if req_type == 'card_list':
        items = SupplyPresentNew.find_by_filter_for_list(sid_cd, sgg_cd, emd_cd,
                                                         sp_sexarea, sp_eexarea,
                                                         st_yyyymm, ed_yyyymm)

        result = []
        for item in items:
            if item.geojson is not None:
                result.append({
                    'geom': json.loads(item.geojson)['coordinates'],
                    'bldng_ko_name': item.bldng_ko_name,
                    'address': item.address,
                    'data': SupplyPresentNew.find_by_filter_for_contents(item.bldng_ko_name, st_yyyymm, ed_yyyymm)
                })

        return render_json(200, rows=result)

    if req_type == 'map':
        items = SupplyPresentNew.find_by_filter_for_map(sid_cd, sgg_cd, emd_cd,
                                                        sp_sexarea, sp_eexarea,
                                                        st_yyyymm, ed_yyyymm)

        result = []
        for item in items:
            if item.geojson is not None:
                result.append({
                    'geom': json.loads(item.geojson)['coordinates'],
                    'bldng_ko_name': item.bldng_ko_name,
                    'address': item.address,
                    'yyyymm': item.yyyymm,
                    'supply_unit': item.supply_unit,
                    'result_announcement_yyyymm': item.result_announcement_yyyymm,
                    'contract_yyyymmdd_start': item.contract_yyyymmdd_start,
                    'contract_yyyymmdd_end': item.contract_yyyymmdd_end,
                    'supply_clsftn': item.supply_clsftn,
                    'supply_area': item.supply_area,
                    'general_unit': item.general_unit,
                    'special_unit': item.special_unit,
                    'price': item.price,
                    'price_per_supply_area': item.price_per_supply_area,
                    'developer': item.developer,
                    'builder': item.builder,
                    'homepage1': item.homepage1,
                    'homepage2': item.homepage2
                })

        return render_json(200, rows=result)

    if req_type == 'bubble':
        start_item = SupplyPresentNew.find_by_filter_for_bubble_start(sid_cd, sgg_cd, emd_cd,
                                                           sp_type,
                                                           sp_sexarea, sp_eexarea,
                                                           st_yyyymm, ed_yyyymm)

        end_item = SupplyPresentNew.find_by_filter_for_bubble_end(sid_cd, sgg_cd, emd_cd,
                                                           sp_type,
                                                           sp_sexarea, sp_eexarea,
                                                           st_yyyymm, ed_yyyymm)

        # items = SupplyPresentNew.find_by_filter_for_bubble(sid_cd, sgg_cd, emd_cd,
        #                                                    sp_type,
        #                                                    sp_sexarea, sp_eexarea,
        #                                                    st_yyyymm, ed_yyyymm)
        start_result = []
        for item in start_item:
            if item.geojson is not None:
                start_result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })
        end_result = []
        for item in end_item:
            if item.geojson is not None:
                end_result.append({
                    'area_ko_nm': item.area_ko_nm,
                    'coordinates': json.loads(item.geojson)['coordinates'],
                    'total_sum': item.total_sum
                })

        return render_json(200, rows={"start": start_result, "end": end_result})

    if req_type == 'grid':
        items = PrestoTest.find_for_supply_present_pivot(sid_cd, sgg_cd, emd_cd,
                                                         sp_type,
                                                         sp_sexarea, sp_eexarea,
                                                         st_yyyymm, ed_yyyymm)

        ret = []
        col = items.get('cols').split(", ")

        for idx, row in enumerate(items.get('rows')):
            temp_dict = {}
            for idxx, item in enumerate(row):
                temp_dict[col[idxx]] = item

            ret.append(temp_dict)

        return render_json(200, {'rows': ret, 'cols': col})


@situation.route('/srch_income_situtn', methods=['POST'])
# 소득현황 검색
def srch_income_situtn():
    sid_cd = request.form.get('sid_cd')
    sgg_cd = request.form.get('sgg_cd')
    emd_cd = request.form.get('emd_cd')

    # 요청 타입 (1인 평균 연봉, 종사자 수)
    is_type = request.form.get('is_type')
    req_type = request.form.get('req_type')

    if req_type == 'check':
        check = IncomeSitutnCompany.find_by_filter_for_check(sid_cd, sgg_cd, emd_cd)

        return render_json(200, hasData=check)

    if is_type == '1':
        if req_type == 'map':
            return 'OK'

        if req_type == 'bubble':
            items = IncomeSitutnCompany.find_by_filter_for_bubble(is_type, sid_cd, sgg_cd, emd_cd)

            result = []
            for item in items:
                if item.geojson:
                    result.append({
                        'area_ko_nm': item.area_ko_nm,
                        'coordinates': json.loads(item.geojson)['coordinates'],
                        'total_sum': int(item.total_sum)
                    })

            return render_json(200, rows=result)

        if req_type == 'grid':
            items = PrestoTest.find_for_income_situtn_pivot(sid_cd, sgg_cd, emd_cd, is_type)

            ret = []
            col = items.get('cols').split(", ")
            for idx, row in enumerate(items.get('rows')):
                temp_dict = {}
                for idxx, item in enumerate(row):
                    temp_dict[col[idxx]] = item

                ret.append(temp_dict)

            return render_json(200, {'rows': ret, 'cols': col})

    if is_type == '2':
        if req_type == 'map':
            return 'OK'

        if req_type == 'bubble':
            items = IncomeSitutnCompany.find_by_filter_for_bubble(is_type, sid_cd, sgg_cd, emd_cd)

            result = []
            for item in items:
                if item.geojson:
                    result.append({
                        'area_ko_nm': item.area_ko_nm,
                        'coordinates': json.loads(item.geojson)['coordinates'],
                        'total_sum': int(item.total_sum)
                    })

            return render_json(200, rows=result)

        if req_type == 'grid':
            items = PrestoTest.find_for_income_situtn_pivot(sid_cd, sgg_cd, emd_cd, is_type)

            ret = []
            col = items.get('cols').split(", ")
            for idx, row in enumerate(items.get('rows')):
                temp_dict = {}
                for idxx, item in enumerate(row):
                    temp_dict[col[idxx]] = item

                ret.append(temp_dict)

            return render_json(200, {'rows': ret, 'cols': col})


@situation.route('/srch_summary', methods=['GET', 'POST'])
def srch_summary():
    geom = request.form.get('geom')

    # 인구통계
    ps_summary = PopltnStats.find_summary_by_geom(geom)
    # 인구이동
    pm_summary = PopltnMvmt.find_summary_by_geom(geom)
    # 수요분석
    ts_summary = TrnstnSitutn.find_summary_by_geom(geom)
    # 자영업현황
    bs_summary = BusinsSitutn.find_summary_by_geom(geom)
    # 세대통계
    hi_summary = HsholdImgrat.find_summary_by_geom(geom)
    # 분양현황
    sp_summary = SupplyPresent.find_summary_by_geom(geom)
    # 소득현황
    is_summary = IncomeSitutnCompany.find_by_summary_by_geom(geom)

    return render_json(200, {
        # 인구통계 기준 년월
        'ps_yyyymm': ps_summary.get('ps_yyyymm')[0][0],
        # 인구통계 총 인구수
        'popltn_sum': ps_summary.get('popltn_sum')[0][0],
        # 인구이동 기준 년월
        'pm_yyyymm': pm_summary.get('pm_yyyymm')[0][0],
        # 인구이동 총 전입자
        'in_popltn_sum': pm_summary.get('in_popltn_sum')[0][0],
        # 인구이동 총 전출자
        'out_popltn_sum': pm_summary.get('out_popltn_sum')[0][0],
        # 수요분석 기준 년월
        'ts_yyyymm': ts_summary.get('ts_yyyymm')[0][0],
        # 수요분석 총 거래량
        'trnstn_amount_sum': ts_summary.get('trnstn_count_sum')[0][0],
        # 수요분석 평균 거래가
        'trnstn_price_avg': ts_summary.get('trnstn_price_avg')[0][0],
        # 자영업현황 기준 년월
        'bs_yyyymm': bs_summary.get('bs_yyyymm'),
        # 자영업현황 자영업소수
        'self_emp_sum': bs_summary.get('self_emp_sum')[0][0],
        # 세대통계 기준 년월
        'hi_yyyymm': hi_summary.get('hi_yyyymm')[0][0],
        # 세대통계 세대수
        'household_sum': hi_summary.get('household_sum')[0][0],
        # 분양현황 기준 년월
        'sp_yyyymm': sp_summary.get('sp_yyyymm')[0][0],
        # 분양현황 분양 단지 수
        'parcel_area_sum': sp_summary.get('parcel_area_sum')[0][0],
        # 분양현황 분양 세대 수
        'parcel_trnstn_sum': sp_summary.get('parcel_trnstn_sum')[0][0],
        # 분양현황 평균 평당가
        'floor_price_avg': sp_summary.get('floor_price_avg')[0][0],
        # 소득현황 기준 년월
        'is_yyyymm': is_summary.get('is_yyyymm'),
        # 소득현황 총 종사자 수
        'labor_sum': is_summary.get('labor_sum')[0][0],
        # 소득현황 평균 추정 연봉
        'income_avg': int(is_summary.get('income_avg')[0][0])
    })


@situation.route('/get_categorys', methods=['POST'])
def get_categorys():
    print(current_user.id)
    items = UserMarkers.find_not_replication_categorys(current_user.id)

    return render_json(200, rows=[{
        'category': item.category
    } for item in items])


@situation.route('/set_marker', methods=['POST'])
@login_required
def set_marker():
    user_id = current_user.id
    category = request.form.get('markerCategory')
    title = request.form.get('markerTitle')
    content = request.form.get('markerContent')
    latitude = request.form.get('lat')
    longitude = request.form.get('log')
    img_name = request.form.get('img')

    UserMarkers.insert_data(user_id, category, title, content, latitude, longitude, img_name)

    return 'OK'


@situation.route('/view_marker', methods=['POST'])
@login_required
def view_marker():
    user_id = current_user.id
    categorys = request.form.getlist('category')

    items = UserMarkers.find_by_category(user_id, categorys)

    return render_json(200, rows=[{
        'idx': item.idx,
        'category': item.category,
        'title': item.title,
        'content': item.content,
        'geom': json.loads(item.geom)['coordinates'],
        'img_name': item.img_name
    } for item in items])


@situation.route('/update_makrer', methods=['POST'])
def update_marker():
    idx = request.form.get('idx')
    category = request.form.get('markerCategory')
    title = request.form.get('markerTitle')
    content = request.form.get('markerContent')

    UserMarkers.update_data(idx, category, title, content)

    return 'OK'


@situation.route('delete_marker', methods=['POST'])
def delete_marker():
    idx = request.form.get('idx')

    UserMarkers.delete_data(idx)

    return 'OK'


@situation.route('/search_address', methods=['POST'])
def search_address():
    address = request.form.get('address')

    results = VWorldAPI.search(address, 'ADDRESS', 'ROAD')

    return render_json(200, results)


@situation.route('/livy_test', methods=['POST'])
def livy_test():
    # res0 = LivyAPI.test_static_method()
    # res1 = LivyAPI.get_sessions(0, 11)
    # res2 = LivyAPI.get_session(16)
    # res3 = LivyAPI.create_session()
    # res4 = LivyAPI.delete_session(52)
    # res5 = LivyAPI.get_statements('popltn_mvmt_pivot')

    res6 = LivyAPI.get_datas('pivot_poplnt_mvmt')
    # res5 = LivyAPI.get_statements('pivot_supply_count')

    print("++++++++++++++++++++++++++++++++++++++++++")
    # print(res0)
    # print(res1)
    # print(res2)
    print(LivyAPI.livy_statements)
    print(LivyAPI.session_id)
    # print(res4)
    # print(res5)
    print("++++++++++++++++++++++++++++++++++++++++++")

    return 'OK'


@situation.route('/presto_test', methods=['POST'])
def presto_test():
    sid_cd = '11'
    sgg_cd = None
    emd_cd = None
    age_grp_cds = ['10', '15', '20']
    st_yyyymm = '201010'
    ed_yyyymm = '201613'
    rsdnc_clsftn_cds = ['1', '2', '3']
    fmly_num_cds = ['1', '2', '3']
    room_num_cds = ['1', '2', '3']
    hs_syear = '2010'
    hs_eyear = '2015'

    # 인구통계
    # hoho = PrestoTest.find_for_popltn_stats_pivot(sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm, ed_yyyymm);
    # 인구주택총조사
    # PrestoTest.find_for_hshold_stats_pivot(sid_cd, sgg_cd, rsdnc_clsftn_cds, fmly_num_cds, room_num_cds, hs_syear, hs_eyear)
    # 인구이동
    # PrestoTest.find_for_popltn_mvmt()
    # 수요분석 - 거래량
    # PrestoTest.find_for_trnstn_situtn_trans_pivot()
    #
    # 수요분석 - 가격
    # PrestoTest.find_for_trnstn_situtn_price_pivot()
    # 입주물량
    # PrestoTest.find_for_idnftn_bldng_pivot()
    # 자영업현황
    # PrestoTest.find_for_busins_situtn_pivot()
    # 세대통계
    # PrestoTest.find_for_hshold_imgrat_pivot()
    # 분양현황
    # PrestoTest.find_for_supply_present_pivot()
    # 소득현황
    # PrestoTest.find_for_income_situtn_pivot()

    return render_json(200, rows=PrestoTest.test())
