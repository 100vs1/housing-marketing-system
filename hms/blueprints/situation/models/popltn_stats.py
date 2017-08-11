# -*- coding: utf-8 -*-
from sqlalchemy import func, and_

from hms.extensions import db
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class PopltnStats(db.Model):
    """
    인구통계 모델 정의 클래스
    인구통계 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'popltn_stats' # 인구통계

    id = db.Column(db.Integer, primary_key=True) # 시퀀스아이디

    sid_cd = db.Column(db.String(2), nullable=False) # 시도코드
    sgg_cd = db.Column(db.String(5), nullable=False) # 시군구코드
    emd_cd = db.Column(db.String(10), nullable=False) # 읍면동코드
    srvy_yyyymm = db.Column(db.String(6), nullable=False) # 조사년월(yyyymm)
    age_grp_cd = db.Column(db.String(20), nullable=False) # 연령대코드
    man_num = db.Column(db.Integer, nullable=False) # 남자수
    woman_num = db.Column(db.Integer, nullable=False) # 여자수
    total_num = db.Column(db.Integer, nullable=False) # 전체수

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PopltnStats, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):

        return PopltnStats.query. \
            filter(PopltnStats.id == identity).first()

    @classmethod
    def select_all(cls, sid_cds, sgg_cds, emd_cds, age_grp_cds, syear, smonth, eyear, emonth):
        sid_nm = db.session.query(LawSidArea.sid_ko_nm). \
            filter(LawSidArea.sid_cd == cls.sid_cd). \
            limit(1).label('area_nm')
        sgg_nm = db.session.query(LawSggArea.sgg_ko_nm). \
            filter(LawSggArea.sgg_cd == cls.sgg_cd). \
            limit(1).label('area_nm')
        emd_nm = db.session.query(LawEmdArea.emd_ko_nm). \
            filter(LawEmdArea.emd_cd == cls.emd_cd). \
            limit(1).label('area_nm')

        sid_ps = db.session.query(sid_nm,
                              func.sum(PopltnStats.man_num).label('man_sum'),
                              func.sum(PopltnStats.woman_num).label('woman_sum'),
                              func.sum(PopltnStats.total_num).label('total_sum')). \
            filter(and_(PopltnStats.sid_cd.in_(sid_cds),
                        PopltnStats.age_grp_cd.in_(age_grp_cds),
                        PopltnStats.srvy_yyyymm >= (syear + smonth),
                        PopltnStats.srvy_yyyymm <= (eyear + emonth))). \
            group_by(PopltnStats.sid_cd). \
            order_by(PopltnStats.sid_cd)

        sgg_ps = db.session.query(sgg_nm,
                              func.sum(PopltnStats.man_num).label('man_sum'),
                              func.sum(PopltnStats.woman_num).label('woman_sum'),
                              func.sum(PopltnStats.total_num).label('total_sum')). \
            filter(and_(PopltnStats.sigu_cd.in_(sgg_cds),
                        PopltnStats.age_grp_cd.in_(age_grp_cds),
                        PopltnStats.srvy_yyyymm >= (syear + smonth),
                        PopltnStats.srvy_yyyymm <= (eyear + emonth))). \
            group_by(PopltnStats.sgg_cd). \
            order_by(PopltnStats.sgg_cd)

        emd_ps = db.session.query(emd_nm,
                              func.sum(PopltnStats.man_num).label('man_sum'),
                              func.sum(PopltnStats.woman_num).label('woman_sum'),
                              func.sum(PopltnStats.total_num).label('total_sum')). \
            filter(and_(PopltnStats.emd_cd.in_(emd_cds),
                        PopltnStats.age_cd.in_(age_grp_cds),
                        PopltnStats.srvy_yyyymm >= (syear + smonth),
                        PopltnStats.srvy_yyyymm <= (eyear + emonth))). \
            group_by(PopltnStats.emd_cd). \
            order_by(PopltnStats.emd_cd)

        return sid_ps.union_all(sgg_ps, emd_ps)
