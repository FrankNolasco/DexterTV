let nombres = $("#nombres");
let password = $("#password");
let perfil_url = $("#perfil_url");
let username = $("#username");
let rol_id = $("#rol_id");
let id = $("#id");
let pelicula = null;
const RowTable = (data) => `
    <div>
        <h3>${data.id} - ${data.nombres}</h3>
        <div class="password-rt">
            <img width="50px" height="50px" src="${data.perfil_url}"/>
            <span>${data.username}</span>
        </div>
    </div>
`;

function search() {
  let id = InputSearch.val();
  if (id) {
    let tbody = document.getElementById("data_searched");
    $.ajax({
      url: `http://localhost:5000/admin/buscar/usuarios/${id}`,
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
            tbody.innerHTML = "No se encontro usuario"
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
    Form.attr("action",'/admin/usuarios/modificar')
    rol_id.val(pelicula.rol_id);
    password.val(pelicula.password);
    nombres.val(pelicula.nombres);
    perfil_url.val(pelicula.perfil_url);
    username.val(pelicula.username);
    id.val(pelicula.id);
  } else {
    alert("que esta pasando acá");
  }
}

function cellsAdd() {
  Form.attr("action",'/admin/usuarios/registrar')
  limpiar();
}

function loadAdmin() {}

function limpiar() {
  InputSearch.val("");
  rol_id.val("");
  password.val("");
  nombres.val("");
  perfil_url.val("");
  username.val("");
  id.val("");
}
