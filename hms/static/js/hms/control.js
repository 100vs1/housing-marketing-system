document.write("<sciprt src=\"{{ url_for('static', filename='scripts/test_0.2.3.js') }}\"></sciprt>");
document.write("<sciprt src='https://openlayers.org/en/v4.2.0/build/ol.js'></sciprt>");

class HmsControl {
    constructor() {

    }

    // app = window.app();

    static controlConfig(controlName) {
        let controlConfig = {

            fullScreen: {
                icon: "{{ url_for('static', filename='styles/vendor/ol3.css') }}",
                flag: false,
                type: 'default'
            },
            zoomSlider: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'default'
            },
            scaleLine: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'default'
            },
            layerSwitcher: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'default'
            },
            searchAddress: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'hms'
            },
            getMarker: {
                icon: "/static/images/icon/control/getMarker.png",
                flag: false,
                type: 'hms'
            },
            viewMarker: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'hms'
            },
            getBulkMarker: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'hms'
            },
            drawPolygon: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'hms'
            },
            drawSquare: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'hms'
            },
            drawCircle: {
                icon: '{{url_for("situation.search_address")}}',
                flag: false,
                type: 'hms'
            },
        };

        return controlConfig[controlName]
    }

    static getControlIcon(controlName) {
        return HmsControl.controlConfig(controlName)['icon'];
    }

    static getControlFlag(controlName) {
        return HmsControl.controlConfig(controlName)['flag']
    }

    static getControlType(controlName) {
        return HmsControl.controlConfig(controlName)['type']
    }

    //  viewControl(controlName) {
    //
    // }
    //
    //  viewControlAll() {
    //
    // }
    //
    //  hideControl(controlName) {
    //
    // }

    getFullScreenControl() {
        return new ol.control.FullScreen();
    }

    getZoomSliderControl() {
        return new ol.control.ZoomSlider();
    }

    getScaleLineControl() {
        return new ol.control.ScaleLine();
    }

    getLayerSwitcherControl() {
        return new ol.control.LayerSwitcher();
    }

    getOverviewMapControl() {
        return new ol.control.OverviewMap({
            className: 'ol-overviewmap ol-custom-overviewmap',
            layers: layers,
            collapseLabel: '\u00BB',
            label: '\u00AB',
            collapsed: false
        });
    }

    getSearchAddressControl() {

    }

    getGetMarkerControl(opt_options) {
        let options = opt_options || {};

        let controlName = 'getMarker';
        let iconPath = HmsControl.getControlIcon(controlName);

        let button = document.createElement('button');
        button.setAttribute('title', MAP.GET_MARKER.NAME);
        button.innerHTML = `<img src="${iconPath}" width="20px">`;

        let getMarkerAction = function() {
            $('.ctl-marker-view').children().first().css('background-color', 'rgba(0, 0, 0, 0.7)');

            $.ajax({
                method: 'POST',
                url: '/get_categorys',
                dataType: 'json'
            }).done(function (data) {
                let results = [];
                $.each(data.rows, function (i, item) {
                    let category = '';
                    String(item.category) !== '' ? category = item.category : category = '구분 없음';
                    results.push(`<option value="${item.category}">${category}</option>`);
                });
                $('#mdl-viewMarker-sp').html(results.join('')).selectpicker('refresh');
            });

            showModal('mdl-viewMarker-area')
        };

        button.addEventListener('click', getMarkerAction, false);
        button.addEventListener('touchstart', getMarkerAction, false);

        let element = document.createElement('div');
        element.className = 'ctl-marker-view ol-unselectable ol-control';
        element.appendChild(button);

        return new ol.control.Control({
            element: element,
            target: options.target
        });
    }

    getSetMarkerControl() {

    }

    getSetBulkMarkerControl() {

    }

    static drawContorl() {

    }

    getDrawPolygonControl() {

    }

    getDrawSqaureControl() {

    }

    getDrawCircleControl() {

    }


    // 유저 정의 부분
    setMarkerControl() {

    }
}

    $(document).ready(function () {
        $("#jqGrid").jqGrid({
            url: 'data.json',
            mtype: "GET",
            datatype: "json",
            colModel: [
                {label: 'OrderID', name: 'OrderID', key: true, width: 155},
                {label: 'Customer ID', name: 'CustomerID', width: 70},
                {label: 'Order Date', name: 'OrderDate', width: 150},
                {
                    label: 'Freight',
                    name: 'Freight',
                    width: 150,
                    formatter: 'number',
                    summaryTpl: "<b>{0}</b>",
                    summaryType: "sum"
                },
                {label: 'Employee ID', name: 'EmployeeID', width: 150}
            ],
            loadonce: true,
            viewrecords: true,
            rowList: [20, 30, 50],
            width: 780,
            height: 250,
            rowNum: 20,
            sortname: 'OrderDate',
            pager: "#jqGridPager",
            grouping: true,
            groupingView: {
                groupField: ["CustomerID", "EmployeeID"],
                groupColumnShow: [true, true],
                groupText: [
                    "CustomerID: <b>{0}</b>",
                    "EmployeeID: <b>{0}</b>"
                ],
                groupOrder: ["asc", "asc"],
                groupSummary: [true, false],
                groupSummaryPos: ['header', 'header'],
                groupCollapse: false
            }
        });
    });
