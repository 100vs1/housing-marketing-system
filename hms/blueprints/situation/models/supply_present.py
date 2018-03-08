# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import func, and_, or_, desc, asc, collate

from hms.extensions import db
from hms.blueprints.common.models.area import LawEmdArea


class SupplyPresent(db.Model):

    __bind_key__ = 'gisdb'
    __tablename__ = 'supply_present'

    id = db.Column(db.Integer(), primary_key=True)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    sid_cd = db.Column(db.String(2))
    sgg_cd = db.Column(db.String(5))
    emd_cd = db.Column(db.String(10))
    yyyymm = db.Column(db.Integer())
    house_mana = db.Column(db.String(16))
    address = db.Column(db.String(120))
    house_sep = db.Column(db.String(10))
    building_nm = db.Column(db.String(80))
    date_winning = db.Column(db.String(16))
    total_area = db.Column(db.Float())
    rank_code = db.Column(db.Integer())
    rank = db.Column(db.String(16))
    target_area = db.Column(db.String(16))
    supply_house = db.Column(db.Integer())
    recive_count = db.Column(db.Integer())
    compet_rate = db.Column(db.Integer())
    plus_area = db.Column(db.String(10))
    plus_min = db.Column(db.Integer())
    plus_max = db.Column(db.Integer())
    plus_avg = db.Column(db.Float())
    supply_estimate = db.Column(db.Integer())
    sep_1 = db.Column(db.String(1))
    sep_2 = db.Column(db.String(1))
    sep_3 = db.Column(db.String(1))
    sep_4 = db.Column(db.String(1))
    date_contract = db.Column(db.String(40))
    house_kind = db.Column(db.String(16))
    supply_area = db.Column(db.Float())
    total_supply = db.Column(db.Integer())
    supply_price = db.Column(db.Integer())
    price_area = db.Column(db.Float())

    def __init__(self, **kwargs):
        super(SupplyPresent, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm):
        result = db.session.query(
            func.count(cls.id).label('data_count')
        ).filter(or_(cls.sid_cd == sid_cd,
                     cls.sgg_cd == sgg_cd,
                     cls.emd_cd == emd_cd)). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).limit(1)

        return result[0][0]

    @classmethod
    def find_by_filter_for_list(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm):
        geojson = func.ST_AsGeoJSON(cls.geom).label('geojson')

        result = db.session.query(
                geojson,
                cls.building_nm,
                cls.address,
                func.count(cls.id).label('group_count'),
            ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            group_by(geojson, cls.building_nm, cls.address).\
            order_by(asc(collate(cls.building_nm, '"C"')))

        return result

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm):
        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.yyyymm,
            cls.house_mana,
            cls.address,
            cls.house_sep,
            cls.building_nm,
            cls.date_winning,
            cls.total_area,
            cls.rank_code,
            cls.rank,
            cls.target_area,
            cls.supply_house,
            cls.recive_count,
            cls.compet_rate,
            cls.plus_area,
            cls.plus_min,
            cls.plus_max,
            cls.plus_avg,
            cls.supply_estimate,
            cls.sep_1,
            cls.sep_2,
            cls.sep_3,
            cls.sep_4,
            cls.date_contract,
            cls.house_kind,
            cls.supply_area,
            cls.total_supply,
            cls.supply_price,
            cls.price_area).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm))
        return result

    @classmethod
    def find_by_filter_for_map_two(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm):

        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.building_nm,
            "ARRAY["
            "'house_kind:' || supply_present.house_kind, "
            "'house_kind_count:' || count(supply_present.id), "
            "'price_area:' || supply_present.price_area"
            "] as result",
            ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                          cls.yyyymm <= ed_yyyymm)).\
            group_by('geojson', cls.house_kind, cls.price_area, cls.building_nm)

        return result

#         return select sp1.building_nm, array_to_string(array_agg(distinct sp1.result), ',') from
# (select geom, building_nm, count(id) as house_kind_count, house_kind, yyyymm, price_area, ARRAY[
#           'house_kind_count:' || count(id)
#           ,'price_area:' || price_area
#           ,'house_kind:' || house_kind
#     	  ,'supply_pricd' || supply_price
#         ]  AS result
# from supply_present
# where '201611' <= yyyymm and yyyymm <= '201711'
# group by geom, house_kind, building_nm, yyyymm, price_area, supply_price) as sp1
# group by sp1.building_nm;


    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm):
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

    @classmethod
    def find_summary_by_geom(cls, geom):
        target_yyyymm = db.session.query(func.max(cls.yyyymm)).limit(1)

        parcel_area_sum = db.session.query(
            func.count(cls.id).label('parcel_area_sum'),
        ). \
            filter(cls.yyyymm == target_yyyymm). \
            filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326)))

        parcel_trnstn_sum = db.session.query(
            func.sum(cls.supply_house).label('parcel_trnstn_sum'),
        ). \
            filter(cls.yyyymm == target_yyyymm). \
            filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326)))

        floor_price_avg = db.session.query(
            func.avg(cls.price_area).label('floor_price_avg')
        ). \
            filter(cls.yyyymm == target_yyyymm). \
            filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326)))

        return {
            'sp_yyyymm': target_yyyymm,
            'parcel_area_sum': parcel_area_sum,
            'parcel_trnstn_sum': parcel_trnstn_sum,
            'floor_price_avg': floor_price_avg
        }

