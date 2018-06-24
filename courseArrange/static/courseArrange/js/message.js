var message = (function () {
    let obj = {};
    obj.createMessage = function (data, type = "success") {
        let newM = $(`<div class="message ${type}">${data}</div>`);
        $(".message-list").append(newM);
        setTimeout(() => {
            newM.fadeOut(1000, () => {
                newM.remove();
            });
        }, 3000);
    }
    let success = function (word) {
        this.createMessage(word);
    };
    let error = function (word) {
        this.createMessage(word,"error");
    };
    obj.success = success.bind(obj);
    obj.error = error.bind(obj);
    return obj;
}
)();