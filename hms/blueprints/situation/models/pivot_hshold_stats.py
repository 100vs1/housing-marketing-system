# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import or_, and_, asc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea


class PivotHsholdStats(db.Model):
    """
    인구주택총조사 모델 정의 클래스
    지역현황 > 인구주택총조사 메뉴에서 사용하며
    Summary Table 정보를 보여주기 위하여 사용한다.
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'pivot_hshold_stats'

    sid_cd = db.Column(db.String(2), primary_key=True, nullable=False)
    sgg_cd = db.Column(db.String(5), primary_key=True,  nullable=False)
    rsdnc_clsftn_cd = db.Column(db.String(1), primary_key=True, nullable=False)
    fmly_num_cd = db.Column(db.String(1), primary_key=True, nullable=False)
    room_num_cd = db.Column(db.String(1), primary_key=True, nullable=False)
    y2000 = db.Column(db.Integer)
    y2005 = db.Column(db.Integer)
    y2010 = db.Column(db.Integer)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PivotHsholdStats, self).__init__(**kwargs)
