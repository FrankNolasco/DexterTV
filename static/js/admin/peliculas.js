let nombre = $("#nombre");
let descripcion = $("#descripcion");
let portada_url = $("#portada_url");
let fecha_hora = $("#fecha_hora");
let duracion = $("#duracion");
let video = $("#video");
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
        <span>${data.fecha_hora}</span>
        <span>${data.video}</span>
    </div>
`;

function search() {
  let id = InputSearch.val();
  if (id) {
    let tbody = document.getElementById("data_searched");
    $.ajax({
      url: `http://localhost:5000/admin/buscar/peliculas/${id}`,
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
    Form.attr("action",'/admin/peliculas/modificar')
    categoria_id.val(pelicula.categoria_id);
    descripcion.val(pelicula.descripcion);
    duracion.val(pelicula.duracion);
    fecha_hora.val(pelicula.fecha_hora);
    nombre.val(pelicula.nombre);
    portada_url.val(pelicula.portada_url);
    video.val(pelicula.video);
    id.val(pelicula.id);
  } else {
    alert("que esta pasando acá");
  }
}

function cellsAdd() {
  Form.attr("action",'/admin/peliculas/registrar')
  limpiar();
}

function loadAdmin() {}

function limpiar() {
  InputSearch.val("");
  categoria_id.val("");
  descripcion.val("");
  duracion.val("");
  fecha_hora.val("");
  nombre.val("");
  portada_url.val("");
  video.val("");
  id.val("");
}
