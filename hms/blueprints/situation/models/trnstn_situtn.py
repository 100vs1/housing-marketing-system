# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
from sqlalchemy import func, and_, or_, desc, cast, DATE, asc, collate
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import compiler

from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea, AdmEmdArea
from geoalchemy2.types import Geometry
from hms.extensions import db


class TrnstnSitutn(db.Model):
    """
    거래현황 모델 정의 클래스
    실거래가 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'trnstn_situtn_new' # 거래현황

    id = db.Column(db.Integer, db.Sequence('trnstn_situtn_new_test_id_seq'), primary_key=True)  # 인덱스
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))    # 지오메트리(Point)
    sid_cd = db.Column(db.String(2))
    sgg_cd = db.Column(db.String(5))
    emd_cd = db.Column(db.String(10))
    yyyymm = db.Column(db.String(6))
    house_clsftn_code = db.Column(db.String(2))
    trnstn_clsftn_code = db.Column(db.String(2))
    build_yyyy = db.Column(db.String(4))
    day = db.Column(db.String(5))
    sale_price = db.Column(db.Integer)
    sale_price_avg = db.Column(db.Float)
    sale_price_avg_per_cnstrtn_area = db.Column(db.Float)
    exclsv_area = db.Column(db.Float)
    cnstrtn_area = db.Column(db.Float)
    mnthly_rent = db.Column(db.Integer)
    mnthly_rent_avg = db.Column(db.Float)
    converted_mnthly_rent = db.Column(db.Integer)
    deposit = db.Column(db.Integer)
    deposit_avg = db.Column(db.Float)
    junse = db.Column(db.Integer)
    junse_avg = db.Column(db.Float)
    junse_avg_per_cnstrtn_area = db.Column(db.Float)
    trnstn_count = db.Column(db.Integer)
    trnstn_count_per_exclsv = db.Column(db.Integer)
    house_count = db.Column(db.Integer)
    house_count_per_exclsv = db.Column(db.Integer)
    earnings_rate = db.Column(db.Float)
    bldng_ko_nm = db.Column(db.String(80))
    address = db.Column(db.String(100))
    floor = db.Column(db.Integer)
    road_address = db.Column(db.String(30))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(TrnstnSitutn, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, sid_cd, sgg_cd, emd_cd,
                                 tst_trans_type, tst_house_kind,
                                 tst_ssale, tst_esale,
                                 tst_sdeposit, tst_edeposit,
                                 tst_srent, tst_erent,
                                 tst_sexarea, tst_eexarea,
                                 tst_sdecrepit, tst_edecrepit,
                                 tst_syyyymm, tst_eyyyymm):

        now = datetime.datetime.now()
        decrepit_eyear = str(now.year - int(tst_sdecrepit))
        decrepit_syear = str(now.year - int(tst_edecrepit))

        result = db.session.query(
            cls.emd_cd,
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.trnstn_clsftn_code == tst_trans_type). \
            filter(cls.house_clsftn_code == tst_house_kind). \
            filter(and_(cls.exclsv_area >= tst_sexarea,
                        cls.exclsv_area <= tst_eexarea)). \
            filter(and_(cls.build_yyyy >= decrepit_syear,
                        cls.build_yyyy <= decrepit_eyear)). \
            filter(and_(cls.yyyymm >= tst_syyyymm,
                        cls.yyyymm <= tst_eyyyymm)). \
            filter(cls.geom is not None)
        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        # 거래구분에 따른 필터 추가
        if str(tst_trans_type) == '1':
            result = result.filter(and_(cls.sale_price >= tst_ssale,
                                        cls.sale_price <= tst_esale))
        elif str(tst_trans_type) == '2':
            result = result.filter(and_(cls.junse >= tst_sdeposit,
                                        cls.junse <= tst_edeposit))
        elif str(tst_trans_type) == '3':
            result = result.filter(and_(cls.deposit >= tst_sdeposit,
                                        cls.deposit <= tst_edeposit)). \
                filter(and_(cls.mnthly_rent >= tst_srent,
                            cls.mnthly_rent <= tst_erent))
        else:
            print('ERROR')
            return 'ERROR'

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        results = result.limit(1)

        print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return result is not None


    @classmethod
    def find_by_filter_for_list(cls, sid_cd, sgg_cd, emd_cd,
                                tst_trans_type, tst_house_kind,
                                tst_ssale, tst_esale,
                                tst_sdeposit, tst_edeposit,
                                tst_srent, tst_erent,
                                tst_sexarea, tst_eexarea,
                                tst_sdecrepit, tst_edecrepit,
                                tst_syyyymm, tst_eyyyymm):

        now = datetime.datetime.now()
        decrepit_eyear = str(now.year - int(tst_sdecrepit))
        decrepit_syear = str(now.year - int(tst_edecrepit))

        query = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.address,
            cls.bldng_ko_nm
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.trnstn_clsftn_code == tst_trans_type). \
            filter(cls.house_clsftn_code == tst_house_kind). \
            filter(and_(cls.exclsv_area >= tst_sexarea,
                        cls.exclsv_area <= tst_eexarea)). \
            filter(and_(cls.build_yyyy >= decrepit_syear,
                        cls.build_yyyy <= decrepit_eyear)). \
            filter(and_(cls.yyyymm >= tst_syyyymm,
                        cls.yyyymm <= tst_eyyyymm)). \
            filter(cls.geom is not None)

        # 거래구분에 따른 필터 추가
        if str(tst_trans_type) == '1':
            query = query.filter(and_(cls.sale_price >= tst_ssale,
                                      cls.sale_price <= tst_esale))
        elif str(tst_trans_type) == '2':
            query = query.filter(and_(cls.junse >= tst_sdeposit,
                                      cls.junse <= tst_edeposit))
        elif str(tst_trans_type) == '3':
            query = query.filter(and_(cls.deposit >= tst_sdeposit,
                                      cls.deposit <= tst_edeposit)). \
                filter(and_(cls.mnthly_rent >= tst_srent,
                            cls.mnthly_rent <= tst_erent))
        else:
            return 'ERROR'

        result = query.group_by('geojson', cls.address, cls.bldng_ko_nm). \
            order_by(asc(collate(cls.bldng_ko_nm, 'C')))

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return result

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd,
                               tst_trans_type, tst_house_kind,
                               tst_ssale, tst_esale,
                               tst_sdeposit, tst_edeposit,
                               tst_srent, tst_erent,
                               tst_sexarea, tst_eexarea,
                               tst_sdecrepit, tst_edecrepit,
                               tst_syyyymm, tst_eyyyymm):

        print(tst_trans_type)

        now = datetime.datetime.now()
        decrepit_eyear = str(now.year - int(tst_sdecrepit))
        decrepit_syear = str(now.year - int(tst_edecrepit))

        query = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.yyyymm,
            db.session.query(Code.name).
                filter(and_(Code.code == cls.house_clsftn_code, Code.group_code == 'ts_house_type')).
                limit(1).label('house_clsftn_code'),
            db.session.query(Code.name).
                filter(and_(Code.code == cls.trnstn_clsftn_code, Code.group_code == 'ts_trnstn_type')).
                limit(1).label('trnstn_clsftn_code'),
            cls.build_yyyy,
            cls.sale_price,
            cls.cnstrtn_area,
            cls.mnthly_rent,
            cls.converted_mnthly_rent,
            cls.deposit,
            cls.trnstn_count,
            cls.trnstn_count_per_exclsv,
            cls.house_count,
            cls.floor,
            cls.house_count_per_exclsv,
            cls.sale_price_avg,
            cls.sale_price_avg_per_cnstrtn_area,
            cls.junse_avg_per_cnstrtn_area,
            cls.exclsv_area,
            cls.mnthly_rent_avg,
            cls.deposit_avg,
            cls.junse_avg,
            cls.earnings_rate,
            cls.bldng_ko_name,
            cls.address,
            cls.road_address
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.trnstn_clsftn_code == tst_trans_type). \
            filter(cls.house_clsftn_code == tst_house_kind). \
            filter(and_(cls.exclsv_area >= tst_sexarea,
                        cls.exclsv_area <= tst_eexarea)). \
            filter(and_(cls.build_yyyy >= decrepit_syear,
                        cls.build_yyyy <= decrepit_eyear)). \
            filter(and_(cls.yyyymm >= tst_syyyymm,
                        cls.yyyymm <= tst_eyyyymm)). \
            filter(cls.geom is not None)

        # 거래구분에 따른 필터 추가
        if str(tst_trans_type) == '1':
            query = query.filter(and_(cls.sale_price >= tst_ssale,
                                      cls.sale_price <= tst_esale))
        elif str(tst_trans_type) == '2':
            query = query.filter(and_(cls.junse >= tst_sdeposit,
                                      cls.junse <= tst_edeposit))
        elif str(tst_trans_type) == '3':
            query = query.filter(and_(cls.deposit >= tst_sdeposit,
                                      cls.deposit <= tst_edeposit)). \
                filter(and_(cls.mnthly_rent >= tst_srent,
                            cls.mnthly_rent <= tst_erent))
        else:
            return 'ERROR'

        result = query.order_by(asc(collate(cls.bldng_ko_name, 'C')), cls.trnstn_yyyymm_start.desc())

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return result

    @classmethod
    def find_by_filter_for_trans_bubble(cls,
                                        sid_cd, sgg_cd, emd_cd,
                                        tst_trans_type, tst_house_kind,
                                        tst_ssale, tst_esale,
                                        tst_sdeposit, tst_edeposit,
                                        tst_srent, tst_erent,
                                        tst_sexarea, tst_eexarea,
                                        tst_sdecrepit, tst_edecrepit,
                                        tst_syyyymm, tst_eyyyymm):

        now = datetime.datetime.now()
        decrepit_eyear = str(now.year - int(tst_sdecrepit))
        decrepit_syear = str(now.year - int(tst_edecrepit))

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        query = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            geojson,
            func.sum(cls.trnstn_count).label('total_sum')
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.trnstn_clsftn_code == tst_trans_type). \
            filter(cls.house_clsftn_code == tst_house_kind). \
            filter(and_(cls.exclsv_area >= tst_sexarea,
                        cls.exclsv_area <= tst_eexarea)). \
            filter(and_(cls.build_yyyy >= decrepit_syear,
                        cls.build_yyyy <= decrepit_eyear)). \
            filter(and_(cls.yyyymm <= tst_eyyyymm,
                        cls.yyyymm >= tst_syyyymm)). \
            filter(cls.geom is not None)

        # 거래구분에 따른 필터 추가
        if str(tst_trans_type) == '1':
            query = query.filter(and_(cls.sale_price >= tst_ssale,
                                      cls.sale_price <= tst_esale))
        elif str(tst_trans_type) == '2':
            query = query.filter(and_(cls.junse >= tst_sdeposit,
                                      cls.junse <= tst_edeposit))
        elif str(tst_trans_type) == '3':
            query = query.filter(and_(cls.deposit >= tst_sdeposit,
                                      cls.deposit <= tst_edeposit)). \
                filter(and_(cls.mnthly_rent >= tst_srent,
                            cls.mnthly_rent <= tst_erent))
        else:
            return 'ERROR'

        result = query.group_by(cls.emd_cd)

        print("BUBBLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        print("BUBBLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return result

    @classmethod
    def find_by_filter_for_price_bubble(cls,
                                        sid_cd, sgg_cd, emd_cd,
                                        tst_trans_type, tst_house_kind,
                                        tst_ssale, tst_esale,
                                        tst_sdeposit, tst_edeposit,
                                        tst_srent, tst_erent,
                                        tst_sexarea, tst_eexarea,
                                        tst_sdecrepit, tst_edecrepit,
                                        tst_syyyymm, tst_eyyyymm):

        now = datetime.datetime.now()
        decrepit_eyear = str(now.year - int(tst_sdecrepit))
        decrepit_syear = str(now.year - int(tst_edecrepit))

        # target_price = None
        # if tst_trans_type == '1':
        #     target_price = cls.sale_price
        # elif tst_trans_type == '2':
        #     target_price = cls.deposit
        # elif tst_trans_type == '3':
        #     target_price = cls.converted_rent

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        if str(tst_trans_type) == '1':
            target_col = func.avg(cls.sale_price_avg_per_cnstrtn_area).label('total_sum')
        elif str(tst_trans_type) == '2':
            target_col = func.avg(cls.junse).label('total_sum')
        elif str(tst_trans_type) == '3':
            target_col = func.avg(cls.converted_mnthly_rent).label('total_sum')

        query = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            geojson,
            target_col
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.trnstn_clsftn_code == tst_trans_type). \
            filter(cls.house_clsftn_code == tst_house_kind). \
            filter(and_(cls.exclsv_area >= tst_sexarea,
                        cls.exclsv_area <= tst_eexarea)). \
            filter(and_(cls.build_yyyy >= decrepit_syear,
                        cls.build_yyyy <= decrepit_eyear)). \
            filter(cls.yyyymm <= tst_eyyyymm). \
            filter(cls.sale_price_avg_per_cnstrtn_area.isnot(None)).\
            filter(cls.geom is not None)


        # 거래구분에 따른 필터 추가
        if str(tst_trans_type) == '1':
            query = query.filter(and_(cls.sale_price >= tst_ssale,
                                      cls.sale_price <= tst_esale))
        elif str(tst_trans_type) == '2':
            query = query.filter(and_(cls.junse >= tst_sdeposit,
                                      cls.junse <= tst_edeposit))
        elif str(tst_trans_type) == '3':
            query = query.filter(and_(cls.deposit >= tst_sdeposit,
                                      cls.deposit <= tst_edeposit)). \
                filter(and_(cls.mnthly_rent >= tst_srent,
                            cls.mnthly_rent <= tst_erent))
        else:
            return 'ERROR'

        result = query.group_by(cls.emd_cd)

        print("BUBBLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        print("BUBBLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return result

    @classmethod
    def find_summary_by_geom(cls, geom):
        target_yyyymm = db.session.query(
            func.concat(func.max(func.substring(cls.trnstn_yyyymm_start, 1, 6)), '00')).limit(1)

        print(target_yyyymm.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        trnstn_count_sum = db.session.query(
            func.sum(cls.trnstn_count).label('trnstn_count_sum'),
        ). \
            filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326))). \
            filter(cls.trnstn_yyyymm_start >= target_yyyymm)

        print(trnstn_count_sum.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        trnstn_price_avg = db.session.query(
            func.avg(cls.sale_price_avg).label('trnstn_price_avg'),
        ). \
            filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326))). \
            filter(cls.trnstn_clsftn_code == '1'). \
            filter(cls.trnstn_yyyymm_start >= target_yyyymm)

        print(trnstn_price_avg.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return {
            'ts_yyyymm': target_yyyymm,
            'trnstn_count_sum': trnstn_count_sum,
            'trnstn_price_avg': trnstn_price_avg
        }
