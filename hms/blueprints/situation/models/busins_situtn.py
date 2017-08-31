# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import func, and_, or_, desc, cast, DATE
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea
from geoalchemy2.types import Geometry
from hms.extensions import db


class BusinsSitutn(db.Model):
    """
    업종현황 모델 정의 클래스
    업종현황 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'busins_situtn'

    id = db.Column(db.Integer, db.Sequence('busins_situtn_id_seq'), primary_key=True)

    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    sid_cd = db.Column(db.String(2), nullable=False)
    sgg_cd = db.Column(db.String(5), nullable=False)
    emd_cd = db.Column(db.String(10), nullable=False)
    lcnsng_dt = db.Column(db.String(8), nullable=False)
    busins_clsftn_cd = db.Column(db.String(20), nullable=False)
    busins_condtn = db.Column(db.String(20))
    loctn_area = db.Column(db.Float)
    compny_nm = db.Column(db.String(60), nullable=False)
    prcl_zipcd = db.Column(db.String(6))
    road_zipcd = db.Column(db.String(7))
    prcl_addrs = db.Column(db.String(120))
    road_addrs = db.Column(db.String(120))
    loctn_phone = db.Column(db.String(35))

    def __init__(self, **kwargs):
        super(BusinsSitutn, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd, busins_clsftn_cd):
        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawSidArea.geom)).label('geojson')). \
             filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('geojson')

        results = db.session.query(
            geojson,
            cls.busins_clsftn_cd).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(cls.busins_clsftn_cd.in_(busins_clsftn_cd)).\
            group_by(geojson, cls.busins_clsftn_cd)

        return results

    @classmethod
    def find_by_filter_for_grid(cls, sid_cd, sgg_cd, emd_cd, busins_clsftn_cd):

        results = db.session.query(
                db.session.query(LawSidArea.sid_ko_nm).filter(LawSidArea.sid_cd == sid_cd).limit(1).label('sid'),
                db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == sgg_cd).limit(1).label('sgg'),
                db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == emd_cd).limit(1).label('emd'),
                cls.lcnsng_dt,
                cls.busins_clsftn_cd,
                cls.busins_condtn,
                cls.loctn_area,
                cls.compny_nm,
                cls.prcl_zipcd,
                cls.prcl_addrs,
                cls.road_zipcd,
                cls.road_addrs,
                cls.loctn_phone).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(cls.busins_clsftn_cd.in_(busins_clsftn_cd)).\
            group_by(
                     cls.lcnsng_dt,
                     cls.busins_clsftn_cd,
                     cls.busins_condtn,
                     cls.loctn_area,
                     cls.compny_nm,
                     cls.prcl_zipcd,
                     cls.prcl_addrs,
                     cls.road_zipcd,
                     cls.road_addrs,
                     cls.loctn_phone)

        print(results)

        return results
