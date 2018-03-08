document.write("<sciprt src=\"{{ url_for('static', filename='scripts/config_0.0.22.js') }}\"></sciprt>");
document.write("<sciprt src=\"{{ url_for('static', filename='js/hms/ui.js') }}\"></sciprt>");
document.write("<sciprt src='https://openlayers.org/en/v4.2.0/build/ol.js'></sciprt>");


class HmsBookmark {
    constructor(url) {
        this.url = url;
        console.log(url);
    }


    static findConfigByIndex(index) {
        let traceIndex = 0;
        let ret = {};
        $.each(FUNC, function (i, item) {
            if (traceIndex === Number(index)) {
                ret = item;
                return false;
            }

            traceIndex += 1;
        });
        return ret;
    }

    setBookmarkName($this) {
        $('input:text[name=txt-bookmark-name]').val($this.is(':checked') ? $this.next().text() : '');
        $('input:checkbox[name=cbx-bookmark]').not($this).prop('checked', false);
    }

    selectBookmarks(page) {
        $.ajax({
            method: 'POST',
            url: this.url.select,
            data: {bookmark_page: page},
            dataType: 'json'
        }).done(function (data) {
            let results = [];

            if (data.items.length !== 0) {
                $.each(data.items, function (i, item) {
                    results.push('<tr><td>');
                    results.push(`<input type="checkbox" name="cbx-bookmark" value="${item.id}" onclick="hmsBookmark.setBookmarkName($(this));">`);
                    results.push(`<a href="#" onclick="hmsBookmark.executeBookmark(${item.target},'${item.parameter}');">${item.name}</a>`);
                    //                        results.push('<td class="text-right"><button class="btn btn-default btn-sm btn-bookmark"><i class="fa fa-eye" aria-hidden="true"></a></button></td>');
                    results.push('</td></tr>');
                });
            } else {
                results.push('<tr><td class="text-center">');
                results.push('검색 결과가 없습니다.');
                results.push('</td></tr>');
            }
            $('#tbl-bookmark tbody').empty().append(results.join(''));
            $('input:text[name=txt-bookmark-name]').val('');
        });
    }

