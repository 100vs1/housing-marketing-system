# -- coding: utf-8 --
import datetime

import pytz
from geoalchemy2 import Geometry
from sqlalchemy import func, distinct

from hms.extensions import db
from lib.util_sqlalchemy import ResourceMixin
import uuid


class BulkMarker(ResourceMixin, db.Model):

    __tablename__ = 'bulk_marker'

    idx = db.Column(db.String, db.Sequence('bulk_marker_pkey'), primary_key=True)

    user_id = db.Column(db.Integer)
    history_idx = db.Column(db.String)
    category = db.Column(db.String(25))
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))
    address = db.Column(db.String(80))
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    number1 = db.Column(db.Integer)
    number2 = db.Column(db.Integer)
    number3 = db.Column(db.Integer)
    number4 = db.Column(db.Integer)
    number5 = db.Column(db.Integer)
    string1 = db.Column(db.String(100))
    string2 = db.Column(db.String(100))
    string3 = db.Column(db.String(100))
    string4 = db.Column(db.String(100))
    string5 = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Seoul')))
    updated_on = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Seoul')))
    img_name = db.Column(db.String)

    def __init__(self, **kwargs):
        super(BulkMarker, self).__init__(**kwargs)

    @classmethod
    def find_by_user_id(cls, user_id):
        result = db.session.query(
            cls.user_id,
            cls.category,
            cls.title,
            cls.content,
            cls.address,
            func.ST_AsGeoJSON(cls.geom).label('geom'),
            cls.number1,
            cls.number2,
            cls.number3,
            cls.number4,
            cls.number5,
            cls.string1,
            cls.string2,
            cls.string3,
            cls.string4,
            cls.string5,
            cls.created_on,
            cls.updated_on,
            cls.img_name
        ).filter(cls.user_id == user_id)

        return result

    @classmethod
    def find_not_replication_categorys(cls, user_id):
        result = db.session.query(
            distinct(cls.category).label('category')
        ).filter(cls.user_id == user_id)

        return result

    @classmethod
    def find_by_categorys(cls, user_id, categorys):
        results = db.session.query(
            cls.idx,
            cls.user_id,
            cls.category,
            cls.title,
            cls.content,
            cls.address,
            func.ST_AsGeoJSON(cls.geom).label('geom'),
            cls.number1,
            cls.number2,
            cls.number3,
            cls.number4,
            cls.number5,
            cls.string1,
            cls.string2,
            cls.string3,
            cls.string4,
            cls.string5,
            cls.created_on,
            cls.updated_on,
            cls.img_name).\
            filter(cls.user_id == user_id).\
            filter(cls.category.in_(categorys))

        return results

    @classmethod
    def insert_data(cls, user_id, history_idx, category, title, content, address, lon, lat,
                    number1, number2, number3, number4, number5,
                    string1, string2, string3, string4, string5,
                    img_name):
        img_name = 'Ctree_1-02.png'

        geom = func.ST_SetSRID(func.ST_Point(lat, lon), '4326').label('geom')
        print(address)
        obj = BulkMarker()
        obj.idx = uuid.uuid4()
        obj.user_id = user_id
        obj.history_idx = history_idx
        obj.category = category
        obj.title = title
        obj.content = content
        obj.address = address
        obj.geom = geom
        obj.number1 = number1
        obj.number2 = number2
        obj.number3 = number3
        obj.number4 = number4
        obj.number5 = number5
        obj.string1 = string1
        obj.string2 = string2
        obj.string3 = string3
        obj.string4 = string4
        obj.string5 = string5
        obj.img_name = img_name

        obj.save()
