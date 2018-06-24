let data_save;
$(document).ready(function () {
    data_save = data;
    $('#btn-search-problem').click(function () {
        const post_data = {};
        post_data["type"] = 0;


        $.ajax({
            url: data_save.problem_search_url,
            type: 'get',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                $("#problem-table-body").empty("");
                for (var i = 0; i < 5; i++) {
                    let table = $('#problem-table-body');

                    let new_tr = $("<tr>" +
                        "<td>" + "1" + "</td>" +
                        "<td>" + "数学" + "</td>" +
                        "<td>" + "ch2" + "</td>" +
                        "<td>" + "函数" + "</td>" +
                        "<td>" + "2018-01-12" + "</td>" +
                        "<td><button class='btn btn-primary btn-problem-detail' style='height:80%'>详细 </button></td>" +
                        "<td><button class='btn btn-primary' style='height:80%'>添加</button></td>" +
                        "</tr>");
                    new_tr.appendTo(table);
                }
                console.log(data);
            },
            error: function (msg) {
                console.log(msg);
            }
        });
    });
    $('.btn-problem-detail').click(function () {
        window.location.href = data_save.problem_detail_url;
    });

});