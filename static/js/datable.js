function activeModify() {
    TitleAdd.attr("class","disabled");
    TitleModify.removeAttr("class");
    dataSearched.attr("class","disabled");
    Form.removeAttr("class");
    cellsModify()
}

function activeCreate() {
    TitleAdd.removeAttr("class");
    TitleModify.attr("class","disabled");
    dataSearched.attr("class","disabled");
    ButtonModificar.attr("disabled",true);
    Form.removeAttr("class");
    cellsAdd()
}


function load() {
    loadAdmin()
    document.getElementById("button").addEventListener("click", search, false);
    document.getElementById("item_modificar").addEventListener("click", activeModify, false);
    document.getElementById("item_nuevo").addEventListener("click", activeCreate, false);
    ButtonModificar.attr("disabled",true);
}
  
document.addEventListener("DOMContentLoaded", load, false);