    executeBookmark(target, parameter) {
        console.log(HmsBookmark.findConfigByIndex());
        let NAME_TYPE_CONF = {
            popltn_stats: {
                ps_age_grp_cd: 'selectpicker',
                ps_syear: 'selectpicker',
                ps_smonth: 'selectpicker',
                ps_eyear: 'selectpicker',
                ps_emonth: 'selectpicker'
            },
            hshold_stats: {
                hs_fmly_num_cd: 'selectpicker',
                hs_rsdnc_clsftn_cd: 'selectpicker',
                hs_room_num_cd: 'selectpicker',
                hs_syear: 'selectpicker',
                hs_smonth: 'selectpicker',
                hs_eyear: 'selectpicker',
                hs_emonth: 'selectpicker'
            },
            popltn_mvmt: {
                pm_aplcnt_age_cd: 'selectpicker',
                pm_mv_reasn_cd: 'selectpicker',
                pm_fmly_num_cd: 'selectpicker',
                pm_syear: 'selectpicker',
                pm_smonth: 'selectpicker',
                pm_eyear: 'selectpicker',
                pm_emonth: 'selectpicker'
            },
            trnstn_situtn_trans: {
                tst_trans_type: 'toggle_button',
                tst_house_kind: 'toggle_button',
                tst_ssale: 'range_slider',
                tst_esale: 'range_slider',
                tst_sdeposit: 'range_slider',
                tst_edeposit: 'range_slider',
                tst_srent: 'range_slider',
                tst_erent: 'range_slider',
                tst_sexarea: 'range_slider',
                tst_eexarea: 'range_slider',
                tst_sdecrepit: 'range_slider',
                tst_edecrepit: 'range_slider',
                tst_sale: 'range_slider',
                tst_deposit: 'range_slider',
                tst_rent: 'range_slider',
                tst_exarea: 'range_slider',
                tst_decrepit: 'range_slider',
                tst_syear: 'selectpicker',
                tst_smonth: 'selectpicker',
                tst_eyear: 'selectpicker',
                tst_emonth: 'selectpicker'
            },
            trnstn_situtn_price: {
                tsp_trans_type: 'toggle_button',
                tsp_house_kind: 'toggle_button',
                tsp_ssale: 'range_slider',
                tsp_esale: 'range_slider',
                tsp_sdeposit: 'range_slider',
                tsp_edeposit: 'range_slider',
                tsp_srent: 'range_slider',
                tsp_erent: 'range_slider',
                tsp_sexarea: 'range_slider',
                tsp_eexarea: 'range_slider',
                tsp_sdecrepit: 'range_slider',
                tsp_edecrepit: 'range_slider',
                tsp_sale: 'range_slider',
                tsp_deposit: 'range_slider',
                tsp_rent: 'range_slider',
                tsp_exarea: 'range_slider',
                tsp_decrepit: 'range_slider',
                tsp_syear: 'selectpicker',
                tsp_smonth: 'selectpicker',
                tsp_eyear: 'selectpicker',
                tsp_emonth: 'selectpicker'
            },
            idnftn_bldng: {
                ib_house_kind: 'toggle_button',
                ib_sexarea: 'range_slider',
                ib_eexarea: 'range_slider',
                ib_exarea: 'range_slider',
                ib_syear: 'selectpicker',
                ib_smonth: 'selectpicker',
                ib_eyear: 'selectpicker',
                ib_emonth: 'selectpicker'
            },
            busins_situtn: {
                busins_wide_cd: 'selectpicker',
                busins_narr_cd: 'selectpicker'
            },
            hshold_imgrat: {
                hi_fmly_num_cd: 'selectpicker',
                hi_syear: 'selectpicker',
                hi_smonth: 'selectpicker',
                hi_eyear: 'selectpicker',
                hi_emonth: 'selectpicker'
            },
            supply_present: {
                sp_type: 'toggle_button',
                sp_sexarea: 'range_slider',
                sp_eexarea: 'range_slider',
                sp_exarea: 'range_slider',
                sp_syear: 'selectpicker',
                sp_smonth: 'selectpicker',
                sp_eyear: 'selectpicker',
                sp_emonth: 'selectpicker'
            },
            income_situtn: {
                is_type: 'toggle_button'
            }
        };

        $('#west-accordion').accordion('option', 'active', target);
        parameter = decodeURIComponent(parameter);

        let codeStyleShort = HmsBookmark.findConfigByIndex(target).CODE_STYLE_SHORT;

        let paramObj = {};
        $.each(parameter.split('&'), function (i, param) {
            let pairs = param.split('=');
            let name = pairs[0];
            let value = pairs[1];

            if (NAME_TYPE_CONF[HmsBookmark.findConfigByIndex(target).CODE_STYLE][name] !== 'range_slider') {
                if (paramObj[name]) {
                    paramObj[name].push(value);
                } else {
                    paramObj[name] = [value];
                }
            } else {
                name = codeStyleShort + '_' + name.substring(codeStyleShort.length + 2, name.length);

                if (paramObj[name]) {
                    paramObj[name].push(Number(value));
                } else {
                    console.log(NAME_TYPE_CONF[HmsBookmark.findConfigByIndex(target).CODE_STYLE][name]);
                    paramObj[name] = [Number(value)];
                }
            }

        });

        $.each(paramObj, function (key, value) {

            // TODO : 지역 코드 여러개 들어갈 수 있도록 해야함
            if (key.indexOf('sid_cd') >= 0 || key.indexOf('sgg_cd') >= 0 || key.indexOf('emd_cd') >= 0) {
                if (HmsBookmark.findConfigByIndex(target).CODE_STYLE === 'popltn_mvmt') {
                    if (key.indexOf('out_') >= 0) {
                        let ko_name = getAreaKor(HmsBookmark.findConfigByIndex(target).LOCATION_TYPE, value);

                        let outAreaContent = '<input locationdepth="' + key.split('_')[0] + '" type="hidden" name="' + key + '" value="' + value + '">' +
                            '<span class="label label-success" style="display: inline-block;">' + ko_name[0].ko_nm + '</span>';
                        $('#spn-' + codeStyleShort + '-oa').html(outAreaContent);
                    }

                    if (key.indexOf('in_') >= 0) {
                        let ko_name = getAreaKor(HmsBookmark.findConfigByIndex(target).LOCATION_TYPE, value);

                        let inAreaContent = '<input locationdepth="' + key.split('_')[0] + '" type="hidden" name="' + key + '" value="' + value + '">' +
                            '<span class="label label-success" style="display: inline-block;">' + ko_name[0].ko_nm + '</span>';
                        $('#spn-' + codeStyleShort + '-ia').html(inAreaContent);
                    }
                } else {
                    let ko_name = getAreaKor(HmsBookmark.findConfigByIndex(target).LOCATION_TYPE, value);

                    let areaContent = '<input locationdepth="' + key.split('_')[0] + '" type="hidden" name="' + key + '" value="' + value + '">' +
                        '<span class="label label-success" style="display: inline-block;">' + ko_name[0].ko_nm + '</span>';
                    $('#spn-' + codeStyleShort + '-area').html(areaContent);
                }
            }

            let nameType = NAME_TYPE_CONF[HmsBookmark.findConfigByIndex(target).CODE_STYLE][key];

            if (nameType === 'selectpicker') {
                $('#' + key).selectpicker('val', value);
            }

            if (nameType === 'toggle_button') {
                $.each($('input[name=' + key + ']'), function (i, element) {
                    if ($(element).val() === value[0]) {
                        $(element).parent().addClass('active');
                        $(element).prop('checked', true);

                        if (codeStyleShort === 'tst' && key === 'tst_trans_type') {
                            chagngetst(value[0]);
                        }

                        if (codeStyleShort === 'tsp' && key === 'tsp_trans_type') {
                            chagngetsp(value[0]);
                        }
                    } else {
                        $(element).parent().removeClass('active');
                        $(element).removeAttr('checked');
                    }
                });
            }

            if (nameType === 'range_slider') {
                let replaceKey = key.replace('_', '-');

                $('#' + replaceKey + '-slider').slider("option", "values", value);
                let $labelEl = $('#' + replaceKey + '-label')
                let originText = $labelEl.text();
                let thisUnit = originText.substring(originText.indexOf("(") + 1, originText.indexOf(")"));

                $labelEl.text(' ' + hmsUtil.setComma(String(value[0])) + ' ~ ' + String(hmsUtil.setComma(value[1])) + ' (' + thisUnit + ')');

                $('#' + key.replace('_', '_s')).val(value[0]);
                $('#' + key.replace('_', '_e')).val(value[1]);
            }
        });
    }

