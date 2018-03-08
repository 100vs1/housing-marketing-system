# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import or_, and_, asc, func
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class PivotPopltnMvmt(db.Model):
    """
    인구통계 모델 정의 클래스
    지역현황 > 인구주택총조사 메뉴에서 사용하며
    Summary Table 정보를 보여주기 위하여 사용한다.
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'pivot_popltn_mvmt'

    sid_cd = db.Column(db.String(2), primary_key=True, nullable=False)
    sgg_cd = db.Column(db.String(5), primary_key=True, nullable=False)
    emd_cd = db.Column(db.String(10), primary_key=True, nullable=False)
    age_grp_cd = db.Column(db.String(3))
    ym200201 = db.Column(db.Integer)
    ym200202 = db.Column(db.Integer)
    ym200203 = db.Column(db.Integer)
    ym200204 = db.Column(db.Integer)
    ym200205 = db.Column(db.Integer)
    ym200206 = db.Column(db.Integer)
    ym200207 = db.Column(db.Integer)
    ym200208 = db.Column(db.Integer)
    ym200209 = db.Column(db.Integer)
    ym200210 = db.Column(db.Integer)
    ym200211 = db.Column(db.Integer)
    ym200212 = db.Column(db.Integer)


    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PivotPopltnMvmt, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_grid(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds):
        age_grp = db.session.query(Code.name).\
            filter(and_(Code.code == cls.age_grp_cd, Code.group_code == 'age_grp')).limit(1).label('age_grp')

        items = db.session.query(
            db.session.query(LawSidArea.sid_ko_nm).filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
            db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd'),
            age_grp,
            cls.ym200201,
            cls.ym200202,
            cls.ym200203,
            cls.ym200204,
            cls.ym200205,
            cls.ym200206,
            cls.ym200207,
            cls.ym200208,
            cls.ym200209,
            cls.ym200210,
            cls.ym200211,
            cls.ym200212). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            filter(cls.age_grp_cd.in_(age_grp_cds)).\
            order_by(asc(cls.age_grp_cd))

        return items

    @classmethod
    def find_by_filter_for_chart(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds):
        age_grp = db.session.query(Code.name).\
            filter(and_(Code.code == cls.age_grp_cd, Code.group_code == 'age_grp')).limit(1).label('age_grp')

        items = db.session.query(
            db.session.query(LawSidArea.sid_ko_nm).filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
            db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd'),
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