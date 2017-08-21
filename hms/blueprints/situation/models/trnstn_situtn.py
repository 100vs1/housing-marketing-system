# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import func, and_, or_, desc, cast, DATE
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import LawSidArea, LawSggArea, LawEmdArea
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
    house_clsftn_cd = db.Column(db.String(20), nullable=False) # 가구구분코드
    cnstrtn_year = db.Column(db.String(4)) # 건축년도(yyyy)
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

    # @classmethod
    # def find_by_identity(cls, identity):
    #
    #     return TrnstnSitutn.query. \
    #         filter(TrnstnSitutn.id == identity).first()


    @classmethod
    def find_by_filter_for_map(cls, sid_cd, sgg_cd, emd_cd, trnstn_clsftn_cd, house_clsftn_cd,
                                st_sale_price, ed_sale_price, st_deposit, ed_deposit,
                                st_mnthly_rent, ed_mnthly_rent, st_exclsv_area, ed_exclsv_area,
                                st_decrepit, ed_decrepit, st_yyyymm, ed_yyyymm):
        # 서브 쿼리
        # geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawSidArea.geom)).label('geojson')). \
        #     filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('geojson')



        # now_year = db.session.query(func. func.extract('year', func.now()));
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++");
        # print(now_year);
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++");

        # if sid_cd is not None:
        #     local_name = db.session.query(LawSidArea.sid_ko_nm).\
        #         filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('local_name')
        # elif sgg_cd is not None:
        #     local_name = db.session.query(LawSggArea.sgg_ko_nm). \
        #         filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('local_name')
        # else:
        #     local_name = db.session.query(LawEmdArea.emd_ko_nm). \
        #         filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('local_name')
        # local_name,

        results = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(cls.geom)).label('geojsonForBuild'),
                                   cls.id.label('id')). \
            filter(or_(cls.sid_cd == sid_cd,
                   cls.sgg_cd == sgg_cd,
                   cls.emd_cd == emd_cd)). \
            filter(cls.trnstn_clsftn_cd == trnstn_clsftn_cd). \
            filter(cls.house_clsftn_cd == house_clsftn_cd). \
            filter(or_(and_(cls.sale_price >= func.cast(st_sale_price, int),
                            cls.sale_price <= func.cast(ed_sale_price, int))),
                      (and_(cls.deposit >= func.cast(st_deposit, int),
                            cls.deposit <= func.cast(ed_deposit, int))),
                      (and_(cls.mnthly_rent >= func.cast(st_mnthly_rent, int),
                            cls.mnthly_rent <= func.cast(ed_mnthly_rent, int)))). \
            filter(and_(cls.exclsv_area >= st_exclsv_area,
                        cls.exclsv_area <= ed_exclsv_area)). \
            group_by(cls.geom, cls.id)
            # filter(and_(func.cast(now_year, int) - func.cast(cls.cnstrtn_year, int) >= st_decrepit,
            #             func.cast(now_year, int) - func.cast(cls.cnstrtn_yeadr, int) <= ed_decrepit)). \
            # filter(and_(cls.trnstn_yyyymm >= st_yyyymm,
            #             cls.trnstn_yyyymm <= ed_yyyymm)). \
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++");
        print(results);
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++");
        return results

    # @classmethod
    # def find_by_filter_for_grid(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm,
    #                                               ed_yyyymm):
    #     results = db.session.query(cls.srvy_yyyymm,
    #                                db.session.query(LawSidArea.sid_ko_nm).
    #                                filter(LawSidArea.sid_cd == cls.sid_cd).limit(1).label('sid'),
    #                                db.session.query(LawSggArea.sgg_ko_nm).
    #                                filter(LawSggArea.sgg_cd == cls.sgg_cd).limit(1).label('sgg'),
    #                                db.session.query(LawEmdArea.emd_ko_nm).
    #                                filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('emd'),
    #                                db.session.query(Code.name).
    #                                filter(and_(Code.code == cls.age_grp_cd,
    #                                            Code.group_code == 'age_grp')).limit(1).label('age_grp'),
    #                                cls.man_num,
    #                                cls.woman_num,
    #                                cls.total_num). \
    #         filter(or_(cls.sid_cd == sid_cd,
    #                    cls.sgg_cd == sgg_cd,
    #                    cls.emd_cd == emd_cd)). \
    #         filter(cls.age_grp_cd.in_(age_grp_cds)). \
    #         filter(and_(cls.srvy_yyyymm >= st_yyyymm,
    #                     cls.srvy_yyyymm <= ed_yyyymm)). \
    #         order_by(desc(cls.srvy_yyyymm))
    #
    #     return results