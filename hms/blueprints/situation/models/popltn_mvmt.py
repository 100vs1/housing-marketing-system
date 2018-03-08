# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
from sqlalchemy import func, and_, or_, desc, cast, DATE, asc, collate
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import compiler

from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import AdmSidArea, AdmSggArea, AdmEmdArea
from geoalchemy2.types import Geometry
from hms.extensions import db


class PopltnMvmt(db.Model):
    """
    인구이동 모델 정의 클래스
    인구이동 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'popltn_mvmt'  # 인구이동

    id = db.Column(db.Integer, primary_key=True)  # 시퀀스아이디

    in_sid_cd = db.Column(db.String(2), nullable=False)  # 전입시도코드
    in_sgg_cd = db.Column(db.String(5), nullable=False)  # 전입시군구코드
    in_emd_cd = db.Column(db.String(10), nullable=False)  # 전입읍면동코드
    in_yyyymm = db.Column(db.String(6), nullable=False)  # 전입년월
    out_sid_cd = db.Column(db.String(2), nullable=False)  # 전출시도코드
    out_sgg_cd = db.Column(db.String(5), nullable=False)  # 전출시군구코드
    out_emd_cd = db.Column(db.String(10), nullable=False)  # 전출읍면동코드
    mv_reasn_cd = db.Column(db.String(20), nullable=False)  # 이동사유코드
    aplcnt_clsftn_cd = db.Column(db.String(20), nullable=False)  # 신청인구분코드
    aplcnt_age_cd = db.Column(db.Integer)  # 신청인나이
    aplcnt_sex_cd = db.Column(db.String(20), nullable=False)  # 신청인성별코드
    fmly_num = db.Column(db.Integer, nullable=False)  # 세대수

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PopltnMvmt, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd, in_emd_cd,
                               mv_reasn_cds, aplcnt_age_cds, fmly_nums, st_yyyymm, ed_yyyymm):
        result = db.session.query(
                func.count(cls.id)
            ).\
            filter(or_(cls.out_sid_cd == out_sid_cds,
                       cls.out_sgg_cd == out_sgg_cds,
                   cls.out_emd_cd == out_emd_cds)). \
            filter(cls.aplcnt_age_cd.in_(aplcnt_age_cds)). \
            filter(cls.mv_reasn_cd.in_(mv_reasn_cds)). \
            filter(cls.fmly_num.in_(fmly_nums)). \
            filter(or_(cls.in_sid_cd == in_sid_cd,
                       cls.in_sgg_cd == in_sgg_cd,
                       cls.in_emd_cd == in_emd_cd)). \
            filter(and_(cls.in_yyyymm >= st_yyyymm,
                        cls.in_yyyymm <= ed_yyyymm))

        return result[0][0]

    @classmethod
    def find_by_filter_for_map(cls, out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd, in_emd_cd,
                               mv_reasn_cds, aplcnt_age_cds, fmly_nums, st_yyyymm, ed_yyyymm):
        # 서브 쿼리
        geojson = ''
        if in_sid_cd is not None:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmSidArea.geom)).label('geojson')). \
                filter(AdmSidArea.sid_cd == cls.in_sid_cd).limit(1).label('geojson')
            group_by_target = cls.in_sid_cd
        elif in_sgg_cd is not None:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmSggArea.geom)).label('geojson')). \
                filter(AdmSggArea.sgg_cd == cls.in_sgg_cd).limit(1).label('geojson')
            group_by_target = cls.in_sgg_cd
        elif in_emd_cd is not None:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
                filter(AdmEmdArea.emd_cd == cls.in_emd_cd).limit(1).label('geojson')
            group_by_target = cls.in_emd_cd

        results = db.session.query(geojson,
                                   func.count(cls.fmly_num).label('hshold_cnt'),
                                   func.sum(cls.fmly_num).label('fmly_sum')). \
            filter(or_(cls.out_sid_cd == out_sid_cds,
                       cls.out_sgg_cd == out_sgg_cds,
                       cls.out_emd_cd == out_emd_cds)). \
            filter(cls.aplcnt_age_cd.in_(aplcnt_age_cds)). \
            filter(cls.mv_reasn_cd.in_(mv_reasn_cds)). \
            filter(cls.fmly_num.in_(fmly_nums)). \
            filter(or_(cls.in_sid_cd == in_sid_cd,
                       cls.in_sgg_cd == in_sgg_cd,
                       cls.in_emd_cd == in_emd_cd)). \
            filter(and_(cls.in_yyyymm >= st_yyyymm,
                        cls.in_yyyymm <= ed_yyyymm)). \
            group_by(group_by_target)

        return results

    @classmethod
    def find_by_filter_for_bubble(cls, out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd, in_emd_cd,
                                mv_reasn_cds, aplcnt_age_cds, fmly_nums, st_yyyymm, ed_yyyymm):

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
            filter(AdmEmdArea.emd_cd == cls.in_emd_cd).limit(1).label('geojson')

        result = db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
                                  filter(AdmEmdArea.emd_cd == cls.in_emd_cd).limit(1).label('area_ko_nm'),
                                  geojson,
                                  cls.in_emd_cd,
                                  func.sum(cls.fmly_num).label('total_sum')). \
            filter(or_(cls.out_sid_cd == out_sid_cds,
                       cls.out_sgg_cd == out_sgg_cds,
                       cls.out_emd_cd == out_emd_cds)). \
            filter(or_(cls.in_sid_cd == in_sid_cd,
                       cls.in_sgg_cd == in_sgg_cd,
                       cls.in_emd_cd == in_emd_cd)). \
            filter(cls.aplcnt_age_cd.in_(aplcnt_age_cds)). \
            filter(cls.mv_reasn_cd.in_(mv_reasn_cds)). \
            filter(cls.fmly_num.in_(fmly_nums)). \
            filter(and_(cls.in_yyyymm >= st_yyyymm,
                        cls.in_yyyymm <= ed_yyyymm)). \
            group_by(cls.in_emd_cd)

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        return result

    @classmethod
    def find_summary_by_geom(cls, geom):
        target_yyyymm = db.session.query(func.max(cls.in_yyyymm)).limit(1)

        target_emd = AdmEmdArea.find_emd_cds_by_geom(geom)

        in_popltn_sum = db.session.query(func.count(cls.id)).\
            filter(cls.in_emd_cd.in_(target_emd)).\
            filter(cls.in_yyyymm == target_yyyymm).limit(1)

        out_popltn_sum = db.session.query(func.count(cls.id)). \
            filter(cls.out_emd_cd.in_(target_emd)). \
            filter(cls.in_yyyymm == target_yyyymm).limit(1)

        return {
            'pm_yyyymm': target_yyyymm,
            'in_popltn_sum': in_popltn_sum,
            'out_popltn_sum': out_popltn_sum,
        }