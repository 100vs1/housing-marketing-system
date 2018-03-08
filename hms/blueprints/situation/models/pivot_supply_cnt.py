# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import func, and_, or_, desc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea


class PivotSupplyCnt(db.Model):
    """

    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'pivot_supply_cnt'

    id = db.Columnt(db.Integer, primary_key=True)
    sid_cd = db.Columnt(db.String(2))
    sgg_cd = db.Columnt(db.String(5))
    emd_cd = db.Columnt(db.String(10))
    house_sep_ = db.Columnt(db.Integer)
    rank_code = db.Columnt(db.Integer)
    supply_est = db.Columnt(db.Float)
    variable = db.Columnt(db.String(20))
    value = db.Columnt(db.Integer)
    ym201506 = db.Columnt(db.Integer)
    ym201507 = db.Columnt(db.Integer)
    ym201508 = db.Columnt(db.Integer)
    ym201509 = db.Columnt(db.Integer)
    ym201510 = db.Columnt(db.Integer)
    ym201511 = db.Columnt(db.Integer)
    ym201512 = db.Columnt(db.Integer)
    ym201601 = db.Columnt(db.Integer)
    ym201602 = db.Columnt(db.Integer)
    ym201603 = db.Columnt(db.Integer)
    ym201604 = db.Columnt(db.Integer)
    ym201605 = db.Columnt(db.Integer)
    ym201606 = db.Columnt(db.Integer)
    ym201607 = db.Columnt(db.Integer)
    ym201608 = db.Columnt(db.Integer)
    ym201609 = db.Columnt(db.Integer)
    ym201610 = db.Columnt(db.Integer)
    ym201611 = db.Columnt(db.Integer)
    ym201612 = db.Columnt(db.Integer)
    ym201701 = db.Columnt(db.Integer)
    ym201702 = db.Columnt(db.Integer)
    ym201703 = db.Columnt(db.Integer)
    ym201704 = db.Columnt(db.Integer)
    ym201705 = db.Columnt(db.Integer)