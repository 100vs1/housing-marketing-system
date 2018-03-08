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


class TrnstnSitutnSupply(db.Model):
    """
    거래현황 모델 정의 클래스
    실거래가 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'trnstn_situtn_supply_new' # 분양권

    id = db.Column(db.Integer, db.Sequence('trnstn_situtn_supply_id_seq'), primary_key=True) # 시퀀스아이디

    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    sid_cd = db.Column(db.String(2))
    sgg_cd = db.Column(db.String(5))
    emd_cd = db.Column(db.String(10))
    yyyymm = db.Column(db.String(6))
    supply_price = db.Column(db.Integer)
    cnstrtn_area = db.Column(db.Float)
    exclsv_area = db.Column(db.Float)
    trnstn_count = db.Column(db.Integer)
    trnstn_count_per_exclsv = db.Column(db.Integer)
    house_count = db.Column(db.Integer)
    house_count_per_exclsv = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    supply_price_avg = db.Column(db.Float)
    supply_price_avg_per_cnstrtn_area = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    bldng_ko_nm = db.Column(db.String(80))
    address = db.Column(db.String(100))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(TrnstnSitutnSupply, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, sid_cd, sgg_cd, emd_cd,
                                 ts_ssale, ts_esale,
                                 ts_sexarea, ts_eexarea,
                                 ts_syyyymm, ts_eyyyymm):

        result = db.session.query(
            func.count(cls.id).label('data_count'),
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.cnstrtn_area >= ts_sexarea,
                        cls.cnstrtn_area <= ts_eexarea)). \
            filter(and_(cls.yyyymm >= ts_syyyymm,
                        cls.yyyymm <= ts_eyyyymm)). \
            filter(and_(cls.supply_price >= ts_ssale, cls.supply_price <= ts_esale)). \
            filter(cls.geom is not None).limit(1).first()

        return result is not None

    @classmethod
    def find_by_filter_for_list(cls, sid_cd, sgg_cd, emd_cd,
                               ts_ssale, ts_esale,
                               ts_sexarea, ts_eexarea,
                               ts_syyyymm, ts_eyyyymm):

        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.address,
            cls.bldng_ko_nm
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.cnstrtn_area >= ts_sexarea,
                        cls.cnstrtn_area <= ts_eexarea)). \
            filter(and_(cls.yyyymm >= ts_syyyymm,
                        cls.yyyymm <= ts_eyyyymm)).\
            filter(and_(cls.supply_price >= ts_ssale, cls.supply_price <= ts_esale)).\
            filter(cls.geom is not None).\
            group_by('geojson', cls.address, cls.bldng_ko_nm).\
            order_by(asc(collate(cls.bldng_ko_nm, 'C')))

        # print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return result

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd,
                               ts_ssale, ts_esale,
                               ts_sexarea, ts_eexarea,
                               ts_syyyymm, ts_eyyyymm):

        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.yyyymm,
            cls.supply_price,
            cls.cnstrtn_area,
            cls.exclsv_area,
            cls.trnstn_count,
            cls.trnstn_count_per_exclsv,
            cls.house_count,
            cls.house_count_per_exclsv,
            cls.floor,
            cls.supply_price_avg,
            cls.supply_price_avg_per_cnstrtn_area,
            cls.bldng_ko_nm,
            cls.address
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.cnstrtn_area >= ts_sexarea,
                        cls.cnstrtn_area <= ts_eexarea)).\
            filter(and_(cls.yyyymm >= ts_syyyymm,
                        cls.yyyymm <= ts_eyyyymm)).\
            filter(and_(cls.supply_price >= ts_ssale,
                        cls.supply_price <= ts_esale)).\
            filter(cls.geom is not None).\
            order_by(asc(collate(cls.bldng_ko_name, '"C"')), cls.trnstn_yyyymm_start.desc())

        # print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return result

    @classmethod
    def find_by_filter_for_trans_bubble(cls,
                                        sid_cd, sgg_cd, emd_cd,
                                        tst_ssale, tst_esale,
                                        tst_sexarea, tst_eexarea,
                                        tst_syyyymm, tst_eyyyymm):
        target_yyyymm = db.session.query(cls.yyyymm). \
            filter(and_(cls.yyyymm >= tst_syyyymm,
                        cls.yyyymm <= tst_eyyyymm)).\
            order_by(desc(cls.yyyymm)).limit(1)

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        query = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            geojson,
            func.count(cls.trnstn_count).label('total_sum')
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.exclsv_area >= tst_sexarea,
                        cls.exclsv_area <= tst_eexarea)). \
            filter(cls.yyyymm == target_yyyymm). \
            filter(and_(cls.supply_price >= tst_ssale,
                        cls.supply_price <= tst_esale)).\
            filter(cls.geom is not None)

        results = query.group_by(cls.emd_cd)

        print('bubble~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        print('bubble~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        return results


    @classmethod
    def find_by_filter_for_price_bubble(cls,
                                        sid_cd, sgg_cd, emd_cd,
                                        tsp_ssale, tsp_esale,
                                        tsp_sexarea, tsp_eexarea,
                                        tsp_syyyymm, tsp_eyyyymm):

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        query = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            geojson,
            func.avg(cls.supply_price_avg_per_cnstrtn_area).label('total_sum')
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.cnstrtn_area >= tsp_sexarea,
                        cls.cnstrtn_area <= tsp_eexarea)). \
            filter(and_(cls.yyyymm >= tsp_syyyymm,
                        cls.yyyymm <= tsp_eyyyymm)). \
            filter(and_(cls.supply_price >= tsp_ssale,
                        cls.supply_price <= tsp_esale)).\
            filter(cls.geom is not None)

        results = query.group_by(cls.emd_cd)

        print('BUBBLE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        print('BUBBLE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        return results


    @classmethod
    def find_summary_by_geom(cls, geom):
        target_yyyymm = db.session.query(
            func.concat(func.max(func.substring(cls.trnstn_yyyymm_start, 1, 6)), '00')).limit(1)

        print(target_yyyymm.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        trnstn_count_sum = db.session.query(
            func.sum(cls.trnstn_count).label('trnstn_count_sum'),
        ).\
            filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326))).\
            filter(cls.yyyymm >= target_yyyymm)

        print(trnstn_count_sum.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        trnstn_price_avg = db.session.query(
            func.avg(cls.sale_price_avg).label('trnstn_price_avg'),
        ). \
            filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326))).\
            filter(cls.trnstn_clsftn_code == '1').\
            filter(cls.yyyymm >= target_yyyymm)

        print(trnstn_price_avg.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return {
            'ts_yyyymm': target_yyyymm,
            'trnstn_count_sum': trnstn_count_sum,
            'trnstn_price_avg': trnstn_price_avg
        }
