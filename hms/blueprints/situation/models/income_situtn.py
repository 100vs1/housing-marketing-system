# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import or_, and_, asc, func
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class IncomeSitutn(db.Model):
    """
    소득현황 모델 정의 클래스
    지역현황 > 수여현황 메뉴에서 사용함
    """

    __bind_key__ = 'gisdb'
    __table_name__ = 'income_situtn'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sid_cd = db.Column(db.String(2))
    sgg_cd = db.Column(db.String(5))
    sid_ko_nm = db.Column(db.String())
    sgg_ko_nm = db.Column(db.String())
    co_income = db.Column(db.Integer())
    sgg_income = db.Column(db.Integer())
    centroid_geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    def __init__(self, **kwargs):
        super(IncomeSitutn, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd):

        result = db.session.query(
            cls.sgg_cd,
            cls.sid_ko_nm,
            cls.sgg_ko_nm,
            cls.co_income,
            cls.sgg_income,
            func.ST_AsGeoJSON(func.ST_Centroid(cls.centroid_geom)).label('geojson')).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd))

        return result

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd):

        result = db.session.query(
            cls.sgg_ko_nm,
            func.ST_AsGeoJSON(func.ST_Centroid(cls.centroid_geom)).label('geojson'),
            cls.co_income,
            cls.sgg_income).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd))

        return result

    @classmethod
    def find_by_filter_for_grid(cls, sid_cd, sgg_cd):

        result = db.session.query(
            cls.sid_ko_nm,
            cls.sgg_ko_nm,
            cls.co_income,
            cls.sgg_income). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd))

        return result
