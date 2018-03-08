# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import func, and_, or_, desc
from sqlalchemy.dialects import postgresql

from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import AdmSidArea, AdmSggArea, AdmEmdArea


class HsholdImgrat(db.Model):
    """
    세대통계 모델 정의 클ㄹ래스
    지역현황 > 세대통계 메뉴에서 사용함
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'hshold_imgrat_new'

    sid_cd = db.Column(db.String(2), primary_key=True)
    sgg_cd = db.Column(db.String(5), primary_key=True)
    emd_cd = db.Column(db.String(10), primary_key=True)
    hshold_num_cd = db.Column(db.String(2), primary_key=True)
    yyyymm = db.Column(db.String(6), primary_key=True)

    hshold_num = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(HsholdImgrat, self).__init__(**kwargs)
    
    #맵 용
    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd, hshold_num_cds, st_yyyymm, ed_yyyymm):
        target_yyyymm = db.session.query(cls.yyyymm). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            order_by(desc(cls.yyyymm)).limit(1)

        if sid_cd:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmSidArea.geom)).label('geojson')). \
                filter(AdmSidArea.sid_cd == cls.sid_cd).limit(1).label('geojson')
        elif sgg_cd:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmSggArea.geom)).label('geojson')). \
                filter(AdmSggArea.sgg_cd == cls.sgg_cd).limit(1).label('geojson')
        else:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
                filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        results = db.session.query(geojson,
                                   cls.hshold_num).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.hshold_num_cd.in_(hshold_num_cds)).\
            filter(cls.yyyymm == target_yyyymm)
        print(results)

        return results

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd, hshold_num_cds, st_yyyymm, ed_yyyymm):
        target_yyyymm = db.session.query(cls.yyyymm). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)).\
            order_by(desc(cls.yyyymm)).limit(1)

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
            filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        results = db.session.query(cls.emd_cd,
            db.session.query(AdmEmdArea.emd_ko_nm).
                                   filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                   geojson,
                                   func.sum(cls.hshold_num).label('total_sum')).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.hshold_num_cd.in_(hshold_num_cds)). \
            filter(cls.yyyymm == target_yyyymm).\
            group_by(cls.emd_cd)

        print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return results

    # @classmethod
    # def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd, hshold_num_cds, yyyymm):
    #
    #     geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
    #         filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')
    #
    #     results = db.session.query(cls.emd_cd,
    #         db.session.query(AdmEmdArea.emd_ko_nm).
    #                                filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
    #                                geojson,
    #                                func.sum(cls.hshold_num).label('total_sum')).\
    #         filter(or_(cls.sid_cd == sid_cd,
    #                    cls.sgg_cd == sgg_cd,
    #                    cls.emd_cd == emd_cd)). \
    #         filter(cls.hshold_num_cd.in_(hshold_num_cds)). \
    #         filter(cls.yyyymm == yyyymm).\
    #         group_by(cls.emd_cd)
    #
    #     print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
    #     return results

    @classmethod
    def find_summary_by_geom(cls, geom):
        target_yyyymm = db.session.query(func.max(cls.yyyymm)).limit(1)

        target_emd = AdmEmdArea.find_emd_cds_by_geom(geom)

        household_sum = db.session.query(
                func.sum(cls.hshold_num)
            ).\
            filter(cls.yyyymm == target_yyyymm).\
            filter(cls.emd_cd.in_(target_emd))

        return {
            'hi_yyyymm': target_yyyymm,
            'household_sum': household_sum
        }