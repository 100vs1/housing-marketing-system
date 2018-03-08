import datetime

import pytz
from geoalchemy2 import Geometry
from sqlalchemy import func, desc

from hms.extensions import db
from lib.util_sqlalchemy import ResourceMixin
import uuid


class BulkHistory(ResourceMixin, db.Model):

    __tablename__ = 'bulk_history'

    idx = db.Column(db.String, db.Sequence('bulk_history_pkey'), primary_key=True)

    user_id = db.Column(db.Integer)
    file_name = db.Column(db.String())
    total_cnt = db.Column(db.Integer())
    success_cnt = db.Column(db.Integer())
    fail_cnt = db.Column(db.Integer())
    summary_info = db.Column(db.String())
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now(pytz.timezone('Asia/Seoul')))
    updated_on = db.Column(db.DateTime(), default=datetime.datetime.now(pytz.timezone('Asia/Seoul')))

    def __init__(self, **kwargs):
        super(BulkHistory, self).__init__(**kwargs)

    @classmethod
    def find_by_user_id(cls, user_id):
        return db.session.query(cls.file_name,
                                cls.total_cnt,
                                cls.success_cnt,
                                cls.fail_cnt,
                                cls.summary_info,
                                func.to_char(cls.created_on, 'yyyy-mm-dd hh24:mi:ss').label('created_on')
                                ).\
            filter(cls.user_id == user_id).order_by(desc(cls.created_on))

    @classmethod
    def insert_data(cls, history_idx, user_id, file_name, total_cnt, success_cnt, false_cnt):
        obj = BulkHistory()
        obj.idx = history_idx
        obj.user_id = user_id
        obj.file_name = file_name
        obj.total_cnt = total_cnt
        obj.success_cnt = success_cnt
        obj.fail_cnt = false_cnt
        obj.summary_info = 'blank'
        # # obj.created_on = func.now()
        # obj.updated_on = datetime.datetime.now(pytz.timezone('Asia/Seoul'))

        obj.save()

