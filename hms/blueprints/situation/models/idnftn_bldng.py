# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import func, and_, or_, desc
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea

class IdnftnBldng(db.Model):
    """
    건물현황 모델 정의 클래스
    건물현황 메뉴에서 사용하며
    해마다 대량으로 적재를 하기 때문에
    DB에서는 연 단위로 테이블 파티셔닝하여 사용한다.
    """
    __bind_key__ = 'gisdb'
    __table_name__ = 'idnftn_bldng'     # 건물현황

    id = db.Column(db.Integer, primary_key=True)    # 시퀀스 아이디

    sid_cd = db.Column(db.String(2), nullable=True)         # 시도코드
    sgg_cd = db.Column(db.String(5), nullable=True)         # 시군구코드
    emd_cd = db.Column(db.String(10), nullable=True)        # 읍면동코드
    main_num = db.Column(db.Integer, nullable=True)         # 본번
    sub_num = db.Column(db.Integer, nullable=True)          # 부번
    prcl_addrs = db.Column(db.String(120), nullable=True)   # 지번주소
    road_addrs = db.Column(db.String(120), nullable=False)  # 도로명주소
    bldng_nm = db.Column(db.String(80), nullable=False)     # 건축물명
    block_nm = db.Column(db.String(60), nullable=False)     # 동명
    bldng_clsftn = db.Column(db.String(20), nullable=False) # 건축물분류
    land_area = db.Column(db.Float, nullable=False)         # 대지면적
    bldng_area = db.Column(db.Float, nullable=False)        # 건축면적
    bldng_covrg_rto = db.Column(db.Float, nullable=False)   # 건폐율
    exclsv_area = db.Column(db.Float, nullable=False)       # 연면적(전용면적)
    floor_exclsv_area = db.Column(db.Float, nullable=False) # 용적률산정연면적
    floor_area_rto = db.Column(db.Float, nullable=False)    # 용적률
    main_strctr = db.Column(db.String(30), nullable=False)  # 주요구조
    etc_strctr = db.Column(db.String(160), nullable=False)  # 기타구조
    main_use = db.Column(db.String(25), nullable=False)     # 주요용도
    etc_use = db.Column(db.String(150), nullable=False)     # 기타용도
    main_roof = db.Column(db.String(30), nullable=False)    # 주요지붕
    etc_roof = db.Column(db.String(250), nullable=False)    # 기타지붕
    fmly_num = db.Column(db.Integer, nullable=False)        # 세대수
    house_num = db.Column(db.Integer, nullable=False)       # 가구수
    bldng_height = db.Column(db.Integer, nullable=False)    # 건물높이
    grnd_floor_num = db.Column(db.Integer, nullable=False)  # 지상층수
    bsmt_floor_num = db.Column(db.Integer, nullable=False)  # 지하층수
    elevtr_num = db.Column(db.Integer, nullable=False)      # 승강기수
    emrg_elevtr_num = db.Column(db.Integer, nullable=False) # 비상용승강기수
    sub_bldng_num = db.Column(db.Integer, nullable=False)   # 부속건축물수
    total_block_area = db.Column(db.Float, nullable=False)  # 총동연면적
    indr_mecha_num = db.Column(db.Integer, nullable=False)  # 옥내기계식대수
    outdr_mecha_num = db.Column(db.Integer, nullable=False) # 옥외기계식대수
    indr_self_num = db.Column(db.Integer, nullable=False)   # 옥내자주식대수
    outdr_self_num = db.Column(db.Integer, nullable=False)  # 옥외자주식대수
    cnstrtn_permsn_dt = db.Column(db.String(8), nullable=False) # 건축허가년월일(yyyymmdd)
    begin_cnstrtn_dt = db.Column(db.String(8), nullable=False)  # 착공년월일(yyyymmdd)
    use_permsn_dt = db.Column(db.String(8), nullable=False)     # 사용승인년월일(yyyymmdd)
    permsn_year = db.Column(db.String(4), nullable=False)       # 허가연도
    total_house_num = db.Column(db.Integer, nullable=False)     # 총호수
    enrgy_efcncy_grade = db.Column(db.String(5), nullable=False)# 에너지효율등급
    enrgy_savng_rate = db.Column(db.Float, nullable=False)      # 에너지절감률
    epi_score = db.Column(db.Integer, nullable=False)           # 에너지성능지표점수
    eco_bldng_grade = db.Column(db.String(5), nullable=False)   # 친환경건축물등급
    eco_bldng_crtscr = db.Column(db.Integer, nullable=False)    # 친환경건축물인증점수
    int_bldng_grade = db.Column(db.String(5), nullable=False)   # 지능형건축물등급
    int_bldng_crtscr = db.Column(db.Integer, nullable=False)    # 지능형건축물인증점수
    srvy_dt = db.Column(db.String(8), nullable=True)            # 조사년월일(yyyymmdd)

    def __init__(self, **kwargs):
        super(IdnftnBldng, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_map(cls):
        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawSidArea.geom)).label('geojson')). \
            filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('geojson')