document.write("<sciprt src=\"{{ url_for('static', filename='scripts/vendor/hms/util.js') }}\"></sciprt>");

class HmsChart {
    constructor() {

    }

    getRadarConfig() {
        return {
            type: 'radar',
            data: {labels: [], datasets: []},
            options: {
                legend: {position: 'top'},
                title: {display: true, text: ''},
                scale: {ticks: {beginAtZero: true}}
            }
        }
    }

    getBarConfig() {
        let hmsUtil = new HmsUtil();

        return {
            type: 'bar',
            data: {labels: [], datasets: []},
            options: {
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {
                            let value = data.datasets[0].data[tooltipItem.index];
						    value = value.toString();
						    return hmsUtil.setComma(value);
                        }
                    }
                },
                legend: {display: true},
                title: {display: true, text: ''},
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: false,
                            userCallback: function(value, index, values) {
                                value = value.toString();
                                return hmsUtil.setComma(value);
                            }
                        }
                    }]
                }
            }
        }
    }

    getHorizontalBarConfig() {
        return {
            type: 'horizontalBar',
            data: {labels: [], datasets: []},
            options: {
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {
                            let value = data.datasets[0].data[tooltipItem.index];
						    value = value.toString();
						    return hmsUtil.setComma(value);
                        }
                    }
                },
                legend: {display: true},
                title: {display: true, text: ''},
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero: false,
                            userCallback: function(value, index, values) {
                                value = value.toString();
                                return hmsUtil.setComma(value);
                            }
                        }
                    }]
                }
            }
        }
    }

    getAreaConfig() {
        return {
            type: 'area',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                legend: {display: true},
                title: {display: false, text: ''}
            }
        }
    }

    getLineConfig() {
        return {
            type: 'line',
            data: {labels: [], datasets: []},
            options: {
                responsive: true,
                title: {display: true, text: ''},
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function (tooltipItem, data) {
                            let value = data.datasets[0].data[tooltipItem.index];
						    value = value.toString();
						    return hmsUtil.setComma(value);
                        }
                    }
                },
                hover: {mode: 'nearest', intersect: false},
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: ''
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: ''
                        },
                        ticks: {
                            beginAtZero: false,
                            userCallback: function(value, index, values) {
                                value = value.toString();
                                return hmsUtil.setComma(value);
                            }
                        }
                    }]
                }
            }
        }
    }

    getPieConfig() {
        return {
            type: 'pie',
            data: {labels: [], datasets: []},
            options: {
                responsive: true,
                legend: {display: true, position: 'top'},
                title: {display: true, position: 'top', text: ''}
            }
        }
    }

    getAcceptableTarget(chartType, target) {
        let acceptableTarget = {
            radar: {
                popltn_stats: false,
                hshold_stats: false,
                popltn_mvmt: false,
                trnstn_situtn: false,
                idnftn_bldng: false,
                busins_situtn: false,
                hshold_imgrat: false,
                supply_present: false,
                income_situtn: false
            },
            bar: {
                popltn_stats: true,
                hshold_stats: true,
                popltn_mvmt: false,
                trnstn_situtn_trans: true,
                trnstn_situtn_price: true,
                idnftn_bldng: true,
                busins_situtn: true,
                hshold_imgrat: true,
                supply_present: true,
                income_situtn: false
            },
            horizontalBar: {
                popltn_stats: true,
                hshold_stats: true,
                popltn_mvmt: false,
                trnstn_situtn_trans: true,
                trnstn_situtn_price: true,
                idnftn_bldng: true,
                busins_situtn: true,
                hshold_imgrat: true,
                supply_present: true,
                income_situtn: false
            },
            area: {
                popltn_stats: false,
                hshold_stats: false,
                popltn_mvmt: false,
                trnstn_situtn_trans: true,
                trnstn_situtn_price: true,
                idnftn_bldng: false,
                busins_situtn: false,
                supply_present: false,
                income_situtn: false
            },
            line: {
                popltn_stats: true,
                hshold_stats: true,
                popltn_mvmt: true,
                trnstn_situtn_trans: true,
                trnstn_situtn_price: true,
                idnftn_bldng: true,
                busins_situtn: true,
                hshold_imgrat: true,
                supply_present: true,
                income_situtn: false
            },
            pie: {
                popltn_stats: false,
                hshold_stats: false,
                popltn_mvmt: false,
                trnstn_situtn: false,
                idnftn_bldng: false,
                busins_situtn: false,
                hshold_imgrat: false,
                supply_present: false,
                income_situtn: false
            }
        };

        return acceptableTarget[chartType][target];
    }

    parseChartTypeToKor(chartType) {
        let parseObj = {
            radar: "레이더",
            bar: "세로 막대",
            horizontalBar: "가로 막대",
            area: "영역",
            line: "라인",
            pie: "파이",
        };

        return parseObj[chartType]
    }

    setChart(chartType, target, canvasId, modalId) {
        let ctx = document.getElementById(canvasId).getContext("2d");

        if (typeof(target) !== 'undefined' &&
            !this.getAcceptableTarget(chartType, target)) {
            alert("본 검색 결과에서는 " + this.parseChartTypeToKor(charType) + " 그래프를 지원하지 않습니다.");
        } else {
            if (chartType === 'radar') {
                //dataParseForRadar를 불러온다.
            } else if(chartType === 'bar') {

            } else if(chartType === 'horizontalBar') {

            } else if(chartType === 'area') {

            } else if(chartType === 'line') {

            } else if(chartType === 'pie') {

            }
        }
    }
}