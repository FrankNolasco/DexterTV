let nombre = $("#nombre");
let descripcion = $("#descripcion");
let video = $("#video");
let duracion = $("#duracion");
let temporada_id = $("#temporada_id");
let portada_url = $("#portada_url");
let id = $("#id");
let pelicula = null;
const RowTable = (data) => `
    <div>
        <h3>${data.id} - ${data.nombre}</h3>
        <div class="descripcion-rt">
            <img src=${data.portada_url} alt="..."/>
            <p>${data.descripcion}</p>
        </div>
        <span>${data.video}</span>
        <span>${data.duracion}</span>
        <button class="menu-inline__item" id="button_modify_${data.id}">
            MODIFICAR
        </button>
    </div>
`;

function search() {
  let id = InputSearch.val();
  if (id) {
    let tbody = document.getElementById("data_searched");
    $.ajax({
      url: `http://localhost:5000/admin/buscar/episodios/${id}`,
      method: "GET",
      data: {},
      cache: false,
      dataType: "json",
      success: function (respuesta) {
        limpiar();

        if (respuesta.not_found === 0) {
          // ButtonModificar.removeAttr("disabled");
          let __inner = "";
          let xd = JSON.parse(respuesta.data);
          Array.isArray(xd) &&
            xd.forEach((element) => {
              __inner += RowTable(element);
            });
          tbody.innerHTML = __inner;
          Array.isArray(xd) &&
            xd.forEach((element) => {
              let btn = document.getElementById(`button_modify_${element.id}`);
              btn.addEventListener(
                "click",
                function () {
                  activeModify(element);
                },
                false
              );
            });
        } else {
          tbody.innerHTML = "No se encontro pelicula";
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

function cellsModify(data) {
  if (data) {
    Form.attr("action", "/admin/episodios/modificar");
    temporada_id.val(data.temporada_id);
    descripcion.val(data.descripcion);
    nombre.val(data.nombre);
    duracion.val(data.duracion);
    video.val(data.video);
    portada_url.val(data.portada_url);
    id.val(data.id);
  } else {
    alert("que esta pasando acá");
  }
}

function cellsAdd() {
  Form.attr("action", "/admin/episodios/registrar");
  limpiar();
}

function loadAdmin() {
  search();
}

function limpiar() {
  descripcion.val("");
  nombre.val("");
  video.val("");
  portada_url.val("");
  duracion.val("");
  id.val("");
}
