$(document).ready(function () {

    var count = 0;

    $('#addinput').click(function () {
        count++;

        var keyvalue = '<div class="keyvalue" index="' + count + '"> <label>요청 변수</label><div class="delete btn-click" cnt="' + count + '"><span></span><span></span></div> <input class="req_data" type="text"><input class="req_data" type="text"></div>'
        $('.keyvalue:last').after(keyvalue);

        console.log('추가완료');
    });




    $(document).on("click", ".delete", function () {
        var cnt = $(this).attr('cnt');
        console.log(cnt);
        var data = $('div [index="' + cnt + '"]').remove();
    });


    $('#senddata').click(function () {
        $('#downdata').remove();
        senddata();

    });


});

function senddata() {
    var url = $('#url').val();
    var key = $('#key').val();
    var req_data = new Array();
    $('.req_data').each(function () {
        var r_data = $(this).val();
        req_data.push(r_data);
    });




    $.ajax({
        type: 'POST',

        url: './publicapi',
        data: {
            url: url,
            key: key,
            req_data: req_data
        },
        dataType: 'JSON',
        success: function (data) {

            console.log(data);
            var rep_data = data['rep_data']
            if (rep_data == 0) {
                rep_data = '<div class="error">데이터가 없습니다.</div>';
            }
            if (rep_data == 1) {
                rep_data = '<div class="error">요청 변수를 확인해 주세요.</div>';
            }
            if (rep_data.length == 149) {
                rep_data = '<div class="error">요청 하신 데이터가 없습니다.</div>';
            }
            if (rep_data == 00) {
                rep_data = '<div class="error">요청하신 날짜에 데이터가 없습니다.</div>'
            }

            var sub_tag = '<div class="dataform subtitle">요청 데이터 </div>' + rep_data;

            $('.infortitle').remove();
            $('.tablesection').empty();
            $('.tablesection').append(sub_tag);
            console.log(rep_data);

            var filename = data['path'];

            var dn_btn = '<form action="./download" method="POST" enctype="multipart/form-data"><input type="hidden" value="' + filename + '" name="filename"><input type="submit" id="downdata" class="box-shadow" value="다운로드"></form>'

            if (filename !== "") {
                $('#senddata').after(dn_btn);
                setTimeout(function () {
                    $('#downdata').remove();
                    deletedata(filename);
                }, 10000);


            };
        },
        error: function (error) {
            console.log(error);
        }

    });
};

function deletedata(filename) {
    console.log(filename);
    $.ajax({
        type: 'POST',

        url: './deletedata',
        data: {
            filename: filename

        },
        dataType: 'JSON',
        success: function (data) {
            console.log(data)
        },
        error: function (error) {
            console.log(error);
        }

    });

};
