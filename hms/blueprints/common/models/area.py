# -*- coding: utf-8 -*-
from geoalchemy2.types import Geometry
import geoalchemy2.functions as func
from hms.extensions import db


class LawSidArea(db.Model):
    """
    법정 시도 구역 모델 정의 클래스
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'law_sid_area'

    sid_cd = db.Column(db.String(2), primary_key=True)

    geom = db.Column(Geometry(geometry_type='MULTYPOLYGON', srid=4326))
    sid_ko_nm = db.Column(db.String(21), nullable=False)
    sid_en_nm = db.Column(db.String(17), nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(LawSidArea, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        return db.session.query(cls.sid_cd,
                                cls.sid_ko_nm,
                                func.ST_AsGeoJSON(func.ST_Centroid(cls.geom)).label('geojson')). \
            filter(cls.sid_cd == identity).first()

    @classmethod
    def find_all(cls):
        return db.session.query(cls.sid_cd,
                                cls.sid_ko_nm,
                                func.ST_AsGeoJSON(func.ST_Centroid(cls.geom)).label('geojson')). \
            order_by(cls.sid_cd.asc()).all()


class LawSggArea(db.Model):
    """
    법정 시군구 구역 모델 정의 클래스
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'law_sgg_area'

    sgg_cd = db.Column(db.String(5), primary_key=True)

    geom = db.Column(Geometry(geometry_type='MULTYPOLYGON', srid=4326))
    sgg_ko_nm = db.Column(db.String(25), nullable=False)
    sgg_en_nm = db.Column(db.String(27), nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(LawSidArea, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        return db.session.query(cls.sgg_cd,
                                cls.sgg_ko_nm,
                                func.ST_AsGeoJSON(func.ST_Centroid(cls.geom)).label('geojson')). \
            filter(cls.sgg_cd == identity).first()

    @classmethod
    def find_by_sid_cd(cls, sid_cd):
        return db.session.query(cls.sgg_cd,
                                cls.sgg_ko_nm,
                                func.ST_AsGeoJSON(func.ST_Centroid(cls.geom)).label('geojson')). \
            filter(cls.sgg_cd.like('{0}%'.format(sid_cd))). \
            order_by(cls.sgg_cd.asc()).all()


class LawEmdArea(db.Model):
    """
    법정 읍면동 구역 모델 정의 클래스
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'law_emd_area'

    emd_cd = db.Column(db.String(10), primary_key=True)

    geom = db.Column(Geometry(geometry_type='MULTYPOLYGON', srid=4326))
    emd_ko_nm = db.Column(db.String(16), nullable=False)
    emd_en_nm = db.Column(db.String(28), nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(LawEmdArea, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        return db.session.query(cls.emd_cd,
                                cls.emd_ko_nm,
                                func.ST_AsGeoJSON(func.ST_Centroid(cls.geom)).label('geojson')). \
            filter(cls.emd_cd == identity).first()

    @classmethod
    def find_by_sgg_cd(cls, sgg_cd):
        return db.session.query(cls.emd_cd,
                                cls.emd_ko_nm,
                                func.ST_AsGeoJSON(func.ST_Centroid(cls.geom)).label('geojson')). \
            filter(cls.emd_cd.like('{0}%'.format(sgg_cd))). \
            order_by(cls.emd_cd.asc()).all()


class AdmSidArea(db.Model):
    """
    행정 시도 구역 모델 정의 클래스
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'adm_sid_area'

    sid_cd = db.Column(db.String(2), primary_key=True)

    geom = db.Column(Geometry(geometry_type='MULTYPOLYGON', srid=4326))
    sid_ko_nm = db.Column(db.String(21), nullable=False)
    sid_en_nm = db.Column(db.String(17), nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(AdmSidArea, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        return cls.query. \
            filter(cls.sid_cd == identity).first()


class AdmSggArea(db.Model):
    """
    행정 시군구 구역 모델 정의 클래스
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'adm_sgg_area'

    sgg_cd = db.Column(db.String(5), primary_key=True)

    geom = db.Column(Geometry(geometry_type='MULTYPOLYGON', srid=4326))
    sgg_ko_nm = db.Column(db.String(25), nullable=False)
    sgg_en_nm = db.Column(db.String(27), nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(AdmSggArea, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        return cls.query. \
            filter(cls.sgg_cd == identity).first()


class AdmEmdArea(db.Model):
    """
    행정 읍면동 구역 모델 정의 클래스
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'adm_emd_area'

    emd_cd = db.Column(db.String(10), primary_key=True)

    geom = db.Column(Geometry(geometry_type='MULTYPOLYGON', srid=4326))
    emd_ko_nm = db.Column(db.String(16), nullable=False)
    emd_en_nm = db.Column(db.String(28), nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(AdmEmdArea, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        return cls.query. \
            filter(cls.emd_cd == identity).first()
