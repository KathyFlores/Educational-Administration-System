var ClassRoomDataModelFactory = function () { };
ClassRoomDataModelFactory.prototype = new DataModelFactory(); // 实现继承
ClassRoomDataModelFactory.prototype.createView = function (t) { // 重写方法
    /* 生成TR DOM */
    let tr = document.createElement("tr");
    let checkbox = $(`<td><input type="checkbox" name="${t.room_id}" value="all"  /></td>`);
    checkbox.children("input").change(checkChange);
    tr.appendChild(checkbox[0]);
    let td = document.createElement("td");
    td.innerHTML = (t.room_id);
    tr.appendChild(td);
    let td1 = document.createElement("td");
    td1.innerHTML = (t.location);
    tr.appendChild(td1);
    let td2 = document.createElement("td");
    td2.innerHTML = (t.capacity);
    tr.appendChild(td2);
    let td3 = document.createElement("td");
    console.log(t.type);
    for (let i = 0; i < t.type.length; i++) {
        td3.innerText += `有${attachName[attachIndex[t.type[i]]]} `;
    }
    tr.appendChild(td3);
    tr.appendChild($(editBar).clone(true)[0]);
    $(tr).find(".icon-delete").click(function () {
        //console.log(checkbox[0].querySelector("input"));
        checkbox[0].querySelector("input").checked = true;
        checkChange.bind(checkbox[0].querySelector("input"))();
    });
    $(tr).find(".icon-edit").click(function () {
        initializeEdit(t);
    });
    tr.setAttribute("key", t.room_id);
    return tr;
};