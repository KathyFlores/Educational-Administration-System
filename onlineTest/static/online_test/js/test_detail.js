// const data = {
//     "title": "JAD",
//     "due": "2020/01/01 00:00:00",
//     "TF_problems": [
//         {
//             "id": "1",
//             "description": "For<code>final int[] ar = new int[10];</code> we can modify the content of the array.",
//             "score": "1",
//             "choose": "T"
//         },
//         {
//             "id": "2",
//             "description": "We can use <code>array.length()</code> to get array's length.",
//             "score": "1",
//             "choose": "F"
//         },
//         {
//             "id": "3",
//             "description": "A thread object has a method called wait().",
//             "score": "1",
//             "choose": "null"
//         }
//     ],
//     "choice_problems": [
//         {
//             "id": "10",
//             "description": "Which of the following declares an array that can support three rows and a variable number of columns?",
//             "score": "2",
//             "A": "int myArray[][] = new int[][3];",
//             "B": "int myArray[][] = new int[3][];",
//             "C": "int myArray[][] = new int[][];",
//             "D": "int myArray[][] = new int[3][3];",
//             "choose": "B"
//         }
//     ]
// };

let data_save;

$(document).ready(function () {
    let i;
    let p;
    let problems = "";
    let total_score = 0;
    data_save = data;


    $("#test_title").text(data.title);
    $("#TF_list").hide();
    $("#choice_list").hide();
    $("#test_total_TF").hide();
    $("#test_total_choice").hide();


    for (i = 0; i < data.TF_problems.length; i++) {
        $("#TF_list").show();
        $("#test_total_TF").show();
        p = '<p>\
                <span class="class_label">' + Number(i + 1) + '. </span>'
            + data.TF_problems[i].description
            + '<span class="problems-score">(' + data.TF_problems[i].score + '分)</span>\
                </p>\
                <div class="problems-answer problems-tof">\
                <label>\
                    <input name="TF_problems' + data.TF_problems[i].id + '" type="radio" id="' + data.TF_problems[i].id + '_T" value="T">T</label>\
                <label>\
                    <input name="TF_problems' + data.TF_problems[i].id + '" type="radio" id="' + data.TF_problems[i].id + '_F" value="F">F</label>\
                </div>\
                <p></p>';
        problems = problems + p;
        total_score = total_score + Number(data.TF_problems[i].score);
    }
    problems = problems + '<div style="text-align: center"><button id="submit_TF" class="btn btn-primary">保存</button></div>';
    $(".TF_problems_list").html(problems);
    $("#TF_num").text(data.TF_problems.length);
    $("#TF_score").text(total_score);

    problems = "";
    total_score = 0;
    for (i = 0; i < data.choice_problems.length; i++) {
        $("#choice_list").show();
        $("#test_total_choice").show();
        p = '<p> \
                <span class="class_label">' + Number(i + 1) + '. </span>'
            + data.choice_problems[i].description
            + '<span class="problems-score">(' + data.choice_problems[i].score + '分)</span>\
                </p>\
                <div class="problems-answer problems-tof">\
                <form>\
                <label>\
                    <input name="choice_problems' + data.choice_problems[i].id + '" type="radio"  id="' + data.choice_problems[i].id + '_A" value="A">A.' + data.choice_problems[i].A + '</label>\
                <label>\
                    <input name="choice_problems' + data.choice_problems[i].id + '" type="radio"  id="' + data.choice_problems[i].id + '_B" value="B">B.' + data.choice_problems[i].B + '</label>\
                <label>\
                    <input name="choice_problems' + data.choice_problems[i].id + '" type="radio"  id="' + data.choice_problems[i].id + '_C" value="C">C.' + data.choice_problems[i].C + '</label>\
                <label>\
                    <input name="choice_problems' + data.choice_problems[i].id + '" type="radio"  id="' + data.choice_problems[i].id + '_D" value="D">D.' + data.choice_problems[i].D + '</label>\
                </form>\
                </div>\
                <p></p>';
        problems = problems + p;
        total_score = total_score + Number(data.choice_problems[i].score);
    }
    problems = problems + '<div style="text-align: center"><button id="submit_choice" class="btn btn-primary">保存</button></div>';
    $(".choice_problems_list").html(problems);
    $("#choice_num").text(data.choice_problems.length);
    $("#choice_score").text(total_score);

    let static_table = "<div>判断题</div>";
    for (i = 0; i < data.TF_problems.length; i++) {
        if (data.TF_problems[i].choose != "None") {
            $("#" + data.TF_problems[i].id + "_" + data.TF_problems[i].choose).attr("checked", "checked");
            static_table = static_table + '<button class="btn btn-danger" style="cursor: default">' + Number(i + 1) + '</button>&nbsp';
        }
        else {
            static_table = static_table + '<button class="btn btn-primary" style="cursor: default">' + Number(i + 1) + '</button>&nbsp';
        }
    }

    static_table = static_table + "<hr><div>选择题</div>";
    for (i = 0; i < data.choice_problems.length; i++) {
        if (data.choice_problems[i].choose != 'None') {
            $("#" + data.choice_problems[i].id + "_" + data.choice_problems[i].choose).attr("checked", "checked");
            static_table = static_table + '<button class="btn btn-danger" style="cursor: default">' + Number(i + 1) + '</button>&nbsp';
        }
        else {
            static_table = static_table + '<button class="btn btn-primary" style="cursor: default">' + Number(i + 1) + '</button>&nbsp';
        }
    }

    $(".statics").html(static_table);

});

