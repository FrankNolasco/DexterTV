let nombre = $("#nombre");
let descripcion = $("#descripcion");
let portada_url = $("#portada_url");
let trailer = $("#trailer");
let categoria_id = $("#categoria_id");
let id = $("#id");
let pelicula = null;
const RowTable = (data) => `
    <div>
        <h3>${data.id} - ${data.nombre}</h3>
        <div class="descripcion-rt">
            <img width="50px" height="50px" src="${data.portada_url}"/>
            <p>${data.descripcion}</p>
        </div>
        <span>${data.trailer}</span>
        <a href="http://localhost:5000/admin/temporadas/${data.id}">Ver temporadas</a>
    </div>
`;

function search() {
  let id = InputSearch.val();
  if (id) {
    let tbody = document.getElementById("data_searched");
    $.ajax({
      url: `http://localhost:5000/admin/buscar/series/${id}`,
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
    Form.attr("action",'/admin/series/modificar')
    categoria_id.val(pelicula.categoria_id);
    descripcion.val(pelicula.descripcion);
    nombre.val(pelicula.nombre);
    portada_url.val(pelicula.portada_url);
    trailer.val(pelicula.trailer);
    id.val(pelicula.id);
  } else {
    alert("que esta pasando acá");
  }
}

function cellsAdd() {
  Form.attr("action",'/admin/series/registrar')
  limpiar();
}

function loadAdmin() {}

function limpiar() {
  InputSearch.val("");
  categoria_id.val("");
  descripcion.val("");
  nombre.val("");
  portada_url.val("");
  trailer.val("");
  id.val("");
}
