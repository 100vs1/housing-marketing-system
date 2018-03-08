# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import func, and_, or_, desc
from sqlalchemy.dialects import postgresql

from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea, LawAreaMaster


class HsholdStats(db.Model):
    """
    인구주택총조사 모델 정의 클래스
    지역현황 > 인구주택총조사 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'hshold_stats'  #인구주택총조사

    id = db.Column(db.Integer, primary_key=True)  # 시퀀스아이디

    sid_cd = db.Column(db.String(2), nullable=False)  # 시도코드
    sgg_cd = db.Column(db.String(5), nullable=False)  # 시군구\코드
    srvy_year = db.Column(db.String(4), nullable=False)  # 조사년도
    rsdnc_clsftn_cd = db.Column(db.String(20), nullable=False)  # 거처분류코드
    fmly_num_cd = db.Column(db.String(20), nullable=False)  # 세대원수코드
    room_num_cd = db.Column(db.String(20), nullable=False)  # 방개수코드
    hshold_num = db.Column(db.Integer, nullable=False)  # 세대수

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(HsholdStats, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, sid_cd, sgg_cd, rsdnc_clsftn_cds, fmly_num_cds, room_num_cds, st_year, ed_year):
        result = db.session.query(
            func.count(cls.sid_cd)
        ).filter(or_(cls.sid_cd == sid_cd,
                     cls.sgg_cd == sgg_cd)). \
            filter(cls.rsdnc_clsftn_cd.in_(rsdnc_clsftn_cds)). \
            filter(cls.fmly_num_cd.in_(fmly_num_cds)). \
            filter(cls.room_num_cd.in_(room_num_cds)). \
            filter(and_(cls.srvy_year >= st_year,
                        cls.srvy_year <= ed_year))

        print(result.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return result[0][0]

    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, rsdnc_clsftn_cds, fmly_num_cds, room_num_cds, st_year, ed_year):
        # 서브 쿼리
        target_yyyymm = db.session.query(cls.srvy_year). \
            filter(and_(cls.srvy_year >= st_year,
                        cls.srvy_year <= ed_year)).\
            order_by(desc(cls.srvy_year)).limit(1)

        if sid_cd is not None:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawSidArea.geom)).label('geojson')).\
                filter(LawSidArea.sid_cd == sid_cd).limit(1).label('geojson')
        else:
            geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawSggArea.geom)).label('geojson')).\
                filter(LawSggArea.sgg_cd == sgg_cd).limit(1).label('geojson')

        results = db.session.query(geojson,
                                   func.sum(cls.hshold_num).label('hshold_sum')). \
            filter(or_(cls.sid_cd == sid_cd,
                   cls.sgg_cd == sgg_cd)). \
            filter(cls.rsdnc_clsftn_cd.in_(rsdnc_clsftn_cds)). \
            filter(cls.fmly_num_cd.in_(fmly_num_cds)). \
            filter(cls.room_num_cd.in_(room_num_cds)). \
            filter(cls.srvy_year == target_yyyymm). \
            group_by(cls.srvy_year).\
            order_by(desc(cls.srvy_year)).limit(1)
        print("START")
        print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        print("END")
        return results

    @classmethod
    def find_by_filter_for_grid(cls, sid_cds, sgg_cds, rsdnc_clsftn_cds, fmly_num_cds, room_num_cds, st_year, ed_year):

        results = db.session.query(
            db.session.query(LawSidArea.sid_ko_nm).
                filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
            db.session.query(LawSggArea.sgg_ko_nm).
                filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
            cls.rsdnc_clsftn_cd, cls.fmly_num_cd, cls.room_num_cd, cls.srvy_year, cls.hshold_num). \
            filter(or_(cls.sid_cd.in_(sid_cds),
                       cls.sgg_cd.in_(sgg_cds))). \
            filter(cls.rsdnc_clsftn_cd.in_(rsdnc_clsftn_cds)). \
            filter(cls.fmly_num_cd.in_(fmly_num_cds)). \
            filter(cls.room_num_cd.in_(room_num_cds)). \
            filter(and_(cls.srvy_year >= st_year,
                        cls.srvy_year <= ed_year))

        return results

    @classmethod
    def find_by_filter_for_bubble(cls, sid_cd, sgg_cd, rsdnc_clsftn_cds, fmly_num_cds, room_num_cds, st_year, ed_year):

        target_year = db.session.query(cls.srvy_year). \
            filter(and_(cls.srvy_year >= st_year,
                        cls.srvy_year <= ed_year)). \
            order_by(desc(cls.srvy_year)).limit(1)

        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawSggArea.geom)).label('geojson')).\
                filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('geojson')

        if sid_cd is not None:
            results = db.session.query(db.session.query(LawSggArea.sgg_ko_nm).
                                       filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('area_ko_nm'),
                                       geojson,
                                       func.sum(cls.hshold_num).label('total_sum'),
                                       cls.sgg_cd). \
                filter(cls.sgg_cd.in_(LawAreaMaster.find_sggs_by_sid_cd(sid_cd))).\
                filter(cls.rsdnc_clsftn_cd.in_(rsdnc_clsftn_cds)). \
                filter(cls.fmly_num_cd.in_(fmly_num_cds)). \
                filter(cls.room_num_cd.in_(room_num_cds)). \
                filter(cls.srvy_year == target_year).\
                group_by(cls.sgg_cd)
            return results

        if sgg_cd is not None:
            results = db.session.query(db.session.query(LawSggArea.sgg_ko_nm).
                                       filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('area_ko_nm'),
                                       geojson,
                                       func.sum(cls.hshold_num).label('total_sum')). \
                filter(cls.sgg_cd == sgg_cd). \
                filter(cls.rsdnc_clsftn_cd.in_(rsdnc_clsftn_cds)). \
                filter(cls.fmly_num_cd.in_(fmly_num_cds)). \
                filter(cls.room_num_cd.in_(room_num_cds)). \
                filter(cls.srvy_year == target_year).\
                group_by(cls.sgg_cd)

            print(results)
            return results
