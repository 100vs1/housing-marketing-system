document.write("<sciprt src=\"{{ url_for('static', filename='scripts/config_0.0.22.js') }}\"></sciprt>");
document.write("<sciprt src='https://openlayers.org/en/v4.2.0/build/ol.js'></sciprt>");

// TODO : 맵에는 크게 두가지 종류가 있음. vworld, geoServer 이거 객체 쪼개서 어떻게 할 방법 강구해보지..
class HmsMap {
    constructor(apiKey, domain) {
        this.apiKey = apiKey;
        this.domain = domain;
    }

    getApiKey() {
        return this.apiKey;
    }

    setApiKey() {
        this.apiKey = apiKey;
    }

    getDomain() {
        return this.domain;
    }

    setDomain() {
        this.domain = domain;
    }

    getBaseMap() {
        return new ol.layer.Tile({
            title: MAP.BASIC_MAP.NAME,
            type: 'base',
            zIndex: MAP.BASIC_MAP.ZINDEX,
            source: new ol.source.XYZ({
                url: 'http://api.vworld.kr/req/wmts/1.0.0/' + this.apiKey + '/Base/{z}/{y}/{x}.png'
            })
        });
    }

    getSatelliteMap() {
        return new ol.layer.Tile({
            title: MAP.SATELLITE_MAP.NAME,
            type: 'base',
            zIndex: MAP.SATELLITE_MAP.ZINDEX,
            source: new ol.source.XYZ({
                url: 'http://api.vworld.kr/req/wmts/1.0.0/' + this.apiKey + '/Satellite/{z}/{y}/{x}.jpeg'
            })
        });
    }

    getGrayMap() {
        return new ol.layer.Tile({
            title: MAP.GRAY_MAP.NAME,
            type: 'base',
            zIndex: MAP.GRAY_MAP.ZINDEX,
            source: new ol.source.XYZ({
                url: 'http://api.vworld.kr/req/wmts/1.0.0/' + this.apiKey + '/gray/{z}/{y}/{x}.png'
            })
        });
    }

    getMidnightMap() {
        return new ol.layer.Tile({
            title: MAP.MIDNIGHT_MAP.NAME,
            type: 'base',
            zIndex: MAP.MIDNIGHT_MAP.ZINDEX,
            source: new ol.source.XYZ({
                url: 'http://api.vworld.kr/req/wmts/1.0.0/' + this.apiKey + '/midnight/{z}/{y}/{x}.png'
            })
        });

    }

    getUserPlanMap() {
        return new ol.layer.Tile({
            title: MAP.USEPLAN_MAP.NAME,
            id: "LT_C_LHBLPN",
            name: "wms_theme", //vmap 올린 레이어를 삭제하거나 수정,변경할때 접근할 name 속성
            projection: "EPSG:900913",
            maxZoom: 18,
            minZoom: 10,
            tilePixelRatio: 1,
            tileSize: [512, 512],
            zIndex: MAP.USEPLAN_MAP.ZINDEX,
            visible: false,
            source: new ol.source.TileWMS({
                url: "http://api.vworld.kr/req/wms?",
                params: {
                    REQUEST: "GetMap",
                    LAYERS: "LT_C_LHBLPN",
                    STYLES: "LT_C_LHBLPN",
                    CRS: "EPSG:900913",
                    apikey: this.apiKey,
                    DOMAIN: "www.local_alphanets.ai",
                    title: MAP.USEPLAN_MAP.NAME,
                    FORMAT: "image/png",
                    WIDTH: 512,
                    HEIGHT: 512
                }
            })
        });
    }

    getJijeockMap() {
        return new ol.layer.Tile({
            title: MAP.JIJEOCK_MAP.NAME,
            id: "LP_PA_CBND_BUBUN,LP_PA_CBND_BONBUN",
            name: "wms_theme", //vmap 올린 레이어를 삭제하거나 수정,변경할때 접근할 name 속성
            projection: "EPSG:900913",
            maxZoom: 18,
            minZoom: 10,
            tilePixelRatio: 1,
            tileSize: [512, 512],
            zIndex: MAP.JIJEOCK_MAP.ZINDEX,
            visible: false,
            source: new ol.source.TileWMS({
                url: "http://api.vworld.kr/req/wms?",
                params: {
                    REQUEST: "GetMap",
                    LAYERS: "LP_PA_CBND_BUBUN,LP_PA_CBND_BONBUN",
                    STYLES: "LP_PA_CBND_BUBUN,LP_PA_CBND_BONBUN",
                    CRS: "EPSG:900913",
                    apikey: this.apiKey,
                    DOMAIN: this.domain,
                    title: MAP.JIJEOCK_MAP.NAME,
                    FORMAT: "image/png",
                    BBOX: "14133818.022824,4520485.8511757,14134123.770937,4520791.5992888",
                    WIDTH: 512,
                    HEIGHT: 512
                }
            })
        })
    }

    getHybridMap() {
        return new ol.layer.Tile({
            title: MAP.HYBRID_MAP.NAME,
            type: 'mapTitle',
            zIndex: MAP.HYBRID_MAP.ZINDEX,
            visible: false,
            source: new ol.source.XYZ({
                url: 'http://api.vworld.kr/req/wmts/1.0.0/' + this.apiKey + '/Hybrid/{z}/{y}/{x}.png'
            })
        });
    }

    getDistAreaMap() {
        return new ol.layer.Image({
            title: MAP.AREA_DT_MAP.NAME,
            zIndex: MAP.AREA_DT_MAP.ZINDEX,
            source: new ol.source.ImageWMS({
                // TODO : GeoServer 쪽 고려해 볼 것
                url: GEO_SERVER_URL,
                serverType: 'geoserver',
                crossOrigin: 'anonymous'
            })
        });
    }

    getInvisibleMap() {
        return new ol.layer.Vector({
            title: MAP.AREA_HL_MAP.NAME,   //스위처 제거
            source: new ol.source.Vector(),
            zIndex: MAP.AREA_HL_MAP.ZINDEX,
            style: new ol.style.Style({
                fill: new ol.style.Fill({
                    color: 'rgba(255, 255, 255, 0)'
                })
            })
        })
    }

    resetSearchResult() {

    }

    resetLayer() {

    }

    resetOverlay() {

    }

    resetController() {

    }
}