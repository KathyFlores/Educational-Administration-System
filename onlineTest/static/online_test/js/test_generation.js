var initialized = false;
let data_save;

function set_auto_subject() {
    $("#auto-test-subject").find("option").remove();

    let url = "/online_test/problem_bank/subject";
    //清空select列表数据
    $.ajax({
        url: url,
        method: 'post',
        async: false,
        success: function (data) {
            console.log(data);
            let subject = data['subject'];
            for (let index in subject   ) {
                $("#auto-test-subject").append("<option "+ "value="+ subject[index][index]+">" + subject[index][index] + "</option>");
            }
        },
        error: function (msg) {
            console.log('error');
            console.log(msg);
        }
    });
}

function set_auto_chapter() {
    $("#auto-test-chapter").find("option").remove();

    let url = "/online_test/problem_bank/chapter";
    $.ajax({
        url: url,
        method: 'post',
        async: false,
        success: function (data) {
            console.log(data);
            let chapter = data["chapter"];
            for (let index in chapter) {
                let chapters = chapter[index][$("#auto-test-subject").val()];
                if (chapters != undefined) {
                    for (let chp_idnex in chapters) {
                        $("#auto-test-chapter").append("<option " + "value=" + chapters[chp_idnex][chp_idnex]+ ">" + chapters[chp_idnex][chp_idnex] + "</option>");
                    }
                }
            }
        },
        error: function (msg) {
            console.log('error');
            console.log(msg);
        }
    });

}

function set_auto_knowledge_point() {
    $("#auto-test-knowledge-point").find("option").remove();

    let url = "/online_test/problem_bank/knowledge_point";
    $.ajax({
        url: url,
        method: 'post',
        async: false,
        success: function (data) {
            console.log(data);
            let knowledge_points = data["knowledge_point"];
            for (let index in knowledge_points) {
                let sub_know = knowledge_points[index][$("#auto-test-subject").val()];
                if (sub_know != undefined) {
                    console.log(sub_know);

                    for (let know_index in sub_know ) {
                        $("#auto-test-knowledge-point").append("<option "+ "value="+ sub_know[know_index][know_index]+">" + sub_know[know_index][know_index] + "</option>");
                        }
                }
            }
        },
        error: function (msg) {
            console.log('error');
            console.log(msg);
        }
    });
}

function set_manual_subject() {
    $("#manual-test-subject").find("option").remove();

    let url = "/online_test/problem_bank/subject";
    //清空select列表数据
    $.ajax({
        url: url,
        method: 'post',
        async: false,
        success: function (data) {
            console.log(data);
            let subject = data['subject'];
            for (let index in subject   ) {
                $("#manual-test-subject").append("<option "+ "value="+ subject[index][index]+">" + subject[index][index] + "</option>");
            }
        },
        error: function (msg) {
            console.log('error');
            console.log(msg);
        }
    });
}

function set_subject() {
    $("#subject").find("option").remove();

    let url = "/online_test/problem_bank/subject";
    //清空select列表数据
    $.ajax({
        url: url,
        method: 'post',
        async: false,
        success: function (data) {
            console.log(data);
            let subject = data['subject'];
            for (let index in subject   ) {
                $("#subject").append("<option "+ "value="+ subject[index][index]+">" + subject[index][index] + "</option>");
            }
        },
        error: function (msg) {
            console.log('error');
            console.log(msg);
        }
    });
}

function set_chapter() {
    $("#chapter").find("option").remove();

    let url = "/online_test/problem_bank/chapter";
    $.ajax({
        url: url,
        method: 'post',
        async: false,
        success: function (data) {
            console.log(data);
            let chapter = data["chapter"];
            for (let index in chapter) {
                let chapters = chapter[index][$(".subject").val()];
                if (chapters != undefined) {
                    for (let chp_idnex in chapters) {
                        $("#chapter").append("<option " + "value=" + chapters[chp_idnex][chp_idnex]+ ">" + chapters[chp_idnex][chp_idnex] + "</option>");
                    }
                }
            }
        },
        error: function (msg) {
            console.log('error');
            console.log(msg);
        }
    });

}

function set_knowledge_point() {
    $("#knowledge-point").find("option").remove();

    let url = "/online_test/problem_bank/knowledge_point";
    $.ajax({
        url: url,
        method: 'post',
        async: false,
        success: function (data) {
            console.log(data);
            let knowledge_points = data["knowledge_point"];
            for (let index in knowledge_points) {
                let sub_know = knowledge_points[index][$("#subject").val()];
                if (sub_know != undefined) {
                    console.log(sub_know);

                    for (let know_index in sub_know ) {
                        console.log('hello');
                        $("#knowledge-point").append("<option "+ "value="+ sub_know[know_index][know_index]+">" + sub_know[know_index][know_index] + "</option>");
                        }
                }
            }
        },
        error: function (msg) {
            console.log('error');
            console.log(msg);
        }
    });
}


