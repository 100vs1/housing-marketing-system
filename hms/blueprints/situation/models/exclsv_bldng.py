# -*- coding: utf-8 -*-
from hms.extensions import db


class ExclsvBldng(db.Model):

    """
    건물현황 모델 정의 클래스
    실거래가 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'texclsv_bldng'

    id = db.Column(db.Integer, db.Sequence('exclsv_bldng_id_seq'), primary_key=True)

    sid_cd = db.Column(db.String(2))
    sgg_cd = db.Column(db.String(5))
    emd_cd = db.Column(db.String(10))
    main_num = db.Column(db.Integer)
    sub_num = db.Column(db.Integer)
    prcl_addrs = db.Column(db.String(120))
    road_addrs = db.Column(db.String(120))
    bldng_nm = db.Column(db.String(80))
    block_nm = db.Column(db.String(60))
    floor_num = db.Column(db.Integer)
    bldng_clsftn = db.Column(db.String(20))
    main_strctr = db.Column(db.String(30))
    etc_strctr = db.Column(db.String(160))
    main_use = db.Column(db.String(25))
    etc_use = db.Column(db.String(120))
    exclsv_area = db.Column(db.Double)
    srvy_dt = db.Column(db.String(8))

    def __init__(self, **kwargs):
        super(ExclsvBldng, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        return ExclsvBldng.query. \
            filter(ExclsvBldng.id == identity).first()