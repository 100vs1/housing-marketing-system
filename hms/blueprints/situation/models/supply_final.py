# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import func, and_, or_, desc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class SupplyFinal(db.Model):

    __bind_key__ = 'gisdb'
    __tablename__ = 'supply_final'

    sid_cd = db.Column(db.String(2), primary_key=True)
    sgg_cd = db.Column(db.String(5), primary_key=True)
    emd_cd = db.Column(db.String(10), primary_key=True)
    geom = db.Column(Geometry(geometry_type='POLYGON', srid=4326))
    address = db.Column(db.String(80))
    yyyymm = db.Column(db.String(6))
    building_n = db.Column(db.String(60))
    supply_est = db.Column(db.String(20))
    sep_1 = db.Column(db.Integer)
    sep_2 = db.Column(db.Integer)
    sep_3 = db.Column(db.Integer)
    sep_4 = db.Column(db.Integer)
    date_in = db.Column(db.String(10))
    # advertisem = db.Column(db.String(10))
    # channal = db.Column(db.String(40))
    date_winni = db.Column(db.String(10))
    # homepage1 = db.Column(db.String(80))
    # homepage2 = db.Column(db.String(80))
    # winning_ch = db.Column(db.String(20))
    # date_contr = db.Column(db.String(25))
    # rank_cod = db.Column(db.Integer)
    # field_20 = db.Column(db.String)
    # etc1 = db.Column(db.String)
    # etc2 = db.Column(db.String)
    # apply_loca = db.Column(db.Integer)
    # house_sep_ = db.Column(db.Integer)
    # house_mana = db.Column(db.String)
    # house_kind = db.Column(db.String)
    # supply_are = db.Column(db.Float)
    # house_ki_1 = db.Column(db.String)
    # supply_pri = db.Column(db.Integer)
    # second_pay = db.Column(db.String)
    # building_c = db.Column(db.String)
    # builder = db.Column(db.String)
    # tel = db.Column(db.String)
    price_area = db.Column(db.String)

    def __init__(self, **kwargs):
        super(SupplyFinal, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm):
        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.address,
            cls.yyyymm,
            cls.building_n,
            cls.supply_est,
            cls.sep_1,
            cls.sep_2,
            cls.sep_3,
            cls.sep_4,
            cls.date_in).\
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
                                  func.ST_AsGeoJSON(cls.geom).label('geojson'),
                                  func.count(cls.emd_cd).label('total_sum')).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            group_by(cls.emd_cd, 'geojson')

        return result