    showAddBookMark() {
        var $target = $('#west-accordion').accordion('option', 'active');

        $('#frm-filter-' + $target)
            .clone()
            .prependTo($('#clone-form'));

        let hmsUi = new HmsUi();
        hmsUi.showModal('mdl-bookmark');

        $('#mdl-bookmark').on('hide.bs.modal', function () {
            $('#clone-form').empty();
        });
    }

    addBookmark() {
        let $nameEl = $('#bookmark-name');
        let $name = $nameEl.val();

        if ($name === '') {
            alert('즐겨찾기 명칭을 입력해주세요.');
            $nameEl.focus();
            return;
        }

        let $target = $('#west-accordion').accordion('option', 'active');
        let $parameter = $('#frm-west-' + $target).serialize();

        $.ajax({
            method: 'POST',
            url: this.url.select,
            data: {name: $name, target: $target, parameter: encodeURIComponent($parameter)},
            dataType: 'json'
        }).done(function (data) {
            alert(data.msg);
            console.log(this);
            this.selectBookmarks(1);

            let hmsUi = new HmsUi();
            hmsUi.hideModal('mdl-bookmark');
        });
    }

    deleteBookmark() {
        var $this = $('input:checkbox[name=cbx-bookmark]');
        if ($this.is(':checked') == false) {
            alert('삭제할 검색 명칭을 체크해주세요.');
            return;
        }
        var $id;
        $this.each(function () {
            if ($(this).is(':checked') == true) {
                $id = $(this).val();
            }
        });
        $.ajax({
            method: 'POST',
            url: this.url.delete,
            data: {id: $id},
            dataType: 'json'
        }).done(function (data) {
            alert(data.msg);
            selectBookmarks(1);
        });
    }

    edit_bookmark() {
        var $this = $('input:checkbox[name=cbx-bookmark]');
        if ($this.is(':checked') == false) {
            alert('수정할 검색 명칭을 체크해주세요.');
            return;
        }
        var $id;
        $this.each(function () {
            if ($(this).is(':checked') == true) {
                $id = $(this).val();
            }
        });
        $.ajax({
            method: 'POST',
            url: this.url.update,
            data: {id: $id, name: $('input:text[name=txt-bookmark-name]').val()},
            dataType: 'json'
        }).done(function (data) {
            alert(data.msg);
            selectBookmarks(1);
        });
    }
}