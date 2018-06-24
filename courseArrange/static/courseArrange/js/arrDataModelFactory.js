var arrDataModelFactory = function () { };
arrDataModelFactory.prototype = new DataModelFactory(); // 实现继承
arrDataModelFactory.prototype.createView = function (t) { // 重写方法
    /* 生成TR DOM */
    //console.log(t);
    delete t.exam_date;
    var tr = document.createElement("tr");
    let checkbox = $(`<td><input type="checkbox" name="${t.cId}" value="all"  /></td>`);
    checkbox.children("input").change(checkChange);
    tr.appendChild(checkbox[0]);
    let td = document.createElement("td");
    td.innerHTML = (t.course_id);
    tr.appendChild(td);
    let td1 = document.createElement("td");
    td1.innerHTML = (t.course_name);
    tr.appendChild(td1);
    let td2 = document.createElement("td");
    td2.innerHTML = (t.room_name);
    tr.appendChild(td2);
    let td3 = document.createElement("td");
    td3.innerHTML = (t.teacher_name);
    tr.appendChild(td3);
    let td4 = document.createElement("td");
    for (let i in t.period) {
        td4.innerText += period_const[parseInt(i) - 1];
        td4.innerText += "第";
        t.period[i].map((e) => {
            td4.innerText += e + " ";
        })
        td4.innerText += "节;";
    }
    tr.appendChild(td4);
    tr.appendChild($(editBar).clone(true)[0]);
    $(tr).find(".icon-edit").click(function () {
        editingTR = this;
        initializeEdit(t);
    });
    tr.setAttribute("key", JSON.stringify(t));
    return tr;
};