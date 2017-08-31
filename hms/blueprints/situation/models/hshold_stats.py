# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import func, and_, or_, desc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class HsholdStats(db.Model):
    """
    세대통계 모델 정의 클래스
    지역현황 > 세대통계 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'hshold_stats'  # 세대통계

    id = db.Column(db.Integer, primary_key=True)  # 시퀀스아이디

    sid_cd = db.Column(db.String(2), nullable=False)  # 시도코드
    sgg_cd = db.Column(db.String(5), nullable=False)  # 시군구코드
    srvy_year = db.Column(db.String(4), nullable=False)  # 조사년도
    rsdnc_clsftn_cd = db.Column(db.String(20), nullable=False)  # 거처분류코드
    fmly_num_cd = db.Column(db.String(20), nullable=False)  # 세대원수코드
    room_num_cd = db.Column(db.String(20), nullable=False)  # 방개수코드
    hshold_num = db.Column(db.Integer, nullable=False)  # 세대수

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(HsholdStats, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_map(cls, sid_cds, sgg_cds, rsdnc_clsftn_cds, fmly_num_cds, room_num_cds, st_year, ed_year):
        # 서브 쿼리
        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawSidArea.geom)).label('geojson')). \
            filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('geojson')

        results = db.session.query(geojson,
                                   func.sum(cls.hshold_num).label('hshold_sum')). \
            filter(or_(cls.sid_cd.in_(sid_cds),
                       cls.sgg_cd.in_(sgg_cds))). \
            filter(cls.rsdnc_clsftn_cd.in_(rsdnc_clsftn_cds)). \
            filter(cls.fmly_num_cd.in_(fmly_num_cds)). \
            filter(cls.room_num_cd.in_(room_num_cds)). \
            filter(and_(cls.srvy_year >= st_year,
                       cls.srvy_year <= ed_year)). \
            group_by(cls.sid_cd)

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
