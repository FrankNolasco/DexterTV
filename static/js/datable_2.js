function activeModify(data) {
    TitleAdd.attr("class","disabled");
    TitleModify.removeAttr("class");
    dataSearched.attr("class","disabled");
    Form.removeAttr("class");
    cellsModify(data)
}

function activeCreate() {
    TitleAdd.removeAttr("class");
    TitleModify.attr("class","disabled");
    dataSearched.attr("class","disabled");
    Form.removeAttr("class");
    cellsAdd()
}


function load() {
    loadAdmin()
    document.getElementById("button").addEventListener("click", search, false);
    document.getElementById("item_nuevo").addEventListener("click", activeCreate, false);
}
  
document.addEventListener("DOMContentLoaded", load, false);

