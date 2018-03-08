# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import or_, and_, asc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class PivotHsholdImgrat(db.Model):
    """
    인구통계 모델 정의 클래스
    지역현황 > 인구주택총조사 메뉴에서 사용하며
    Summary Table 정보를 보여주기 위하여 사용한다.
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'pivot_hshold_imgrat'

    sid_cd = db.Column(db.String(), primary_key=True)
    sgg_cd = db.Column(db.String(), primary_key=True)
    emd_cd = db.Column(db.String(), primary_key=True)
    hshold_num_cd = db.Column(db.String(2), primary_key=True)

    ym201312 = db.Column(db.Integer)
    ym201401 = db.Column(db.Integer)
    ym201402 = db.Column(db.Integer)
    ym201403 = db.Column(db.Integer)
    ym201404 = db.Column(db.Integer)
    ym201405 = db.Column(db.Integer)
    ym201406 = db.Column(db.Integer)
    ym201407 = db.Column(db.Integer)
    ym201408 = db.Column(db.Integer)
    ym201409 = db.Column(db.Integer)
    ym201410 = db.Column(db.Integer)
    ym201411 = db.Column(db.Integer)
    ym201412 = db.Column(db.Integer)
    ym201501 = db.Column(db.Integer)
    ym201502 = db.Column(db.Integer)
    ym201503 = db.Column(db.Integer)
    ym201504 = db.Column(db.Integer)
    ym201505 = db.Column(db.Integer)
    ym201506 = db.Column(db.Integer)
    ym201507 = db.Column(db.Integer)
    ym201508 = db.Column(db.Integer)
    ym201509 = db.Column(db.Integer)
    ym201510 = db.Column(db.Integer)
    ym201511 = db.Column(db.Integer)
    ym201512 = db.Column(db.Integer)
    ym201601 = db.Column(db.Integer)
    ym201602 = db.Column(db.Integer)
    ym201603 = db.Column(db.Integer)
    ym201604 = db.Column(db.Integer)
    ym201605 = db.Column(db.Integer)
    ym201606 = db.Column(db.Integer)
    ym201607 = db.Column(db.Integer)
    ym201608 = db.Column(db.Integer)
    ym201609 = db.Column(db.Integer)
    ym201610 = db.Column(db.Integer)
    ym201611 = db.Column(db.Integer)
    ym201612 = db.Column(db.Integer)
    ym201701 = db.Column(db.Integer)
    ym201702 = db.Column(db.Integer)
    ym201703 = db.Column(db.Integer)
    ym201704 = db.Column(db.Integer)
    ym201705 = db.Column(db.Integer)
    ym201706 = db.Column(db.Integer)
    ym201707 = db.Column(db.Integer)
    ym201708 = db.Column(db.Integer)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PivotHsholdImgrat, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_grid(cls, sid_cd, sgg_cd ,emd_cd, hshold_num_cd):
        sid = db.session.query(LawSidArea.sid_ko_nm).filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid')
        sgg = db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg')
        emd = db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd')
        hshold_num = db.session.query(Code.name). \
            filter(and_(Code.code == cls.hshold_num_cd, Code.group_code == 'hshold_num_cd')).limit(1).label('hshold_num')

        items = db.session.query(sid,
                                 sgg,
                                 emd,
                                 hshold_num,
                                 cls.ym201312,
                                 cls.ym201401,
                                 cls.ym201402,
                                 cls.ym201403,
                                 cls.ym201404,
                                 cls.ym201405,
                                 cls.ym201406,
                                 cls.ym201407,
                                 cls.ym201408,
                                 cls.ym201409,
                                 cls.ym201410,
                                 cls.ym201411,
                                 cls.ym201412,
                                 cls.ym201501,
                                 cls.ym201502,
                                 cls.ym201503,
                                 cls.ym201504,
                                 cls.ym201505,
                                 cls.ym201506,
                                 cls.ym201507,
                                 cls.ym201508,
                                 cls.ym201509,
                                 cls.ym201510,
                                 cls.ym201511,
                                 cls.ym201512,
                                 cls.ym201601,
                                 cls.ym201602,
                                 cls.ym201603,
                                 cls.ym201604,
                                 cls.ym201605,
                                 cls.ym201606,
                                 cls.ym201607,
                                 cls.ym201608,
                                 cls.ym201609,
                                 cls.ym201610,
                                 cls.ym201611,
                                 cls.ym201612,
                                 cls.ym201701,
                                 cls.ym201702,
                                 cls.ym201703,
                                 cls.ym201704,
                                 cls.ym201705,
                                 cls.ym201706,
                                 cls.ym201707,
                                 cls.ym201708
                                 ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(cls.hshold_num_cd.in_(hshold_num_cd)).\
            order_by(asc(cls.hshold_num_cd))

        return items