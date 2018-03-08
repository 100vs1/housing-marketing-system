# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import func, and_, or_, desc, asc, collate
from sqlalchemy.dialects import postgresql

from hms.extensions import db
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class IdnftnBldng(db.Model):
    """
    입주물량 모델 정의 클래스
    입주물량 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'idntfn_bldng'

    id = db.Column(db.Integer, db.Sequence('idntfn_bldng_new_id_seq'), primary_key=True)

    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    sid_cd = db.Column(db.String(2))
    sgg_cd = db.Column(db.String(5))
    emd_cd = db.Column(db.String(10))
    area_location_kor = db.Column(db.String(80))
    manage_building_paper = db.Column(db.String(16))
    area_location_road_kor = db.Column(db.String(100))
    building_kor = db.Column(db.String(80))
    dong_kor = db.Column(db.String(80))
    ho_kor = db.Column(db.String(80))
    area_wide = db.Column(db.Float())
    build_wide = db.Column(db.Float())
    building_exist = db.Column(db.Float())
    total_area = db.Column(db.Float())
    adjust_area_per = db.Column(db.Float())
    area_ratio = db.Column(db.Float())
    main_build_code = db.Column(db.String(3))
    count_family = db.Column(db.Integer())
    count_house = db.Column(db.Integer())
    a_floor = db.Column(db.String(10))
    b_floor = db.Column(db.String(10))
    total_building_area = db.Column(db.Float())
    date_permission = db.Column(db.String(10))
    date_build = db.Column(db.String(16))
    permission_using_date = db.Column(db.String(16))
    year_permission = db.Column(db.String(6))
    house_in_building = db.Column(db.String(20))
    parking_sum = db.Column(db.Integer())
    ex_use = db.Column(db.String(80))
    main_use_code = db.Column(db.String(5))
    main_use_name = db.Column(db.String(80))
    height = db.Column(db.Integer())
    cnstrtn_area = db.Column(db.Float())
    house_clsftn_code = db.Column(db.String(1))
    house_count = db.Column(db.Integer())
    house_count_per_exclsv = db.Column(db.Integer())
    exclsv_area = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    def __init__(self, **kwargs):
        super(IdnftnBldng, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, sid_cd, sgg_cd, emd_cd,
                                 ib_house_kind, ib_sexarea, ib_eexarea,
                                 ib_syyyymm, ib_eyyyymm):

        result = db.session.query(
            cls.emd_cd
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.house_clsftn_code == ib_house_kind). \
            filter(and_(cls.exclsv_area >= ib_sexarea,
                        cls.exclsv_area <= ib_eexarea)). \
            filter(and_(cls.year_permission >= ib_syyyymm,
                        cls.year_permission <= ib_eyyyymm)). \
            filter(cls.geom is not None).limit(1).first()

        return result is not None

    @classmethod
    def find_by_filter_for_list(cls, sid_cd, sgg_cd, emd_cd,
                                ib_house_kind, ib_sexarea, ib_eexarea,
                                ib_syyyymm, ib_eyyyymm):

        result = db.session.query(
            func.ST_asGeoJSON(cls.geom).label('geojson'),
            cls.area_location_kor,
            cls.building_kor
        ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(cls.house_clsftn_code == ib_house_kind).\
            filter(and_(cls.exclsv_area >= ib_sexarea,
                        cls.exclsv_area <= ib_eexarea)).\
            filter(and_(cls.year_permission >= ib_syyyymm,
                        cls.year_permission <= ib_eyyyymm)).\
            filter(cls.geom is not None).\
            group_by('geojson', cls.area_location_kor, cls.building_kor).\
            order_by(asc(collate(cls.building_kor, 'C')))

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return result

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd,
                               ib_house_kind, ib_sexarea, ib_eexarea,
                               ib_syyyymm, ib_eyyyymm):
        result = db.session.query(
            func.ST_asGeoJSON(cls.geom).label('geojson'),
            cls.exclsv_area,
            cls.count_family,
            cls.area_location_kor,
            cls.building_kor,
            cls.area_wide,
            cls.build_wide,
            cls.building_exist,
            cls.area_ratio,
            cls.a_floor,
            cls.b_floor,
            cls.year_permission,
            cls.parking_sum,
            cls.height
        ). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.house_clsftn_code == ib_house_kind). \
            filter(and_(cls.exclsv_area >= ib_sexarea,
                        cls.exclsv_area <= ib_eexarea)). \
            filter(and_(cls.year_permission >= ib_syyyymm,
                        cls.year_permission <= ib_eyyyymm)). \
            filter(cls.geom is not None). \
            order_by(asc(collate(cls.building_kor, 'C')))

        return result

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd,
                                  ib_house_kind, ib_sexarea, ib_eexarea,
                                  ib_syyyymm, ib_eyyyymm):
        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        result = db.session.query(
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
            geojson,
            func.count(cls.count_family).label('total_sum')
        ).filter(or_(cls.sid_cd == sid_cd,
                     cls.sgg_cd == sgg_cd,
                     cls.emd_cd == emd_cd)). \
            filter(cls.house_clsftn_code == ib_house_kind). \
            filter(and_(cls.exclsv_area >= ib_sexarea,
                        cls.exclsv_area <= ib_eexarea)). \
            filter(cls.year_permission == ib_eyyyymm). \
            filter(cls.year_permission is not None). \
            filter(cls.geom is not None).\
            group_by(cls.emd_cd)

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return result
