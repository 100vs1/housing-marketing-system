# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import func, and_, or_, desc, asc, collate
from sqlalchemy.dialects import postgresql

from hms.extensions import db
from hms.blueprints.common.models.area import LawEmdArea


class SupplyPresentNew(db.Model):

    __bind_key__ = 'gisdb'
    __tablename__ = 'supply_present_new'

    id = db.Column(db.Integer, db.Sequence('supply_present_new_id_seq'), primary_key=True)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    sid_cd = db.Column(db.String(2), primary_key=True)
    sgg_cd = db.Column(db.String(5), primary_key=True)
    emd_cd = db.Column(db.String(10), primary_key=True)
    yyyymm = db.Column(db.String(6))
    house_management_num = db.Column(db.String(16))
    house_management_num2 = db.Column(db.String(10))
    contract_yyyymmdd_start = db.Column(db.String(8))
    contract_yyyymmdd_end = db.Column(db.String(8))
    move_in_yyyymm = db.Column(db.String(6))
    announcement_yyyymm = db.Column(db.String(8))
    result_announcement_yyyymm = db.Column(db.String(8))
    address = db.Column(db.String(200))
    bldng_ko_name = db.Column(db.String(80))
    news_paper = db.Column(db.String(50))
    builder = db.Column(db.String(50))
    developer = db.Column(db.String(50))
    homepage1 = db.Column(db.String(80))
    homepage2 = db.Column(db.String(80))
    result_announcement_media = db.Column(db.String(30))
    application_rank = db.Column(db.String(10))
    ex = db.Column(db.String(80))
    house_clsftn_name = db.Column(db.String(30))
    house_type = db.Column(db.String(20))
    house_type2 = db.Column(db.String(20))
    money_2nd = db.Column(db.String(20))
    tel = db.Column(db.String(20))
    supply_clsftn = db.Column(db.String(10))
    application_area = db.Column(db.String(20))
    competition_rate = db.Column(db.String(20))
    application_result = db.Column(db.String(30))
    plus_area = db.Column(db.String(30))
    receipt = db.Column(db.String(20))
    house_count = db.Column(db.Integer())
    supply_area = db.Column(db.Integer())
    price = db.Column(db.Integer())
    general_unit = db.Column(db.Integer())
    special_unit = db.Column(db.Integer())
    supply_unit = db.Column(db.Integer())
    application_count = db.Column(db.Integer())
    plus_min = db.Column(db.Integer())
    plus_max = db.Column(db.Integer())
    exclsv_area = db.Column(db.Float())
    price_per_supply_area = db.Column(db.Float())
    plus_mid = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    def __init__(self, **kwargs):
        super(SupplyPresentNew, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, sid_cd, sgg_cd, emd_cd,
                                 sp_sexarea, sp_eexarea,
                                 st_yyyymm, ed_yyyymm):

        result = db.session.query(
            cls.emd_cd
        ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).limit(1).first()

        return result is not None

    @classmethod
    def find_by_filter_for_list(cls, sid_cd, sgg_cd, emd_cd,
                                sp_sexarea, sp_eexarea,
                                st_yyyymm, ed_yyyymm):

        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.bldng_ko_name,
            cls.address
        ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            filter(cls.geom is not None).\
            group_by('geojson', cls.bldng_ko_name, cls.address). \
            order_by(asc(collate(cls.bldng_ko_name, 'C')))

        return result

    @classmethod
    def find_by_filter_for_card_list(cls, sid_cd, sgg_cd, emd_cd,
                                sp_sexarea, sp_eexarea,
                                st_yyyymm, ed_yyyymm):

        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.bldng_ko_name,
            cls.general_unit,
            cls.special_unit,
            cls.yyyymm,
            cls.move_in_yyyymm,
            cls.exclsv_area,
            cls.price,
            cls.price_per_supply_area
        ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            filter(cls.geom is not None).\
            order_by(asc(collate(cls.bldng_ko_name, 'C')), cls.exclsv_area)

        return result

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd,
                               sp_sexarea, sp_eexarea,
                               st_yyyymm, ed_yyyymm):

        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.bldng_ko_name,
            cls.address,
            cls.yyyymm,
            cls.supply_unit,
            cls.result_announcement_yyyymm,
            cls.contract_yyyymmdd_start,
            cls.contract_yyyymmdd_end,
            cls.supply_clsftn,
            cls.supply_area,
            cls.general_unit,
            cls.special_unit,
            cls.price,
            cls.price_per_supply_area,
            cls.developer,
            cls.builder,
            cls.homepage1,
            cls.homepage2
        ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            filter(cls.geom is not None)

        return result

    @classmethod
    def find_by_filter_for_contents(cls, bldng_ko_name, sgg_cd, emd_cd,
                                sp_sexarea, sp_eexarea,
                                st_yyyymm, ed_yyyymm):

        result = db.session.query(
            cls.exclsv_area,
            cls.price,
            cls.price_per_supply_area
        ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            filter(cls.geom is not None).\
            order_by(asc(collate(cls.bldng_ko_name, 'C')), cls.exclsv_area)

        return result

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd,
                               sp_sexarea, sp_eexarea,
                               st_yyyymm, ed_yyyymm):

        result = db.session.query(
            func.ST_AsGeoJSON(cls.geom).label('geojson'),
            cls.bldng_ko_name,
            cls.address,
            cls.yyyymm,
            cls.supply_unit,
            cls.result_announcement_yyyymm,
            cls.contract_yyyymmdd_start,
            cls.contract_yyyymmdd_end,
            cls.supply_clsftn,
            cls.supply_area,
            cls.general_unit,
            cls.special_unit,
            cls.price,
            cls.price_per_supply_area,
            cls.developer,
            cls.builder,
            cls.homepage1,
            cls.homepage2
        ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)).\
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            filter(cls.geom is not None)

        return result

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd,
                                  sp_type,
                                  sp_sexarea, sp_eexarea,
                                  st_yyyymm, ed_yyyymm):

        if sp_type == '1':
            total = func.sum(cls.supply_unit).label('total_sum')
        else:
            total = func.trunc(func.avg(cls.price_per_supply_area)).label('total_sum')

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        result = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            geojson,
            total
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)). \
            filter(cls.geom is not None).\
            group_by(cls.emd_cd)

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return result

    @classmethod
    def find_by_filter_for_bubble_start(cls, sid_cd, sgg_cd, emd_cd,
                                  sp_type,
                                  sp_sexarea, sp_eexarea,
                                  st_yyyymm, ed_yyyymm):

        if sp_type == '1':
            total = func.sum(cls.supply_unit).label('total_sum')
        else:
            total = func.trunc(func.avg(cls.price_per_supply_area)).label('total_sum')

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        result = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            geojson,
            total
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)). \
            filter(cls.yyyymm.like(st_yyyymm + '%')). \
            filter(cls.geom is not None).\
            group_by(cls.emd_cd)

        return result

    @classmethod
    def find_by_filter_for_bubble_end(cls, sid_cd, sgg_cd, emd_cd,
                                    sp_type,
                                    sp_sexarea, sp_eexarea,
                                    st_yyyymm, ed_yyyymm):
        if sp_type == '1':
            total = func.sum(cls.supply_unit).label('total_sum')
        else:
            total = func.trunc(func.avg(cls.price_per_supply_area)).label('total_sum')

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        result = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            geojson,
            total
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(and_(cls.supply_area >= sp_sexarea,
                        cls.supply_area <= sp_eexarea)). \
            filter(cls.yyyymm.like(ed_yyyymm + '%')). \
            filter(cls.geom is not None). \
            group_by(cls.emd_cd)

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return result
