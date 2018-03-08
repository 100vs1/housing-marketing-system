# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import func, and_, or_, desc, cast, DATE, asc, text, collate
from sqlalchemy.dialects import postgresql

from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea
from geoalchemy2.types import Geometry

from hms.blueprints.common.models.code import Code
from hms.extensions import db


class BusinsSitutn(db.Model):
    """
    업종현황 모델 정의 클래스
    업종현황 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'busins_situtn_new'

    sid_cd = db.Column(db.String(2), primary_key=True)
    sgg_cd = db.Column(db.String(5), primary_key=True)
    emd_cd = db.Column(db.String(10), primary_key=True)
    busins_cd = db.Column(db.String(8))
    brand_nm = db.Column(db.String(80))
    busins_wide_cd = db.Column(db.String(2))
    busins_narrow_cd = db.Column(db.String(4))
    main_num = db.Column(db.Integer)
    sub_num = db.Column(db.Integer)
    prcl_addrs = db.Column(db.String(80))
    road_cd = db.Column(db.String(20))
    building_mana = db.Column(db.String(20))
    dong = db.Column(db.String(20))
    floor = db.Column(db.String(20))
    house_cd = db.Column(db.String(15))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    def __init__(self, **kwargs):
        super(BusinsSitutn, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd, busins_wide_cds, busins_narrow_cds):
        busins_wide_cd = db.session.query(Code.name). \
            filter(and_(Code.code == cls.busins_wide_cd, Code.group_code == 'busins_wide_cd')).limit(1).label('busins_wide_cd')

        busins_narrow_cd = db.session.query(Code.name). \
            filter(and_(Code.code == cls.busins_narrow_cd, Code.group_code == 'busins_narr_cd')).limit(1).label(
            'busins_narrow_cd')

        results = db.session.query(
            cls.sid_cd,
            cls.sgg_cd,
            cls.emd_cd,
            cls.brand_nm,
            cls.prcl_addrs,
            busins_wide_cd,
            busins_narrow_cd,
            func.ST_AsGeoJSON(cls.geom).label('geojson')). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.busins_narrow_cd.in_(busins_narrow_cds)).\
            order_by(asc(collate(busins_narrow_cd, 'C')), asc(collate(cls.brand_nm, 'C'))).all()
        # print("*" * 50)
        # for item in results:
        #     print(item)
        # print("*" * 50)

        return results

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd, busins_wide_cds, busins_narrow_cds):
        # busins_wide_cd = db.session.query(Code.name). \
        #     filter(and_(Code.code == cls.busins_wide_cd, Code.group_code == 'busins_wide_cd')).limit(1).label(
        #     'busins_wide_cd')
        #
        # busins_narrow_cd = db.session.query(Code.name). \
        #     filter(and_(Code.code == cls.busins_narrow_cd, Code.group_code == 'busins_narr_cd')).limit(1).label(
        #     'busins_narrow_cd')

        items = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')).
                filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson'),
            func.count(cls.emd_cd).label('total_sum')). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.busins_narrow_cd.in_(busins_narrow_cds)).\
            group_by(cls.emd_cd)

        return items

    @classmethod
    def find_by_filter_for_grid(cls, sid_cd, sgg_cd, emd_cd, busins_wide_cds, busins_narrow_cds):
        busins_wide_cd = db.session.query(Code.name). \
            filter(and_(Code.code == cls.busins_wide_cd, Code.group_code == 'busins_wide_cd')).limit(1).label(
            'busins_wide_cd')

        busins_narrow_cd = db.session.query(Code.name). \
            filter(and_(Code.code == cls.busins_narrow_cd, Code.group_code == 'busins_narr_cd')).limit(1).label(
            'busins_narrow_cd')

        if sid_cd:
            items = db.session.query(
                db.session.query(LawSidArea.sid_ko_nm).filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid_ko_nm'),
                db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg_ko_nm'),
                busins_wide_cd,
                busins_narrow_cd,
                func.count(cls.sid_cd).label('busins_cnt')
            ).filter(cls.sid_cd == sid_cd).\
                filter(cls.busins_narrow_cd.in_(busins_narrow_cds)).\
                group_by(cls.sid_cd, cls.sgg_cd, busins_wide_cd, busins_narrow_cd)

            rows = []
            for item in items:
                rows.append({
                    'sid_ko_nm': item.sid_ko_nm,
                    'sgg_ko_nm': item.sgg_ko_nm,
                    'busins_wide_cd': item.busins_wide_cd,
                    'busins_narrow_cd': item.busins_narrow_cd,
                    'busins_cnt': item.busins_cnt
                })
            cols = ['sid_ko_nm', 'sgg_ko_nm', 'busins_wide_cd', 'busins_narrow_cd', 'busins_cnt']

            return {'rows': rows, 'cols': cols}
        elif sgg_cd:
            items = db.session.query(
                db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg_ko_nm'),
                db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd_ko_nm'),
                busins_wide_cd,
                busins_narrow_cd,
                func.count(cls.sgg_cd).label('busins_cnt')
            ).filter(cls.sgg_cd == sgg_cd).\
                filter(cls.busins_narrow_cd.in_(busins_narrow_cds)).\
                group_by(cls.sgg_cd, cls.emd_cd, busins_wide_cd, busins_narrow_cd)

            rows = []
            for item in items:
                rows.append({
                    'sgg_ko_nm': item.sgg_ko_nm,
                    'emd_ko_nm': item.emd_ko_nm,
                    'busins_wide_cd': item.busins_wide_cd,
                    'busins_narrow_cd': item.busins_narrow_cd,
                    'busins_cnt': item.busins_cnt
                })
            cols = ['sgg_ko_nm', 'emd_ko_nm', 'busins_wide_cd', 'busins_narrow_cd', 'busins_cnt']

            return {'rows': rows, 'cols': cols}
        elif emd_cd:
            items = db.session.query(
                db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd_ko_nm'),
                busins_wide_cd,
                busins_narrow_cd,
                func.count(cls.emd_cd).label('busins_cnt')
            ).filter(cls.emd_cd == emd_cd).\
                filter(cls.busins_narrow_cd.in_(busins_narrow_cds)).\
                group_by(cls.emd_cd, busins_wide_cd, busins_narrow_cd)

            rows = []
            for item in items:
                rows.append({
                    'emd_ko_nm': item.emd_ko_nm,
                    'busins_wide_cd': item.busins_wide_cd,
                    'busins_narrow_cd': item.busins_narrow_cd,
                    'busins_cnt': item.busins_cnt
                })
            cols = ['emd_ko_nm', 'busins_wide_cd', 'busins_narrow_cd', 'busins_cnt']

            return {'rows': rows, 'cols': cols}
        else:
            print("에러지")

        # busins_wide_cd = db.session.query(Code.name). \
        #     filter(and_(Code.code == cls.busins_wide_cd, Code.group_code == 'busins_wide_cd')).limit(1).label(
        #     'busins_wide_cd')
        #
        # busins_narrow_cd = db.session.query(Code.name). \
        #         filter(and_(Code.code == cls.busins_narrow_cd, Code.group_code == 'busins_narr_cd')).limit(1).label(
        #     'busins_narrow_cd')
        #
        # items = db.session.query(
        #     db.session.query(LawSidArea.sid_ko_nm).filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid_ko_nm'),
        #     db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg_ko_nm'),
        #     # db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd_ko_nm'),
        #     busins_wide_cd,
        #     busins_narrow_cd,
        #     func.count(cls.emd_cd).label('busins_cnt')). \
        #     filter(or_(cls.sid_cd == sid_cd,
        #                cls.sgg_cd == sgg_cd,
        #                cls.emd_cd == emd_cd)). \
        #     filter(cls.busins_narrow_cd.in_(busins_narrow_cds)). \
        #     group_by(cls.sid_cd, cls.sgg_cd, busins_wide_cd, busins_narrow_cd)
        #
        # print(items.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        # return items

    @classmethod
    def find_summary_by_geom(cls, geom):
        target_emd = LawEmdArea.find_emd_cds_by_geom(geom)

        self_emp_sum = db.session.query(func.count(cls.emd_cd)). \
            filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326)))

        return {
            'bs_yyyymm': '201706',
            'self_emp_sum': self_emp_sum
        }
