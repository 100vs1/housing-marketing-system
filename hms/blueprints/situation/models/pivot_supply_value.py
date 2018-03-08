# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import func, and_, or_, desc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class PivotSupplyValue(db.Model):
    """

    """

    __bind_key__ = 'gisdb'
    __table_name__ = 'pivot_supply_value'

    sid_cd = db.Column(db.String(2), primary_key=True)
    sgg_cd = db.Column(db.String(5), primary_key=True)
    emd_cd = db.Column(db.String(10), primary_key=True)
    date_in = db.Column(db.String(8), primary_key=True)
    rank_code = db.Column(db.Integer, primary_key=True)
    house_sep = db.Column(db.Integer, primary_key=True)
    supply_area = db.Column(db.Float, primary_key=True)
    variable = db.Column(db.String(), primary_key=True)
    ym201506 = db.Column(db.Float)
    ym201507 = db.Column(db.Float)
    ym201508 = db.Column(db.Float)
    ym201509 = db.Column(db.Float)
    ym201510 = db.Column(db.Float)
    ym201511 = db.Column(db.Float)
    ym201512 = db.Column(db.Float)
    ym201601 = db.Column(db.Float)
    ym201602 = db.Column(db.Float)
    ym201603 = db.Column(db.Float)
    ym201604 = db.Column(db.Float)
    ym201605 = db.Column(db.Float)
    ym201606 = db.Column(db.Float)
    ym201607 = db.Column(db.Float)
    ym201608 = db.Column(db.Float)
    ym201609 = db.Column(db.Float)
    ym201610 = db.Column(db.Float)
    ym201611 = db.Column(db.Float)
    ym201612 = db.Column(db.Float)
    ym201701 = db.Column(db.Float)
    ym201702 = db.Column(db.Float)
    ym201703 = db.Column(db.Float)
    ym201704 = db.Column(db.Float)
    ym201705 = db.Column(db.Float)

    def __init__(self, **kwargs):
        super(PivotSupplyValue, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_grid(cls, sid_cd, sgg_cd, emd_cd):
        result = db.session.query(
            db.session.query(LawSidArea.sid_ko_nm).filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
            db.session.query(LawSggArea.sgg_ko_nm).filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
            db.session.query(LawEmdArea.emd_ko_nm).filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd'),
            cls.sid_cd,
            cls.sgg_cd,
            cls.emd_cd,
            cls.date_in,
            cls.rank_code,
            cls.house_sep,
            cls.supply_area,
            cls.variable,
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
            cls.ym201705). \
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd))

        return result