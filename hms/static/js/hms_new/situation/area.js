class area{
    constructor() {

    }

    getAdmAreaKor(depth, cd) {
        let ret = [];

        $.ajax({
            method: 'GET',
            url: '/common/get_adm_area_ko_names',
            data: {[depth]: cd},
            // async: true,
            beforeSend: function() {
                alert('데이터 처리 중');
            },
            complete: function() {
                alert('데이터 완료');
            }
        }).done(function (data) {
            ret = data.items;
            console.log(ret);
        }).complete(function (data) {
            console.log(data);
            return data;
        })
    }
}