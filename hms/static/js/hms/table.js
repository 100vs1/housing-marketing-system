const EXCEPTIONS_COL_NAME = {
    'sid_ko_nm': '시도',
    'sgg_ko_nm': '시군구',
    'emd_ko_nm': '시도'
};

class HmsSituationTable {

    constructor(id, cols, rows, title, summaryType) {
        this.cols = cols;                 // 데이터 컬럼 Array
        this.rows = rows;                 // 데이터 Row Array
        this.title = title;               // Table Title
        this.colNames = null;             // colNames
        this.colModel = null;             // colModel
        this.id = id;                     // Table Element ID
        this.targetEL = $('#' + id).find($('table'));    // Table Element
        this.summaryType = summaryType;
        this.tableConfig = this.initTableConfig();  // Table Configuration

        // this.resetTable();
    }

    initTableConfig() {
        return {
            datatype: "local",
            height: 600,
            styleUI: 'Bootstrap',
            loadone: true,
            colNames: [],
            colModel: [],
            loadonce: true,
            viewrecords: true,
            autowidth: true,
            shrinkToFit: true,
            rowNum: 100,
            rowList: [100, 200, 300],
            grouping: true,
            groupingView: {
                groupField: ['sid_ko_nm'],
                groupColumnShow: [true],
                groupText: [
                    "<b>{0}</b>",
                ],
                groupOrder: ["asc"],
                groupSummary: [true],
                groupSummaryPos: ['header'],
                groupCollapse: false
            }
        };
    }

    getColNames() {
        return this.colNames;
    }

    setColNames(colNames) {
        this.colNames = colNames;
    }

    getColModel() {
        return this.colModel;
    }

    setColModel(colModel) {
        this.colModel = colModel;
    }

    getRows() {
        return this.rows;
    }

    setRows(rows) {
        this.rows = rows;
    }

    getTableConfig(type = "situation") {
        return this.tableConfig
    }

    setTableConfig(tableConfig) {
        this.tableConfig = tableConfig;
    }

    setGroupView(groupView) {
        this.tableConfig.groupingView = groupView;
    }

    getGroupView() {
        return this.tableConfig.groupingView;
    }

    setGroupFieldId(groupField) {
        if (Array.isArray(groupField)) {
            this.tableConfig.groupField = groupField;
        } else {
            throw new Error(`${this.constructor.name}: GroupField type is wrong ${groupField}`);
        }
    }

    resetTableForUI() {
        $('#pivotTitle').html("");
        $('#pivotFilters').html("");
        $('#pivotDownload').html("");
        $('#pivot-tab').html("");
        $('#pivot-table').html("<table id='pivotTables'></table>");
    }

    resetTable() {
        $('#' + this.id).html("<table id='pivotTables'></table>");
        // $('#' + id).replaceWith(`<table id="${id}"></table>`)
        // this.targetEL.jqGrid('clearGridData').trigger('reloadGrid');
    }

    parseColNames(exceptions) {
        if(!exceptions){
            exceptions = EXCEPTIONS_COL_NAME;
        }

        if (!this.getColNames()) {
            let colNames = [];
            let hmsUtil = new HmsUtil();

            let forLength = this.cols.length;
            for (let i = 0; i < forLength; i++) {
                let item = this.cols[i];

                if (item in exceptions) {
                    item = exceptions[item];
                } else {
                    item = hmsUtil.getDateToKor([item], " ");
                }

                colNames.push(item);
            }

            this.setColNames(colNames);
            return colNames;
        } else {
            return this.getColNames();
        }
    }

    parseColModel(exceptions) {
        if (!exceptions){
            exceptions = EXCEPTIONS_COL_NAME
        }

        let numberFormat = this.numberFormat;
        let hmsUtil = new HmsUtil();
        if (!this.getColModel()) {
            let rows = this.cols;
            let colModel = [];

            let forLength = rows.length;
            for (let i = 0; i < forLength; i++) {
                let tempColModel = {};
                let item = rows[i];

                if (item in exceptions) {
                    tempColModel.name = item;
                } else {
                    tempColModel.name = item;
                    tempColModel.formatter = formatNumber;
                    tempColModel.summaryTpl = '<b>{0}</b>';
                    tempColModel.summaryType = this.summaryType;
                    tempColModel.align = 'right';


                    function formatNumber(cellValue, options, rowdata, action) {
                        if (cellValue === "")
                            return 0;
                        if (cellValue === null || cellValue === 'null')
                            return 0;
                        if ((cellValue !== null || cellValue !== 'null')) {
                            if (getDecimalCount(cellValue) > 0) {
                                return parseFloat(cellValue).toFixed(2);
                            }
                            return hmsUtil.setComma(cellValue);
                        }

                        return hmsUtil.setComma(cellValue);
                    }

                    function getDecimalCount(number) {
                        number = parseFloat(number);

                        let decimalIdx = String(number).indexOf('.');
                        if (decimalIdx !== -1) {
                            return String(number).substring(decimalIdx + 1, String(number).length).length
                        } else {
                            return 0;
                        }
                    }
                }

                colModel.push(tempColModel);
            }

            this.setColModel(colModel);
            return colModel;
        } else {
            return this.getColModel();
        }
    }

