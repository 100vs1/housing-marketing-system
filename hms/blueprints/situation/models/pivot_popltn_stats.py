# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import or_, and_, asc, func
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import AdmSidArea, AdmSggArea, AdmEmdArea


class PivotPopltnStats(db.Model):
    """
    인구통계 모델 정의 클래스
    지역현황 > 인구주택총조사 메뉴에서 사용하며
    Summary Table 정보를 보여주기 위하여 사용한다.
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'pivot_popltn_stats'

    sid_cd = db.Column(db.String(2), primary_key=True, nullable=False)
    sgg_cd = db.Column(db.String(5), primary_key=True, nullable=False)
    emd_cd = db.Column(db.String(10), primary_key=True, nullable=False)
    age_grp_cd = db.Column(db.String(3))
    ym201207 = db.Column(db.Integer)
    ym201208 = db.Column(db.Integer)
    ym201209 = db.Column(db.Integer)
    ym201210 = db.Column(db.Integer)
    ym201211 = db.Column(db.Integer)
    ym201212 = db.Column(db.Integer)
    ym201301 = db.Column(db.Integer)
    ym201302 = db.Column(db.Integer)
    ym201303 = db.Column(db.Integer)
    ym201304 = db.Column(db.Integer)
    ym201305 = db.Column(db.Integer)
    ym201306 = db.Column(db.Integer)
    ym201307 = db.Column(db.Integer)
    ym201308 = db.Column(db.Integer)
    ym201309 = db.Column(db.Integer)
    ym201310 = db.Column(db.Integer)
    ym201311 = db.Column(db.Integer)
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

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PivotPopltnStats, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_grid(cls, sid_cds, sgg_cds, emd_cds, age_grp_cds):
        age_grp = db.session.query(Code.name).\
            filter(and_(Code.code == cls.age_grp_cd, Code.group_code == 'age_grp')).limit(1).label('age_grp')

        items = db.session.query(
            db.session.query(AdmSidArea.sid_ko_nm).filter(AdmSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
            db.session.query(AdmSggArea.sgg_ko_nm).filter(AdmSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
            db.session.query(AdmEmdArea.emd_ko_nm).filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd'),
            age_grp,
            cls.ym201207,
            cls.ym201208,
            cls.ym201209,
            cls.ym201210,
            cls.ym201211,
            cls.ym201212,
            cls.ym201301,
            cls.ym201302,
            cls.ym201303,
            cls.ym201304,
            cls.ym201305,
            cls.ym201306,
            cls.ym201307,
            cls.ym201308,
            cls.ym201309,
            cls.ym201310,
            cls.ym201311,
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
            cls.ym201707). \
            filter(or_(cls.sid_cd.in_(sid_cds) ,
                       cls.sgg_cd.in_(sgg_cds),
                       cls.emd_cd.in_(emd_cds))).\
            filter(cls.age_grp_cd.in_(age_grp_cds)).\
            order_by(asc(cls.age_grp_cd))

        return items

    @classmethod
    def find_by_filter_for_chart(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds):
        age_grp = db.session.query(Code.name).\
            filter(and_(Code.code == cls.age_grp_cd, Code.group_code == 'age_grp')).limit(1).label('age_grp')

        items = db.session.query(
            db.session.query(AdmSidArea.sid_ko_nm).filter(AdmSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
            db.session.query(AdmSggArea.sgg_ko_nm).filter(AdmSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
            db.session.query(AdmEmdArea.emd_ko_nm).filter(AdmEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd'),
            age_grp,
            func.sum(cls.ym201207).label('201207'),
            func.sum(cls.ym201208).label('201208'),
            func.sum(cls.ym201209).label('201209'),
            func.sum(cls.ym201210).label('201210'),
            func.sum(cls.ym201211).label('201211'),
            func.sum(cls.ym201212).label('201212'),
            func.sum(cls.ym201301).label('201301'),
            func.sum(cls.ym201302).label('201302'),
            func.sum(cls.ym201303).label('201303'),
            func.sum(cls.ym201304).label('201304'),
            func.sum(cls.ym201305).label('201305'),
            func.sum(cls.ym201306).label('201306'),
            func.sum(cls.ym201307).label('201307'),
            func.sum(cls.ym201308).label('201308'),
            func.sum(cls.ym201309).label('201309'),
            func.sum(cls.ym201310).label('201310'),
            func.sum(cls.ym201311).label('201311'),
            func.sum(cls.ym201312).label('201312'),
            func.sum(cls.ym201401).label('201401'),
            func.sum(cls.ym201402).label('201402'),
            func.sum(cls.ym201403).label('201403'),
            func.sum(cls.ym201404).label('201404'),
            func.sum(cls.ym201405).label('201405'),
            func.sum(cls.ym201406).label('201406'),
            func.sum(cls.ym201407).label('201407'),
            func.sum(cls.ym201408).label('201408'),
            func.sum(cls.ym201409).label('201409'),
            func.sum(cls.ym201410).label('201410'),
            func.sum(cls.ym201411).label('201411'),
            func.sum(cls.ym201412).label('201412'),
            func.sum(cls.ym201501).label('201501'),
            func.sum(cls.ym201502).label('201502'),
            func.sum(cls.ym201503).label('201503'),
            func.sum(cls.ym201504).label('201504'),
            func.sum(cls.ym201505).label('201505'),
            func.sum(cls.ym201506).label('201506'),
            func.sum(cls.ym201507).label('201507'),
            func.sum(cls.ym201508).label('201508'),
            func.sum(cls.ym201509).label('201509'),
            func.sum(cls.ym201510).label('201510'),
            func.sum(cls.ym201511).label('201511'),
            func.sum(cls.ym201512).label('201512'),
            func.sum(cls.ym201601).label('201601'),
            func.sum(cls.ym201602).label('201602'),
            func.sum(cls.ym201603).label('201603'),
            func.sum(cls.ym201604).label('201604'),
            func.sum(cls.ym201605).label('201605'),
            func.sum(cls.ym201606).label('201606'),
            func.sum(cls.ym201607).label('201607'),
            func.sum(cls.ym201608).label('201608'),
            func.sum(cls.ym201609).label('201609'),
            func.sum(cls.ym201610).label('201610'),
            func.sum(cls.ym201611).label('201611'),
            func.sum(cls.ym201612).label('201612'),
            func.sum(cls.ym201701).label('201701'),
            func.sum(cls.ym201702).label('201702'),
            func.sum(cls.ym201703).label('201703'),
            func.sum(cls.ym201704).label('201704'),
            func.sum(cls.ym201705).label('201705'),
            func.sum(cls.ym201706).label('201706'),
            func.sum(cls.ym201707).label('201706')).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(cls.age_grp_cd.in_(age_grp_cds)).\
            order_by(asc(cls.age_grp_cd))

        return items
