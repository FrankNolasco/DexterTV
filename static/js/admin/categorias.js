let nombre = $("#nombre");
let id = $("#id");
let pelicula = null;

const RowTable = (data) => ` <h3>${data.id} - ${data.nombre}</h3> `;

function search() {
  let id = InputSearch.val();
  if (id) {
    let tbody = document.getElementById("data_searched");
    $.ajax({
      url: `http://localhost:5000/admin/buscar/categorias/${id}`,
      method: "GET",
      data: {},
      cache: false,
      dataType: "json",
      success: function (respuesta) {
        limpiar();
        pelicula = respuesta;
        if(pelicula.not_found === 0){
            ButtonModificar.removeAttr("disabled");
            tbody.innerHTML = RowTable(pelicula)
        }else{
            tbody.innerHTML = "No se encontro pelicula"
        }
        dataSearched.removeAttr("class");
        Form.attr("class", "disabled");
      },
      error: function (err) {
        tbody.innerHTML = "";
        alert("Error de servidor");
      },
    });
  } else {
    alert("No puede buscar un id vacío");
  }
}

function cellsModify() {
  if (pelicula.not_found === 0) {
    Form.attr("action",'/admin/categorias/modificar')
    nombre.val(pelicula.nombre);
    id.val(pelicula.id);
  } else {
    alert("que esta pasando acá");
  }
}

function cellsAdd() {
  Form.attr("action",'/admin/categorias/registrar')
  limpiar();
}

function loadAdmin() {}

function limpiar() {
  InputSearch.val("");
  nombre.val("");
}
