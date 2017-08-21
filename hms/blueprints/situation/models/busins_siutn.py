# -*- coding: utf-8 -*-
from geoalchemy2.types import Geometry
from hms.extensions import db


class BusinsSiutn(db.Model):
    """
    업종현황 모델 정의 클래스
    업종현황 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'busins_siutn'

    id = db.Column(db.Integer, db.Sequence('busins_situtn_id_seq'), primary_key=True)

    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    sid_cd = db.Column(db.String(2), nullable=False)
    sgg_cd = db.Column(db.String(5), nullable=False)
    emd_cd = db.Column(db.String(10), nullable=False)
    lcnsng_dt = db.Column(db.String(8), nullable=False)
    busins_clsftn_cd = db.Column(db.String(20), nullable=False)
    busins_condtn = db.Column(db.String(20))
    loctn_area = db.Column(db.Double)
    compny_nm = db.Column(db.String(60), nullable=False)
    prcl_zipcd = db.Column(db.String(6))
    road_zipcd = db.Column(db.String(7))
    prcl_addrs = db.Column(db.String(120))
    road_addrs = db.Column(db.String(120))
    loctn_phone = db.Column(db.String(35))

    def __init__(self, **kwargs):
        super(BusinsSiutn, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        return  BusinsSiutn.query. \
            filter(BusinsSiutn.id == identity).first()