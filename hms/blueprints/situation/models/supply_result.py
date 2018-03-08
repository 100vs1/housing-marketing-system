# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import func, and_, or_, desc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class SupplyResult(db.Model):
    """

    """

    __bind_key__ = 'gisdb'
    __table_name__ = 'supply_result'

    id = db.Column(db.Integer, primary_key=True)
    sid_cd = db.Column(db.String(2))
    sgg_cd = db.Column(db.String(5))
    emd_cd = db.Column(db.String(10))
    geom = db.Column(db.String())
    # address = db.Column(db.String(80))
    # house_mana = db.Column(db.String(20))
    # house_sep = db.Column(db.String(10))
    yyyymm = db.Column(db.Integer)
    building_nm = db.Column(db.String(40))
    date_winni = db.Column(db.String(20))
    total_area = db.Column(db.Float)
    # house_kind = db.Column(db.String(10))
    rank = db.Column(db.String(10))
    custom_address = db.Column(db.String(80))
    supply_house = db.Column(db.Integer)
    recive_count = db.Column(db.String(20))
    compet_rate = db.Column(db.String(20))
    plus_area = db.Column(db.String(20))
    plus_min = db.Column(db.String(20))
    plus_max = db.Column(db.String(20))
    plus_avg = db.Column(db.String(20))
    # latitude = db.Column(db.Float)
    # longitude = db.Column(db.Float)

    def __init__(self, **kwargs):
        super(SupplyResult, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm):
        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.yyyymm,
            cls.building_nm,
            cls.date_winni,
            cls.total_area,
            cls.rank,
            cls.custom_address,
            cls.supply_house,
            cls.recive_count,
            cls.compet_rate,
            cls.plus_area,
            cls.plus_min,
            cls.plus_max,
            cls.plus_avg,).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm))
        return result

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm):
        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
                filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        result = db.session.query(db.session.query(LawEmdArea.emd_ko_nm).
                                  filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                  geojson,
                                  func.count(cls.emd_cd).label('total_sum')).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)). \
            group_by(cls.emd_cd)

        return result
