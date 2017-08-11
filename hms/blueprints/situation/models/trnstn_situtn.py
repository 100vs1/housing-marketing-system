# -*- coding: utf-8 -*-
from geoalchemy2.types import Geometry
from hms.extensions import db


class TrnstnSitutn(db.Model):
    """
    거래현황 모델 정의 클래스
    실거래가 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __tablename__ = 'trnstn_situtn' # 거래현황

    id = db.Column(db.Integer, db.Sequence('trnstn_situtn_id_seq'), primary_key=True) # 시퀀스아이디

    geom = db.Column(Geometry(geometry_type='POINT', srid=4326)) # 지오메트리
    sid_cd = db.Column(db.String(2), nullable=False) # 시도코드
    sgg_cd = db.Column(db.String(5), nullable=False) # 시군구코드
    emd_cd = db.Column(db.String(10), nullable=False) # 읍면동코드
    trnstn_yyyymm = db.Column(db.String(6), nullable=False) # 거래년월(yyyymm)
    trnstn_clsftn_cd = db.Column(db.String(20), nullable=False) # 거래구분코드
    house_clsftn_cd = db.Column(db.String(2), nullable=False) # 가구구분코드
    cnstrtn_year = db.Column(db.String(4)) # 계약연도(yyyy)
    floor_num = db.Column(db.Integer) # 층수
    cntrct_momnt = db.Column(db.String(6)) # 계약기간
    cntrct_area = db.Column(db.Float) # 계약면적
    exclsv_area = db.Column(db.Float) # 전용면적
    land_area = db.Column(db.Float) # 대지면적
    sale_price = db.Column(db.Integer) # 매매가
    deposit = db.Column(db.Integer) # 보증금
    mnthly_rent = db.Column(db.Integer) # 월세
    prcl_addrs = db.Column(db.String(120)) # 지번주소
    road_addrs = db.Column(db.String(120)) # 도로명주소
    bldng_nm = db.Column(db.String(80)) # 건물명
    main_num = db.Column(db.Integer) # 본번
    sub_num =db.Column(db.Integer) # 부번

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(TrnstnSitutn, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):

        return TrnstnSitutn.query. \
            filter(TrnstnSitutn.id == identity).first()
