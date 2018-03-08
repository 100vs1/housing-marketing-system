# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import or_, and_, asc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class PivotBusinsSitutn(db.Model):
    """
    업종현황 모델 정의 클래스
    지역현황 > 업종현황 메뉴에서 사용하며
    Summary Table 정보를 보여주기 위하여 사용한다.
    """

    __bind__ = 'gisdb'
    __tablename__ = "pivot_busins_situtn"

    sid_cd = db.Column(db.String(2), primary_key=True, nullable=False)
    sgg_cd = db.Column(db.String(5), primary_key=True, nullable=False)
    emd_cd = db.Column(db.String(10), primary_key=True, nullable=False)
    busins_wide_cd = db.Column(db.String(2))
    busins_narrow_cd = db.Column(db.String(4))
    busins_cnt = db.Column(db.Integer)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PivotBusinsSitutn, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_grid(cls, sid_cd, sgg_cd, emd_cd, busins_wide_cds, busins_narrow_cds):

        busins_wide_cd = db.session.query(Code.name). \
            filter(and_(Code.code == cls.busins_wide_cd, Code.group_code == 'busins_wide_cd')).limit(1).label('busins_wide_cd')

        busins_narrow_cd = db.session.query(Code.name). \
            filter(and_(Code.code == cls.busins_narrow_cd, Code.group_code == 'busins_narr_cd')).limit(1).label(
            'busins_narrow_cd')

        items = db.session.query(
            db.session.query(LawSidArea.sid_ko_nm).filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
            db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd'),
            busins_wide_cd,
            busins_narrow_cd,
            cls.busins_cnt). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)). \
            filter(cls.busins_narrow_cd.in_(busins_narrow_cds))

        return items
