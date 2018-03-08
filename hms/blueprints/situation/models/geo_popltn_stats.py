# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2.types import Geometry
from sqlalchemy import func, and_, asc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class GeoPopltnStats(db.Model):
    """
    인구통계 버블 차트용 모델 정의 클래스
    지역현황 > 업종현황 메뉴에서 사용함
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'geo_popltn_stats'

    area_cd = db.Column(db.String(10), primary_key=True, nullable=False)
    area_type = db.Column(db.String(1), primary_key=True, nullable=False)
    srvy_yyyymm = db.Column(db.Integer, primary_key=True, nullable=False)
    age_grp_cd = db.Column(db.String(6), primary_key=True, nullable=False)
    centroid_geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    popltn_cnt = db.Column(db.Integer)
    area_ko_nm = db.Column(db.String(80))
    area_en_nm = db.Column(db.String(80))

    def __init__(self, **kwargs):
        super(GeoPopltnStats, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm, age_grp_cds):
        if(sid_cd):
            target_area_cd = sid_cd
            hoho_cd = str(sgg_cd) + "00000000"
        elif(sgg_cd):
            target_area_cd = sgg_cd
            hoho_cd = str(sgg_cd) + "00000"
        else:
            target_area_cd = emd_cd
            hoho_cd = str(sgg_cd) + "00"

        print("*" * 50)
        print(sid_cd)
        print(sgg_cd)
        print(emd_cd)
        print(st_yyyymm)
        print(ed_yyyymm)
        print(age_grp_cds)
        print(target_area_cd)
        print("*" * 50)

        # (target_area_cd + '%')

        results = db.session.query(cls.area_cd,
                                   func.ST_AsGeoJSON(func.ST_Centroid(cls.centroid_geom)).label('geojson'),
                                   func.sum(cls.popltn_cnt).label('popltn_sum')). \
            filter(and_(cls.srvy_yyyymm >= st_yyyymm,
                        cls.srvy_yyyymm <= ed_yyyymm)). \
            filter(and_(cls.area_cd.like(target_area_cd + '%'),
                        cls.area_cd != hoho_cd)). \
            filter(cls.age_grp_cd.in_(age_grp_cds)).\
            group_by(cls.area_cd, cls.centroid_geom)

        # results = db.session.query(cls.area_cd,
        #                            cls.centroid_geom,
        #                            func.sum(cls.popltn_cnt).label('popltn_sum')).\
        #     filter(and_(cls.srvy_yyyymm >= st_yyyymm,
        #                 cls.srvy_yyyymm <= ed_yyyymm)). \
        #     filter(cls.age_grp_cd.in_(age_grp_cds)). \
        #     group_by(cls.area_cd, cls.centroid_geom)

        return results