    setGroupData() {
        // situation에서는 그룹핑을 하나만,
        // 컬럼 처음 값으로 하는 것으로 정의한다.
        let groupView = this.getGroupView();
        groupView.groupField = [this.cols[0]];

    }

    setTableData(colNamesExcept, colModelExcept) {
        this.setGroupData();
        this.tableConfig.colNames = this.parseColNames(colNamesExcept);
        this.tableConfig.colModel = this.parseColModel(colModelExcept);

        this.targetEL.jqGrid(this.getTableConfig());

        for (let i = 0; i <= this.rows.length; i++) {
            this.targetEL.jqGrid('addRowData', i + 1, this.rows[i]);
        }

        this.targetEL.jqGrid().trigger('reloadGrid');
    }


    // TODO 우선 이거 나중에 Table UI Class로 빼던지 어쩌던지..
    addTimeseries(targetId, tableObject) {
        let CONFIG = [
            {
                "value": "yearly",
                "text": "년 별",
                "checked": false,
                "standard": [1]
            },
            {
                "value": "halfly",
                "text": "반기 별",
                "checked": false,
                "standard": [1, 6]
            },
            {
                "value": "quarterly",
                "text": "분기 별",
                "checked": false,
                "standard": [1, 4, 7, 10]
            },
            {
                "value": "monthly",
                "text": "월 별",
                "checked": true,
                "standard": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            }
        ];

        let inputName = 'table-time-series';
        let forLength = CONFIG.length;
        let targetHtml = '<div class="form-group">';
        for (let i = 0; i < forLength; i++) {
            let item = CONFIG[i];

            if (item.checked) {
                targetHtml += `<label class="radio-inline"><input type="radio" name="${inputName}" value="${item.value}" checked="checked">${item.text}</label>`
            } else {
                targetHtml += `<label class="radio-inline"><input type="radio" name="${inputName}" value="${item.value}">${item.text}</label>`
            }
        }
        targetHtml += '</div>';

        $('#' + targetId).html(targetHtml);

        $('input:radio[name="' + inputName + '"]').on('change', function () {

            let targetValue = $(this).val();
            let thisConfig = findByObjectByValue(targetValue);

            // 데이터 파싱
            let resetRows = [];
            $.each(tableObject.rows, function (rowKey, rowValue) {
                let tempObject = {};
                $.each(rowValue, function (k, v) {
                    if (isNaN(Number(k))) {
                        tempObject[k] = v;
                    } else {
                        if ($.inArray(k % 100, thisConfig.standard) !== -1) {
                            tempObject[k] = v;
                        }
                    }
                });
                resetRows.push(tempObject);
            });

            let resetCols = [];
            $.each(tableObject.cols, function (colKey, colValue) {
                if (isNaN(Number(colValue))) {
                    resetCols.push(colValue);
                } else {
                    if ($.inArray(colValue % 100, thisConfig.standard) !== -1) {
                        resetCols.push(colValue);
                    }
                }
            });

            $('#pivot-table').html("<table id='pivotTables'></table>");
            let tempTable = new HmsSituationTable(tableObject.id, resetCols, resetRows, tableObject.title, tableObject.summaryType);

            tempTable.setTableData();
            console.log(tempTable);
        });

        function findByObjectByValue(value) {
            for (let i = 0; i < forLength; i++) {
                if (CONFIG[i].value === value) return CONFIG[i]
            }
        }
    }

    addDownload(targetId, buttonId, extension) {
        let targetEL = this.targetEL;
        let title = this.title;
        let targetHtml =
            '<div class="form-group">' +
            '<button id="' + buttonId + '" class="btn btn-default pull-right" type="button">\<n></n>' +
            // '다운로드' + extension +
            '다운로드' +
            '</button>' +
            '</div>';

        $('#' + targetId).html(targetHtml);

        $('#' + buttonId).on("click", function () {
            let hmsUtil = new HmsUtil();
            if (extension === 'excel') {
                targetEL.jqGrid("exportToExcel", {
                    includeLabels: true,
                    includeGroupHeader: true,
                    includeFooter: true,
                    fileName: title + "_" + hmsUtil.getCurrentDate() + ".xlsx",
                    maxlength: 1000 // maxlength for visible string data
                });
            }
            else if (extension === 'pdf') {
                targetEL.jqGrid("exportToPdf", {
                    includeLabels: true,
                    includeGroupHeader: true,
                    includeFooter: true,
                    fileName: title + "_" + hmsUtil.getCurrentDate() + ".pdf",
                    maxlength: 1000 // maxlength for visible string data
                });
            }
            else if (extension === 'csv') {
                targetEL.jqGrid("exportToCsv", {
                    includeLabels: true,
                    includeGroupHeader: true,
                    includeFooter: true,
                    fileName: title + "_" + hmsUtil.getCurrentDate() + ".csv",
                    mimetype: "text/csv;charset=utf-8",
                    maxlength: 1000 // maxlength for visible string data
                });
            }
            else {
                throw new Error("It is not supported type of download")
            }
        });
    }
}