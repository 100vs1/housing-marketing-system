# -*- coding: utf-8 -*-
from hms.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class CodeGroup(ResourceMixin, db.Model):
    """
    코드 그룹 모델 정의 클래스
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'code_groups'

    code = db.Column(db.String(20), primary_key=True)

    is_use = db.Column(db.Boolean(), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    definition = db.Column(db.String(300))
    created_id = db.Column(db.Integer, nullable=False)
    updated_id = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(CodeGroup, self).__init__(**kwargs)


class Code(ResourceMixin, db.Model):
    """
    코드 모델 정의 클래스
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'codes'

    code = db.Column(db.String(20), primary_key=True)
    group_code = db.Column(db.String(20), db.ForeignKey('code_groups.code'),
                           primary_key=True, index=True)

    is_use = db.Column(db.Boolean(), nullable=False, server_default='1')
    is_display = db.Column(db.Boolean(), nullable=False, server_default='1')
    display_order = db.Column(db.Integer, nullable=False, server_default='0')
    name = db.Column(db.String(30), nullable=False)
    definition = db.Column(db.String(300))
    created_id = db.Column(db.Integer, nullable=False)
    updated_id = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Code, self).__init__(**kwargs)

    @classmethod
    def find_by_group_code(cls, group_code):
        # 그룹코드로 가용한 코드 목록을 조회한다.
        codes = cls.query.join(CodeGroup). \
            filter(cls.group_code == group_code). \
            filter(CodeGroup.is_use == True). \
            filter(cls.is_use == True). \
            filter(cls.is_display == True). \
            order_by(cls.display_order).all()

        return codes
