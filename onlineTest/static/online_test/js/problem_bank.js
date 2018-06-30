let data_save;
$(document).ready(function () {
    data_save = data;

    $('#btn-search-problem').click(function () {
        const post_data = {};
        post_data["type"] = 2;
        post_data["creator"] = $("#creator").val();
        post_data["subject"] = $("#subject").val();
        post_data["chapter"] = $("#chapter").val();
        post_data["knowledge_point"] = $("#knowledge-point").val();


        $.ajax({
            url: data_save.problem_search_url,
            method: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                let problems = data["infos"];
                console.log(problems);

                let choice_problem = problems['choice'];
                console.log('hello');

                $("#choice-problem-table-body").empty("");
                for (let index in choice_problem) {
                    let table = $('#choice-problem-table-body');
                    let subject = choice_problem[index][index]["subject"];
                    if ( subject == undefined) {
                        subject = "软件工程";
                    }

                    let new_tr = $("<tr>" +
                        "<td class='hidden'>"  +choice_problem[index][index]["pk"] + "</td>" +
                        "<td>" + choice_problem[index][index]["content"].slice(0, 10) +"..."+ "</td>" +
                        "<td>" + subject + "</td>" +
                        "<td>" + choice_problem[index][index]["chapter"] + "</td>" +
                        "<td>" + choice_problem[index][index]["knowledge_point"] + "</td>" +
                        "<td>" + choice_problem[index][index]["creator"] + "</td>" +
                        "<td><button class='btn btn-primary btn-problem-detail' style='height:80%'>详细 </button></td>" +
                        "</tr>");
                    new_tr.appendTo(table);
                }

                let judge_problems = problems['judge'];

                $("#judge-problem-table-body").empty("");
                for (let index in judge_problems) {
                    console.log(judge_problems[index][index]["content"]);
                    let table = $('#judge-problem-table-body');

                     let subject = judge_problems[index][index]["subject"];
                    if ( subject == undefined) {
                        subject = "软件工程";
                    }

                    let new_tr = $("<tr>" +
                        "<td class='hidden'>"  + judge_problems[index][index]["pk"] + "</td>" +
                        "<td>" + judge_problems[index][index]["content"].slice(0, 10) +"..."+ "</td>" +
                        "<td>" + subject + "</td>" +
                        "<td>" + judge_problems[index][index]["chapter"] + "</td>" +
                        "<td>" + judge_problems[index][index]["knowledge_point"] + "</td>" +
                        "<td>" + judge_problems[index][index]["creator"]+ "</td>" +
                        "<td><button class='btn btn-primary btn-problem-detail' style='height:80%'>详细 </button></td>" +
                        "</tr>");
                    new_tr.appendTo(table);
                }
            },
            error: function (msg) {
                console.log('error');
                console.log(msg);
            }
        });
    });

    $('#btn-single-problem-nav').click(function () {
       window.open(data_save.problem_detail_url);
    });

    $(document).on('click', '.btn-problem-detail', function () {
        let pk = $(this).parent().parent().children("td:nth-child(1)").text();
        if ($('#choice_problem').is('.active')) {
            console.log(1)
            let url = data_save.problem_choice_detail_url;
            let index = url.lastIndexOf("\/");
            url = url.substr(0, index-1);
            url += pk+"/";
            console.log(url);

            window.open(url);
        } else {
            console.log(2);
            let url = data_save.problem_judge_detail_url;
            let index = url.lastIndexOf("\/");
            url = url.substr(0, index-1);
            url += pk+"/";
            console.log(url);

            window.open(url);
        }
    });

    $('#btn-insert-problem').click(function () {
        const post_data = {};

        let type = $('#choice_problem').is('.active')?1:0;
        console.log(type);
        post_data["type"] = type;
        post_data["content"] = $('#content').val();
        if (type == 1) {
            post_data["choice_a"] = $("#choice_a").val();
            post_data["choice_b"] = $("#choice_b").val();
            post_data["choice_c"] = $("#choice_c").val();
            post_data["choice_d"] = $("#choice_d").val();
        }

        post_data["solution"] = ($("#solution").val() === "T");
        post_data["score"] = $("#score").val();
        post_data["subject"] = $("#subject").val();
        post_data["chapter"] = $("#chapter").val();
        post_data["knowledge_point"] = $("#knowledge_point").val();

        console.log(post_data)
        $.ajax({
            url: data_save.problem_add_url,
            type: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                if (data['result'] === "ok")
                    alert('添加成功');
            },
            error: function (msg) {
                console.log('error');
                console.log(msg);
            }
        });
    });
    $('#btn-update-problem').click(function () {
        const post_data = {};

        post_data["type"] = type;
        post_data["content"] = $('#content').val();
        let url = window.location.href;
        url = url.substr(0, url.length-1);

        let index = url.lastIndexOf("\/");
        let pk = url.substr(index+1, url.length-index);

        url = "/online_test/problem_bank/"+pk+"/mod/";
        console.log(url);

        if (type == 1) {
            post_data["choice_a"] = $("#choice_a").val();
            post_data["choice_b"] = $("#choice_b").val();
            post_data["choice_c"] = $("#choice_c").val();
            post_data["choice_d"] = $("#choice_d").val();
        }
        post_data["solution"] = $("#solution").val();
        post_data["score"] = $("#score").val();
        post_data["subject"] = $("#subject").val();
        post_data["chapter"] = $("#chapter").val();
        post_data["knowledge_point"] = $("#knowledge_point").val();


        console.log(post_data);
        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                console.log(data);
                if (data['result'] === "ok")
                    alert('更新成功');
            },
            error: function (msg) {
                console.log('error');
                console.log(msg);
            }

        });
    });
    $('#btn-update-choice-problem').click(function () {
        const post_data = {};

        post_data["type"] = 1;
        post_data["content"] = $('#content').val();
        let url = window.location.href;
        url = url.substr(0, url.length-1);

        let index = url.lastIndexOf("\/");
        let pk = url.substr(index+1, url.length-index);

        url = "/online_test/problem_bank/"+pk+"/mod/";
        console.log(url);

        post_data["solution"] = $("#solution").val();
        post_data["score"] = $("#score").val();
        post_data["subject"] = $("#subject").val();
        post_data["chapter"] = $("#chapter").val();
        post_data["knowledge_point"] = $("#knowledge_point").val();
        console.log(post_data);

        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                console.log(data);
                if (data['result'] === "ok")
                    alert('更新成功');
            },
            error: function (msg) {
                console.log('error');
                console.log(msg);
            }

        });
    });
    $('#btn-delete-problem').click(function () {
        let url = window.location.href;
        url = url.substr(0, url.length-1);

        let index = url.lastIndexOf("\/");
        let pk = url.substr(index+1, url.length-index);
        url = "/online_test/problem_bank/"+pk+"/del/";
        console.log(data_save.problem_delete_url);
        console.log(url);

        const post_data = {};
        post_data["type"] = type;

        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                // if (data['result'] === "ok")
                alert('删除成功');
                window.close();
            },
            error: function (msg) {
                alert("删除未成功，请稍后尝试");
                console.log('error');
                console.log(msg);
            }
        });
    });

    $('#btn-delete-choice-problem').click(function () {
        let url = window.location.href;
        url = url.substr(0, url.length-1);

        let index = url.lastIndexOf("\/");
        let pk = url.substr(index+1, url.length-index);
        url = "/online_test/problem_bank/"+pk+"/del/";
        console.log(data_save.problem_delete_url);
        console.log(url);

        const post_data = {};
        post_data["type"] = 1;

        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                // if (data['result'] === "ok")
                alert('删除成功');
                window.close();
            },
            error: function (msg) {
                alert("删除未成功，请稍后尝试");
                console.log('error');
                console.log(msg);
            }
        });
    });
});
