# -*- coding: utf-8 -*-
from __future__ import print_function

from geoalchemy2 import Geometry
from sqlalchemy import func, and_, or_, desc
from hms.extensions import db


class StatsBoardNoori(db.Model):
    """

    """

    __bind_key__ = 'gisdb'
    __table_name__ = 'stats_board_noori'

    id = db.Column(db.BigInteger, primary_key=True)
    parent = db.Column(db.String(10))
    text = db.Column(db.String(30))
    form_id = db.Column(db.Integer)
    style_num = db.Column(db.String)
    target_date = db.Column(db.String)

    def __init__(self, **kwargs):
        super(StatsBoardNoori, self).__init__(**kwargs)

    @classmethod
    def find_all_tree_data(cls):
        result = db.sesssion.query(
            cls.id,
            cls.parent,
            cls.text,
            cls.form_id,
            cls.style_num,
            cls.target_date
        )

        return result
