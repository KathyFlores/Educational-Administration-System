
let data_save;
$(document).ready(function () {
    data_save = data;
    $('#btn-search-problem').click(function () {
        const post_data = {};
        post_data["type"] = 0;


        $.ajax({
            url: data_save.problem_search_url,
            method: 'post',
            dataType: 'json',
            data: post_data,
            async: false,
            success: function (data) {
                if (data['result'] === "ok")
                    alert('提交成功');
                console.log(data);
            },
            error: function (msg) {
                console.log(msg);
            }
        });
    });
    $('#btn-single-problem-nav').click(function () {
        window.location.href = data_save.problem_detail_url;
    });
    $('.btn-problem-detail').click(function () {
        window.location.href = data_save.problem_detail_url;
    });
    $('#btn-update-problem').click(function () {
        const post_data = {};
        post_data["test_id"] = $('#type').val();
        post_data["content"] = $('#content').val();
        post_data["solution"] = $("#solution").val();
        post_data["subject"] = $("#subject").val();
        post_data["chapter"] = $("#chapter").val();
        post_data["knowledge_point"] = $("#knowledge_point").val();
        post_data["add_time"] = $("#add_time").val();
        post_data["latest_modify_time"] = $("#latest_modify_time").val();
        post_data["type"] = $("#type").val();


        $.ajax({
            url: data_save.problem_add_url,
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
        }).done(function(data) {
            Observable.fire(data);
        });
    });
});

Observable.add(function() {
  //pocessData
  data['problemCount'] = data['count'];
})

Observable.add(function() {
  $('problemHolder1').html(data['problems'][1]);
  $('problemHolder2').html(data['problems'][2]);
  $('problemHolder3').html(data['problems'][3]);
})