function auto_check() {
     let name = $("#auto-test-name");
     let subject = $("#auto-test-subject").val();
     let start_time = $("#auto-test-start-time").val();
     let end_time = $("#auto-test-end-time").val();
     if (name == ""||subject == ""||start_time == ""||end_time == "")
         return false;
     return true;
}

function manual_check() {
     let name = $("#manual-test-name");
     let subject = $("#manual-test-subject").val();
     let start_time = $("#manual-test-start-time").val();
     let end_time = $("#manual-test-end-time").val();
     if (name == ""||subject == ""||start_time == ""||end_time == "")
         return false;
     return true;
}

$(document).ready(function () {
    data_save = data;
    set_subject();
    set_chapter();
    set_knowledge_point();

    set_auto_subject();
    set_auto_chapter();
    set_auto_knowledge_point();

    set_manual_subject();

    $("#subject").change(function () {
        set_chapter() ;
        set_knowledge_point();
    })

    $("#auto-test-subject").change(function () {
        set_auto_chapter() ;
        set_auto_knowledge_point();
    })

    $('#btn-search-problem').click(function () {
        const post_data = {};
        post_data["type"] = 2;
        post_data["creator"] = $("#creator").val();
        post_data["subject"] = $("#subject").val();
        post_data["chapter"] = $("#chapter").val();
        post_data["knowledge_point"] = $("#knowledge-point").val();

        $.ajax({
            url: data_save.problem_search_url,
            type: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                $("#problem-table-body").empty("");
                let problems = data["infos"];

                let judge_problems = problems['judge'];
                for (let index in judge_problems) {
                    let table = $('#problem-table-body');
                    let new_tr = $("<tr>" +
                        "<td class='hidden'>"  +judge_problems[index][index]["pk"] + "</td>" +
                        "<td>" + "判断" + "</td>" +
                         "<td>" + judge_problems[index][index]["content"].slice(0, 10) +"..."+ "</td>" +
                        "<td>" + judge_problems[index][index]["subject"] + "</td>" +
                        "<td>" + judge_problems[index][index]["chapter"] + "</td>" +
                        "<td>" + judge_problems[index][index]["knowledge_point"] + "</td>" +
                        "<td><button class='btn btn-primary btn-static-problem-detail' style='height:80%'>详细 </button></td>" +
                        "<td><button class='btn btn-primary btn-insert-test-problem' style='height:80%'> 添加到当前试卷</button></td>" +
                        "</tr>");
                    new_tr.appendTo(table);
                }

                let choice_problem = problems['choice'];
                for (let index in choice_problem) {
                    let table = $('#problem-table-body');
                    let new_tr = $("<tr>" +
                        "<td class='hidden'>"  +choice_problem[index][index]["pk"] + "</td>" +
                        "<td>" + "选择" + "</td>" +
                        "<td>" + choice_problem[index][index]["content"].slice(0, 10) +"..."+ "</td>" +
                        "<td>" + choice_problem[index][index]["subject"] + "</td>" +
                        "<td>" + choice_problem[index][index]["chapter"] + "</td>" +
                        "<td>" + choice_problem[index][index]["knowledge_point"] + "</td>" +
                        "<td><button class='btn btn-primary btn-static-problem-detail' style='height:80%'>详细 </button></td>" +
                        "<td><button class='btn btn-primary btn-insert-test-problem' style='height:80%'> 添加到当前试卷</button></td>" +
                        "</tr>");
                    new_tr.appendTo(table);
                }
                console.log(data);
            },
            error: function (msg) {
                console.log('failure');
                console.log(msg);
            }
        });
    });

    $(document).on('click', '.btn-insert-test-problem', function () {
       let table = $('#test-content-table-body');
       let new_tr = $('<tr></tr>');
       let pk = $(this).parent().parent().children("td:nth-child(1)").text();
       let old_row = $(this).parent().parent();

       let col = $("<td class='hidden'>"+pk+"</td>");
       new_tr.append(col);
       col = $("<td>"+old_row.children("td:nth-child(2)").text()+"</td>");
       new_tr.append(col);
       col = $("<td>"+old_row.children("td:nth-child(3)").text()+"</td>");
       new_tr.append(col);
       col = $("<td>"+old_row.children("td:nth-child(4)").text()+"</td>");
       new_tr.append(col);
       col = $("<td>"+old_row.children("td:nth-child(5)").text()+"</td>");
       new_tr.append(col);
       col = $("<td>"+old_row.children("td:nth-child(6)").text()+"</td>");
       new_tr.append(col);
       col = $( "<td><button  class='btn btn-primary btn-static-problem-detail' style='height:80%'>详细</button></td>");
       new_tr.append(col);
       col = $( "<td><button class='btn btn-primary btn-delete-test-problem' style='height:80%'> 从当前试卷删除 </button></td>");
       new_tr.append(col);
       new_tr.appendTo(table);
    });

    $(document).on('click', '#problem-search .btn-static-problem-detail', function () {
        let pk = $(this).parent().parent().children("td:nth-child(1)").text();
        console.log(pk);
        let type = $(this).parent().parent().children("td:nth-child(2)").text();
        console .log(type);
        if (type == '判断') {
            let url = 'problem_bank/single_problem/static/judge/'+pk+"/";
            window.open(url);
        } else {
            let url = 'problem_bank/single_problem/static/choice/'+pk+"/";
            window.open(url);
        }
    });

    $(document).on('click', '#test-content .btn-static-problem-detail', function () {
        let pk = $(this).parent().parent().children("td:nth-child(1)").text();
        console.log(pk);
        let type = $(this).parent().parent().children("td:nth-child(2)").text();
        console .log(type);

        if (type == '判断') {
            let url = 'problem_bank/single_problem/static/judge/'+pk+"/";
            window.open(url);
        } else {
            let url = 'problem_bank/single_problem/static/choice/'+pk+"/";
            window.open(url);
        }
    });

    $(document).on('click', '.btn-delete-test-problem', function () {
        console.log('hello');
       $(this).parent().parent().remove();
    });

    $('#init-auto-test').click(function () {
        initialized = auto_check();
        if (!initialized) {
            alert("请将相应的数据填完整");
            return;
        }

        cur_test.name = $("#auto-test-name").val();
        cur_test.subject = $("#auto-test-subject").val();
        cur_test.start_time = $("#auto-test-start-time").val();
        cur_test.end_time = $("#auto-test-end-time").val();
        cur_test.questions = [];
        const post_data = {};
        post_data["name"] = data_save.test.name;
        post_data["subject"] = data_save.test.subject;
        post_data["start_time"] = data_save.test.start_time;
        post_data["end_time"] = data_save.test.end_time;
        post_data["chapter"] = $("#auto-test-chapter").val();
        post_data["knowledge_point"] = $("#auto-test-knowledge-point").val();
        post_data["choice_num"] = $("#auto-test-choice-num").val();
        post_data["judge_num"] = $("#auto-test-judge-num").val();

        console.log(data_save.auto_test_add_url)

        $.ajax({
            url: data_save.auto_test_add_url,
            type: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                console.log(data);
                alert('创建成功');

            },
            error: function (msg) {
                console.log("failure");
                console.log(msg);
            }
        });
    });
    $('#init-manual-test').click(function () {

        initialized = manual_check();
        if (!initialized) {
            alert("请将相应的数据填完整");
            return;
        }

        const post_data = {};
        cur_test.name = $("#manual-test-name").val();
        cur_test.subject = $("#manual-test-subject").val();
        cur_test.start_time = $("#manual-test-start-time").val();
        cur_test.end_time = $("#manual-test-end-time").val();
        cur_test.questions = [];

        $("#test-content-table-body").find("tr").each(function(){
            let tdArr = $(this).children();
            let question = {};
            question['pk'] = tdArr.eq(0).text();
            cur_test.questions.push(question);

        });
        alert("创建成功！");
        // post_data['test'] = cur_test;
        //
        // $.ajax({
        //     url: data_save.judge_url,
        //     type: 'post',
        //     dataType: 'json',
        //     data: post_data,
        //     async: false,
        //     success: function (data) {
        //         if (data['result'] === "ok")
        //             alert('提交成功');
        //     }
        // });
    });

    $('#submit-test').click(function () {
        if (!initialized) {
            alert("请先创建相关试卷");
            return;
        }

        const post_data = {};
        post_data["name"] = data_save.test.name;
        post_data["subject"] = data_save.test.subject;
        post_data["start_time"] = data_save.test.start_time;
        post_data["end_time"] = data_save.test.end_time;
        let questions = [];
        $("#test-content-table-body").find("tr").each(function(){
            let tdArr = $(this).children();
            let question = {};
            question['type'] = tdArr.eq(1).text() == "判断"?0:1;
            question['pk'] = tdArr.eq(0).text();
            questions.push(question);

        });
        post_data["questions"] = questions;
        console.log(post_data);

        $.ajax({
            url: data_save.test_add_url,
            type: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                if (data['result'] === "ok")
                    alert('提交成功');
            }
        });
    });

});