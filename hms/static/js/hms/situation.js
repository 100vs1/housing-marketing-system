document.write("<sciprt src=\"{{ url_for('static', filename='scripts/config_0.0.22.js') }}\"></sciprt>");
document.write("<sciprt src='https://openlayers.org/en/v4.2.0/build/ol.js'></sciprt>");

class HmsSituationMap {
    codeStyle = "";
    layer = "";
    layerName = "";

    getCodeStyle() {
        return this.codeStyle;
    }

    setCodeStyle(codeStyle) {
        this.codeStyle = codeStyle;
    }

    getLayer() {
        return this.layer;
    }

    setLayer(layer) {
        this.layer = layer;
    }

    getLayerName() {
        return this.layerName;
    }

    setLayerName(layerName) {
        this.layerName = layerName;
    }

    srchMapResult(codeStyle) {
        if(this.detectAreaStatus()) {

        } else {
            this.setCodeStyle(codeStyle)
        }
    }

    resetMapLayer(map, targetLayer) {
        map.removeLayer("")
    }

    detectAreaStatus(codeStyle) {
        // TODO : 두가지 지역 선택 케이스 확인
        // let areaText = document.getElementById(`spn-${FUNC[codeStyle.toUpperCase()].CODE_STYLE_SHORT}-area`);
        let areaText = document.getElementById(`spn-${FUNC[codeStyle.toUpperCase()].CODE_STYLE_SHORT}-area`);

        return $(areaText).text() !== "";
    }
}