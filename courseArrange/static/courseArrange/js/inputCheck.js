String.prototype.isNull = function () {
    if (this === "") return true;
    if (this.trim() === "") return true;
}

var inputCheck = function (formRoot) {
    let flag = false;
    formRoot.children("input").map((
        (v, i, a) => {
            //console.log($(i));
            if ($(i).prev().hasClass("must") && $(i).val().isNull()) {
                message.error($(i).prev().text() + " 不能为空！");
                flag = true;
            }

            if ($(i).prev().hasClass("digit") && ($(i).val().match(/[^0-9]/) || parseInt($(i).val()) <= 0)) {
                message.error($(i).prev().text() + ' 只能为正整数');
                flag = true;
            }
        }
    ));
    return flag;
}