# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime

import pytz
from geoalchemy2.types import Geometry
from sqlalchemy import func, distinct, asc
from sqlalchemy.dialects import postgresql

from lib.util_sqlalchemy import ResourceMixin
import uuid

from hms.extensions import db


class UserMarkers(ResourceMixin, db.Model):
    """
    유저 마커 정의 클래스
    유저 마커 데이터 저장을 위해 사용하며
    파티셔닝이 고려되어야 하나 아직은 하지 않음
    """

    # __bind_key__ = 'gisdb'
    __tablename__ = 'marker'   # 유저 마커

    idx = db.Column(db.String, db.Sequence('markers_pkey'), primary_key=True)

    user_id = db.Column(db.Integer)
    category = db.Column(db.String(25))
    title = db.Column(db.String(50))
    content = db.Column(db.String(200))
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Seoul')))
    updated_on = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Seoul')))
    img_name = db.Column(db.String)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(UserMarkers, self).__init__(**kwargs)

    @classmethod
    def find_not_replication_categorys(cls, user_id):
        results = db.session.query(
            distinct(cls.category).label('category')).\
            filter(cls.user_id == user_id).order_by(asc(cls.category))

        return results

    @classmethod
    def find_by_category(cls, user_id, categorys):
        results = db.session.query(
            cls.idx,
            cls.category,
            cls.title,
            cls.content,
            func.ST_AsGeoJSON(cls.geom).label('geom'),
            cls.img_name). \
            filter(cls.user_id == user_id). \
            filter(cls.category.in_(categorys)).order_by(asc(cls.category))

        print(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        return results

    @classmethod
    def insert_data(cls, user_id, category, title, content, latitude, longitude, img_name):
        geom = func.ST_SetSRID(func.ST_Point(latitude, longitude), '4326').label('geom')

        obj = UserMarkers()
        print(obj)

        obj.idx = obj.get_uuid()
        obj.user_id = user_id
        obj.category = category
        obj.title = title
        obj.content = content
        obj.geom = geom
        obj.img_name = img_name

        obj.save()

    @classmethod
    def update_data(cls, idx, category, title, content):
        obj = UserMarkers.query.get(idx)

        obj.category = category
        obj.title = title
        obj.content = content
        obj.updated_on = datetime.datetime.now(pytz.timezone('Asia/Seoul'))

        obj.save()

    @classmethod
    def delete_data(cls, idx):
        obj = UserMarkers.query.get(idx)
        obj.delete()

    @classmethod
    def get_uuid(cls):
        return uuid.uuid4()
