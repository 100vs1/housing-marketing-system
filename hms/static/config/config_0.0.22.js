FUNC = {
    POPLTN_STATS: {
        KOR_NAME: "인구통계",
        CODE_STYLE: "popltn_stats",
        CODE_STYLE_SHORT: "ps",
        DISPLAY_ORDER: 0,
        LOCATION_TYPE: "adm",
        PERIOD_STANDARD: "month",
        TIME_START: 201001,
        TIME_END: 201801,
        TIME_STEP: 1,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "행정안정부",
    },
    HSHOLD_STATS: {
        KOR_NAME: "인구주택총조사",
        CODE_STYLE: "hshold_stats",
        DISPLAY_ORDER: 1,
        CODE_STYLE_SHORT: "hs",
        LOCATION_TYPE: "law",
        PERIOD_STANDARD: "year",
        TIME_START: 2000,
        TIME_END: 2010,
        TIME_STEP: 5,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "행정자치부",
    },
    POPLTN_MVMT: {
        KOR_NAME: "인구이동",
        CODE_STYLE: "popltn_mvmt",
        CODE_STYLE_SHORT: "pm",
        DISPLAY_ORDER: 2,
        LOCATION_TYPE: "adm",
        PERIOD_STANDARD: "month",
        TIME_START: 201001,
        TIME_END: 201612,
        TIME_STEP: 1,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "통계청",
    },
    TRNSTN_SITUTN_TRANS: {
        KOR_NAME: "수요분석 - 거래량",
        CODE_STYLE: "trnstn_situtn_trans",
        CODE_STYLE_SHORT: "tst",
        DISPLAY_ORDER: 3,
        LOCATION_TYPE: "law",
        PERIOD_STANDARD: "month",
        TIME_START: 201101,
        TIME_END: 201801,
        TIME_STEP: 1,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "국토교통부",
    },
    TRNSTN_SITUTN_PRICE: {
        KOR_NAME: "수요분석 - 가격",
        CODE_STYLE: "trnstn_situtn_price",
        CODE_STYLE_SHORT: "tsp",
        DISPLAY_ORDER: 4,
        LOCATION_TYPE: "law",
        PERIOD_STANDARD: "month",
        TIME_START: 201101,
        TIME_END: 201801,
        TIME_STEP: 1,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "국토교통부",
    },
    IDNFTN_BLDNG: {
        KOR_NAME: "입주물량",
        CODE_STYLE: "idnftn_bldng",
        CODE_STYLE_SHORT: "ib",
        DISPLAY_ORDER: 5,
        LOCATION_TYPE: "law",
        PERIOD_STANDARD: "month",
        TIME_START: 200001,
        TIME_END: 201801,
        TIME_STEP: 1,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "세움터",
    },
    BUSINS_SITUTN: {
        KOR_NAME: "자영업현황",
        CODE_STYLE: "busins_situtn",
        CODE_STYLE_SHORT: "bs",
        DISPLAY_ORDER: 6,
        LOCATION_TYPE: "law",
        PERIOD_STANDARD: null,
        TIME_START: null,
        TIME_END: null,
        TIME_STEP: null,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: "hms:busins_situtn",
        DATA_SOURCE: "Ctree 수집 데이터 (2010)",
    },
    HSHOLD_IMGRAT: {
        KOR_NAME: "세대통계",
        CODE_STYLE: "hshold_imgrat",
        CODE_STYLE_SHORT: "hi",
        DISPLAY_ORDER: 7,
        LOCATION_TYPE: "adm",
        PERIOD_STANDARD: "month",
        TIME_START: 201312,
        TIME_END: 201708,
        TIME_STEP: 1,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "통계청",
    },
    SUPPLY_PRESENT: {
        KOR_NAME: "분양현황",
        CODE_STYLE: "supply_present",
        CODE_STYLE_SHORT: "sp",
        DISPLAY_ORDER: 8,
        LOCATION_TYPE: "law",
        PERIOD_STANDARD: "month",
        TIME_START: 201506,
        TIME_END: 201705,
        TIME_STEP: 1,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "APT2you",
    },
    INCOME_SITUTN: {
        KOR_NAME: "소득현황",
        CODE_STYLE: "income_situtn",
        CODE_STYLE_SHORT: "is",
        DISPLAY_ORDER: 9,
        LOCATION_TYPE: "law",
        PERIOD_STANDARD: null,
        TIME_START: null,
        TIME_END: null,
        TIME_STEP: null,
        MAP_LAYER: undefined,
        MAP_LAYER_NAME_FOR_GEO: [],
        DATA_SOURCE: "Ctree 수집 데이터 (2016.05)",
    }
};

FUNC_SHORT = {
    ps:FUNC.POPLTN_STATS,
    hs:FUNC.HSHOLD_STATS,
    pm:FUNC.POPLTN_MVMT,
    tst:FUNC.TRNSTN_SITUTN_TRANS,
    tsp:FUNC.TRNSTN_SITUTN_PRICE,
    ib:FUNC.IDNFTN_BLDNG,
    bs:FUNC.BUSINS_SITUTN,
    hi:FUNC.HSHOLD_IMGRAT,
    sp:FUNC.SUPPLY_PRESENT,
    is:FUNC.INCOME_SITUTN,
};

DEFAULT_FUNC = FUNC.POPLTN_STATS;

ZOOM = {
    BOUNCE_AFTER: {
        SID: 11,
        SGG: 13,
        EMD: 15
    }
};

