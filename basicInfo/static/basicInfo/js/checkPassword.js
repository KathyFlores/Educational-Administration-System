/**
 * Created by Alan on 10/06/2018.
 */

var reg1 = /(^\d{6,}$)|(^[a-zA-Z]{6,}$)|(^[^a-zA-Z0-9]{6,}$)/; //数字，字母或符号其中的一种
var reg7 = /\d*\D*((\d+[a-zA-Z]+[^0-9a-zA-Z]+)|(\d+[^0-9a-zA-Z]+[a-zA-Z]+)|([a-zA-Z]+\d+[^0-9a-zA-Z]+)|([a-zA-Z]+[^0-9a-zA-Z]+\d+)|([^0-9a-zA-Z]+[a-zA-Z]+\d+)|([^0-9a-zA-Z]+\d+[a-zA-Z]+))\d*\D*/; //数字字母字符任意组合
function checkPasswordLength(value) {
    if (value.length < 6) {
        $("#pwdPrompt div:eq(1)").html("密码长度不能小于6位");
        return false;
    } else {
        $("#pwdPrompt div:eq(1)").css("display", "none");
        $("#pwdPrompt div:eq(0)").css("display", "block");
        if (reg1.test(value)) {
            $("#pwdLength span:eq(0)").css("display", "block");
            $("#pwdLength span:eq(1)").css("display", "none");
            $("#pwdLength span:eq(2)").css("display", "none");
            return true;
        }
        else if (!reg7.test(value)) {
            $("#pwdLength span:eq(0)").css("display", "none");
            $("#pwdLength span:eq(1)").css("display", "block");
            $("#pwdLength span:eq(2)").css("display", "none");
            return true;
        }
        else {
            $("#pwdLength span:eq(0)").css("display", "none");
            $("#pwdLength span:eq(1)").css("display", "none");
            $("#pwdLength span:eq(2)").css("display", "block");
            return true;
        }
        return true;
    }
}

function checkSignUp() {
    var password1=document.getElementById('password1').value.toString();
    var password2=document.getElementById('password2').value.toString();

    if(password1.length<6)
    {
        alert("密码长度不能小于6位！");
    }
    else if(!(password2===password1))
    {
        alert("两次密码输入不相等！");
    }


}










