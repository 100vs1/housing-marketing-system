# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import func, and_, or_, desc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


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
    def find_by_filter_for_map(cls, out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd, in_emd_cd,
                               mv_reasn_cds, aplcnt_age_cds, aplcnt_sex_cds, fmly_nums, st_yyyymm, ed_yyyymm):
        # 서브 쿼리
        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawSidArea.geom)).label('geojson')). \
            filter(LawSidArea.sid_cd == cls.in_sid_cd).limit(1).label('geojson')

        results = db.session.query(geojson,
                                   func.count(cls.fmly_num).label('hshold_cnt'),
                                   func.sum(cls.fmly_num).label('fmly_sum')). \
            filter(or_(cls.out_sid_cd.in_(out_sid_cds),
                       cls.out_sgg_cd.in_(out_sgg_cds),
                       cls.out_emd_cd.in_(out_emd_cds))). \
            filter(cls.aplcnt_age_cd.in_(aplcnt_age_cds)). \
            filter(cls.aplcnt_sex_cd.in_(aplcnt_sex_cds)). \
            filter(cls.mv_reasn_cd.in_(mv_reasn_cds)). \
            filter(cls.fmly_num.in_(fmly_nums)). \
            filter(or_(cls.in_sid_cd == in_sid_cd,
                       cls.in_sgg_cd == in_sgg_cd,
                       cls.in_emd_cd == in_emd_cd)). \
            filter(and_(cls.in_yyyymm >= st_yyyymm,
                        cls.in_yyyymm <= ed_yyyymm)). \
            group_by(cls.in_sid_cd)

        return results

    @classmethod
    def find_by_filter_for_grid(cls, out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd, in_emd_cd,
                                mv_reasn_cds, aplcnt_age_cds, aplcnt_sex_cds, fmly_nums, st_yyyymm, ed_yyyymm):
        results = db.session.query(cls.in_yyyymm,
                                   db.session.query(LawSidArea.sid_ko_nm).
                                   filter(LawSidArea.sid_cd == cls.in_sid_cd).limit(1).label('in_sid'),
                                   db.session.query(LawSggArea.sgg_ko_nm).
                                   filter(LawSggArea.sgg_cd == cls.in_sgg_cd).limit(1).label('in_sgg'),
                                   db.session.query(LawEmdArea.emd_ko_nm).
                                   filter(LawEmdArea.emd_cd == cls.in_emd_cd).limit(1).label('in_emd'),
                                   db.session.query(LawSidArea.sid_ko_nm).
                                   filter(LawSidArea.sid_cd == cls.out_sid_cd).limit(1).label('out_sid'),
                                   db.session.query(LawSggArea.sgg_ko_nm).
                                   filter(LawSggArea.sgg_cd == cls.out_sgg_cd).limit(1).label('out_sgg'),
                                   db.session.query(LawEmdArea.emd_ko_nm).
                                   filter(LawEmdArea.emd_cd == cls.out_emd_cd).limit(1).label('out_emd'),
                                   db.session.query(Code.name).
                                   filter(and_(Code.code == cls.mv_reasn_cd,
                                               Code.group_code == 'mv_reasn')).limit(1).label('mv_reasn'),
                                   db.session.query(Code.name).
                                   filter(and_(Code.code == cls.aplcnt_clsftn_cd,
                                               Code.group_code == 'aplcnt_clsftn')).limit(1).label('aplcnt_clsftn'),
                                   db.session.query(Code.name).
                                   filter(and_(Code.code == cls.aplcnt_age_cd,
                                               Code.group_code == 'aplcnt_age')).limit(1).label('aplcnt_age'),
                                   db.session.query(Code.name).
                                   filter(and_(Code.code == cls.aplcnt_sex_cd,
                                               Code.group_code == 'aplcnt_sex')).limit(1).label('aplcnt_sex'),
                                   cls.fmly_num). \
            filter(or_(cls.out_sid_cd.in_(out_sid_cds),
                       cls.out_sgg_cd.in_(out_sgg_cds),
                       cls.out_emd_cd.in_(out_emd_cds))). \
            filter(cls.aplcnt_age_cd.in_(aplcnt_age_cds)). \
            filter(cls.aplcnt_sex_cd.in_(aplcnt_sex_cds)). \
            filter(cls.mv_reasn_cd.in_(mv_reasn_cds)). \
            filter(cls.fmly_num.in_(fmly_nums)). \
            filter(or_(cls.in_sid_cd == in_sid_cd,
                       cls.in_sgg_cd == in_sgg_cd,
                       cls.in_emd_cd == in_emd_cd)). \
            filter(and_(cls.in_yyyymm >= st_yyyymm,
                        cls.in_yyyymm <= ed_yyyymm)). \
            order_by(desc(cls.in_yyyymm))

        return results