BASE_MAP = {
    CENTER: [126.98892500157243, 37.51901189108098],
    ZOOM: 11,
    MIN_ZOOM: 7,
    MAX_ZOOM: 20,
    PROJECTION: "EPSG:4326"
};

// 레이어 별 zIndex
LAYER_ZINDEX = {
    BASE_MAP: 10,            // 기본 지도
    SATELLITE_MAP: 11,       // 위성 지도
    GRAY_MAP: 12,            // 흑백 지도
    MIDNIGHT_MAP: 13,        // 야간 지도

    JIJEOCK_MAP: 20,         // 지적도
    USEPLAN_MAP: 21,         // 토지이용계획도
    HYBRID_MAP: 22,          // 하이브리드 지도

    AREA_HL_MAP: 30,         // 지역 폴리곤 마스크
    AREA_DT_MAP: 31,         // 지역 구분 마스크

    HEAT_MAP: 40,            // 히트맵
    BUBBLE_MAP: 41,          // 버블맵
    RESULT_MAP: 42,          // 맵 결과

    GET_MARKER: 50,         // 마커 보기
    GET_BULK_MARKER: 50,    // 마커 보기-사용자 데이터 정의
    SET_MARKER: 51,         // 마커 그리기

    SET_CIRCLE: 60,         // 버퍼 그리기
    SET_SQUARE: 60,         // 사각형 그리기
    SET_POLYGON: 60,         // 폴리곤 그리기

    TOP: 100                // 최상위,
};

MAP = {
    BASIC_MAP: {
        NAME: "기본 지도",
        ZINDEX: LAYER_ZINDEX.BASE_MAP,
        TYPE: "base"
    },
    SATELLITE_MAP: {
        NAME: "위성 지도",
        ZINDEX: LAYER_ZINDEX.SATELLITE_MAP,
        TYPE: "base"
    },
    GRAY_MAP: {
        NAME: "흑백 지도",
        ZINDEX: LAYER_ZINDEX.GRAY_MAP,
        TYPE: "base"
    },
    MIDNIGHT_MAP: {
        NAME: "야간 지도",
        ZINDEX: LAYER_ZINDEX.MIDNIGHT_MAP,
        TYPE: "base"
    },
    JIJEOCK_MAP: {
        NAME: "지적도",
        ZINDEX: LAYER_ZINDEX.JIJEOCK_MAP,
        TYPE: "base"
    },
    USEPLAN_MAP: {
        NAME: "토지 이용 계획도",
        ZINDEX: LAYER_ZINDEX.USEPLAN_MAP,
        TYPE: "base"
    },
    HYBRID_MAP: {
        NAME: "하이브리드 지도",
        ZINDEX: LAYER_ZINDEX.HYBRID_MAP,
        TYPE: "base"
    },
    AREA_HL_MAP: {
        NAME: "지역 폴리곤 마스크",
        ZINDEX: LAYER_ZINDEX.AREA_HL_MAP,
        TYPE: "base"
    },
    AREA_DT_MAP: {
        NAME: "지역 구분 마스크",
        ZINDEX: LAYER_ZINDEX.AREA_DT_MAP,
        TYPE: "base"
    },
    HEAT_MAP: {
        NAME: "히트맵",
        ZINDEX: LAYER_ZINDEX.HEAT_MAP,
        TYPE: "base"
    },
    BUBBLE_MAP: {
        NAME: "버블맵",
        ZINDEX: LAYER_ZINDEX.BUBBLE_MAP,
        TYPE: "base"
    },
    SET_MARKER: {
        NAME: "마커 그리기",
        ZINDEX: LAYER_ZINDEX.SET_MARKER,
        TYPE: "base"
    },
    GET_MARKER: {
        NAME: "마커 보기",
        ZINDEX: LAYER_ZINDEX.GET_MARKER,
        TYPE: "base"
    },
    GET_BULK_MARKER: {
        NAME: '마커 보기-사용자 데이터 정의',
        ZINDEX: LAYER_ZINDEX.GET_BULK_MARKER,
        TYPE: "base"
    },
    SET_CIRCLE: {
        NAME: "원 그리기",
        ZINDEX: LAYER_ZINDEX.SET_CIRCLE,
        TYPE: "base"
    },
    SET_SQUARE: {
        NAME: "사각형 그리기",
        ZINDEX: LAYER_ZINDEX.SET_SQUARE,
        TYPE: "base"
    },
    SET_POLYGON: {
        NAME: "다각형 그리기",
        ZINDEX: LAYER_ZINDEX.SET_POLYGON,
        TYPE: "base"
    },
};

GEO_SERVER_URL = "http://183.111.230.252:8080/geoserver/hms/wms";
VWORLD_API_KEY = "5873A17E-28A2-36A7-A25B-4451ACA7C2DD";
DOMAIN = "www.ct-gis.com";

// GEO_SERVER Layer 목록
GEO_LAYER = {};

COLOR = {
    BUBBLE: {
        MIN_COLOR: 'rgb(204, 204, 204)',
        MAX_COLOR: 'rgb(76, 76, 76)'
    },
    DRAW: {
        FILL: 'rgba(255, 255, 255, 0.3)',
        STROKE: '#a406ff'
    }
};

ETC_UI = {
    BUBBLE: {
        MIN_RADIUS: 25,
        MAX_RADIUS: 120,
        TOTAL_STEP: 20,
    },
};