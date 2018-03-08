# -*- coding: utf-8 -*-
from __future__ import print_function

from sqlalchemy import func, and_, or_, desc
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import compiler

from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea, AdmSidArea, AdmSggArea, \
    AdmEmdArea


class PopltnStats(db.Model):
    """
    인구통계 모델 정의 클래스
    인구통계 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'popltn_stats_new'  # 인구통계

    id = db.Column(db.Integer, primary_key=True)  # 시퀀스아이디

    sid_cd = db.Column(db.String(2), nullable=False)  # 시도코드
    sgg_cd = db.Column(db.String(5), nullable=False)  # 시군구코드
    emd_cd = db.Column(db.String(10), nullable=False)  # 읍면동코드
    yyyymm = db.Column(db.String(6), nullable=False)  # 조사년월(yyyymm)
    age_grp_cd = db.Column(db.String(20), nullable=False)  # 연령대코드
    # man_num = db.Column(db.Integer, nullable=False)  # 남자수
    # woman_num = db.Column(db.Integer, nullable=False)  # 여자수
    total_num = db.Column(db.Integer, nullable=False)  # 전체수

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PopltnStats, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm, ed_yyyymm):
        result = db.session.query(
                func.count(cls.emd_cd).label('data_count')
            ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.age_grp_cd.in_(age_grp_cds)). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm))

        return result[0][0]

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm,
                               ed_yyyymm):

        if sid_cd is not None:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmSidArea.geom)).label('geojson')). \
                filter(AdmSidArea.sid_cd == sid_cd).limit(1).label('geojson')
        elif sgg_cd is not None:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmSggArea.geom)).label('geojson')). \
                filter(AdmSggArea.sgg_cd == sgg_cd).limit(1).label('geojson')
        else:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
                filter(AdmEmdArea.emd_cd == emd_cd).limit(1).label('geojson')

        result = db.session.query(geojson,
                                   # local_name,
                                   func.sum(cls.total_num).label('total_num')). \
            filter(or_(cls.sid_cd == sid_cd,
                   cls.sgg_cd == sgg_cd,
                   cls.emd_cd == emd_cd)). \
            filter(cls.age_grp_cd.in_(age_grp_cds)). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)). \
            group_by(cls.yyyymm).\
            order_by(desc(cls.yyyymm)).limit(1)
        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return result

    @classmethod
    def find_by_filter_for_grid(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm,
                                                  ed_yyyymm):
        return db.session.query(cls.yyyymm,
                                   db.session.query(AdmSidArea.sid_ko_nm).
                                   filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
                                   db.session.query(AdmSggArea.sgg_ko_nm).
                                   filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
                                   db.session.query(AdmEmdArea.emd_ko_nm).
                                   filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd'),
                                   db.session.query(Code.name).
                                   filter(and_(Code.code == cls.age_grp_cd,
                                               Code.group_code == 'age_grp')).limit(1).label('age_grp'),
                                   # cls.man_num,
                                   # cls.woman_num,
                                   cls.total_num). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.age_grp_cd.in_(age_grp_cds)). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)). \
            order_by(desc(cls.yyyymm))

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd, yyyymm, age_grp_cds):
        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')).\
            filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        # 코드 분류는 필요하나 가독성 때문에 어쩔 수 없이 이렇게 개발해둠 sqlAlchemy ORM의 단점
        if sid_cd:
            result = db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
                                      filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                      geojson,
                                      func.sum(cls.total_num).label('total_sum')).\
                filter(cls.sid_cd == sid_cd).\
                filter(cls.age_grp_cd.in_(age_grp_cds)).\
                filter(cls.yyyymm == yyyymm).\
                group_by(cls.emd_cd)

        if sgg_cd:
            result = db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
                                      filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                      geojson,
                                      func.sum(cls.total_num).label('total_sum')). \
                filter(cls.sgg_cd == sgg_cd). \
                filter(cls.age_grp_cd.in_(age_grp_cds)). \
                filter(cls.yyyymm == yyyymm). \
                group_by(cls.emd_cd)

        if emd_cd:
            result = db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
                                      filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                      geojson,
                                      func.sum(cls.total_num).label('total_sum')). \
                filter(cls.emd_cd == emd_cd). \
                filter(cls.age_grp_cd.in_(age_grp_cds)). \
                filter(cls.yyyymm == yyyymm). \
                group_by(cls.emd_cd)

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return result

    # @classmethod
    # def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm, age_grp_cds):
    #     target_yyyymm = db.session.query(cls.yyyymm). \
    #         filter(and_(cls.yyyymm >= st_yyyymm,
    #                     cls.yyyymm <= ed_yyyymm)).\
    #         order_by(desc(cls.yyyymm)).limit(1)
    #
    #     if sid_cd:
    #         geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')).\
    #             filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')
    #
    #         result = db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
    #                                    filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
    #                                    geojson,
    #                                    func.sum(cls.total_num).label('total_sum')). \
    #             filter(cls.sid_cd == sid_cd). \
    #             filter(cls.age_grp_cd.in_(age_grp_cds)).\
    #             filter(cls.yyyymm == target_yyyymm).\
    #             group_by(cls.emd_cd)
    #
    #         print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
    #
    #         return result
    #
    #     if sgg_cd:
    #         geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
    #             filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')
    #         return db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
    #                                    filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
    #                                    geojson,
    #                                    func.sum(cls.total_num).label('total_sum')). \
    #             filter(cls.sgg_cd == sgg_cd). \
    #             filter(cls.age_grp_cd.in_(age_grp_cds)). \
    #             filter(cls.yyyymm == target_yyyymm). \
    #             group_by(cls.emd_cd)
    #
    #     if emd_cd:
    #         geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
    #             filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')
    #
    #         return db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
    #                                    filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
    #                                    geojson,
    #                                    func.sum(cls.total_num).label('total_sum')). \
    #             filter(cls.emd_cd == emd_cd). \
    #             filter(cls.age_grp_cd.in_(age_grp_cds)). \
    #             filter(and_(cls.yyyymm >= st_yyyymm,
    #                         cls.yyyymm <= ed_yyyymm)). \
    #             group_by(cls.emd_cd)

    @classmethod
    def find_by_filter_for_bubbleF(cls, sid_cd, sgg_cd, emd_cd, st_yyyymm, ed_yyyymm, age_grp_cds):
        target_yyyymm = db.session.query(cls.yyyymm). \
            filter(and_(cls.yyyymm >= st_yyyymm,
                        cls.yyyymm <= ed_yyyymm)). \
            order_by(desc(cls.yyyymm)).limit(1)

        if sid_cd:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
                filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

            return db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
                                    filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                    geojson,
                                    func.sum(cls.total_num).label('total_sum')). \
                filter(cls.sid_cd == sid_cd). \
                filter(cls.age_grp_cd.in_(age_grp_cds)). \
                filter(cls.yyyymm == target_yyyymm). \
                group_by(cls.emd_cd)

        if sgg_cd:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
                filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')
            return db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
                                    filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                    geojson,
                                    func.sum(cls.total_num).label('total_sum')). \
                filter(cls.sgg_cd == sgg_cd). \
                filter(cls.age_grp_cd.in_(age_grp_cds)). \
                filter(cls.yyyymm == target_yyyymm). \
                group_by(cls.emd_cd)

        if emd_cd:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(AdmEmdArea.geom)).label('geojson')). \
                filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

            return db.session.query(db.session.query(AdmEmdArea.emd_ko_nm).
                                    filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                    geojson,
                                    func.sum(cls.total_num).label('total_sum')). \
                filter(cls.emd_cd == emd_cd). \
                filter(cls.age_grp_cd.in_(age_grp_cds)). \
                filter(and_(cls.yyyymm >= st_yyyymm,
                            cls.yyyymm <= ed_yyyymm)). \
                group_by(cls.emd_cd)

    @classmethod
    def find_summary_by_geom(cls, geom):
        target_yyyymm = db.session.query(func.max(cls.yyyymm)).limit(1)

        target_emd = AdmEmdArea.find_emd_cds_by_geom(geom)

        target_emd_kor_nm = AdmEmdArea.find_emd_kor_nms_by_geom(geom)

        target_emd_kor_str = ''
        for item in target_emd_kor_nm:
            # target_emd_kor_str.append(item[0]);
            target_emd_kor_str += item[0] + ','
            # print(item[0])
        # print(target_emd_kor_str)

        popltn_sum = db.session.query(func.sum(cls.total_num)).\
            filter(cls.emd_cd.in_(target_emd)).\
            filter(cls.yyyymm == target_yyyymm).limit(1)

        return {
            'target_emd': target_emd_kor_nm,
            'ps_yyyymm': target_yyyymm,
            'popltn_sum': popltn_sum
        }