$(function () {
    show_time();
});

function show_time() {
    const time_start = new Date().getTime();
    const time_end = new Date(data_save.due).getTime();
    let time_distance = time_end - time_start;
    if (time_distance > 0) {
        let int_day = Math.floor(time_distance / 86400000);
        time_distance -= int_day * 86400000;
        let int_hour = Math.floor(time_distance / 3600000);
        time_distance -= int_hour * 3600000;
        let int_minute = Math.floor(time_distance / 60000);
        time_distance -= int_minute * 60000;
        let int_second = Math.floor(time_distance / 1000);
        if (int_day < 10) {
            int_day = "0" + int_day;
        }
        if (int_hour < 10) {
            int_hour = "0" + int_hour;
        }
        if (int_minute < 10) {
            int_minute = "0" + int_minute;
        }
        if (int_second < 10) {
            int_second = "0" + int_second;
        }
        $("#time_left").text("" + int_day + " 天 " + int_hour + " 时 " + int_minute + " 分 " + int_second + " 秒 ");
    }
    else {
        $("#time_left").text("已结束");
    }
    setTimeout("show_time()", 1000);
}

$(document).ready(function () {
    $('#submit_TF').click(function () {

        var time_start = new Date().getTime();
        var time_end = new Date(data_save.due).getTime();

        if(time_end < time_start){
            alert("无法提交：测试已结束");
            return;
        }

        const post_data = {};
        post_data["test_id"] = data_save.test_id;
        post_data["type"] = "true_or_false";

        for (let i = 0; i < data_save.TF_problems.length; i++) {
            post_data[data_save.TF_problems[i].id] = $("input[name='TF_problems" + data_save.TF_problems[i].id + "']:checked").val();
        }

        $.ajax({
            url: data_save.judge_url,
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
    $('#submit_choice').click(function () {
        const post_data = {};
        post_data["test_id"] = data_save.test_id;
        post_data["type"] = "choice";

        for (let i = 0; i < data_save.choice_problems.length; i++) {
            post_data[data_save.choice_problems[i].id] = $("input[name='choice_problems" + data_save.choice_problems[i].id + "']:checked").val();
        }
        $.ajax({
            url: data_save.judge_url,
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
