function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }

  function delete_cookie(cname) {
    document.cookie = cname +'=; Expires=Thu, 01 Jan 1970 00:00:01 GMT; Path=/;';
    window.location.href="http://fcv.onecloud.cl:8080/login";
  }
  function cerrar_sesion() {
    cleanCookieByName("uid");
    cleanCookieByName("rol_id");
    deleteCookies();
    window.location.href="http://fcv.onecloud.cl:8080/login";
  }

  function cleanCookieByName(cname) {
    document.cookie = cname +'=; Expires=Thu, 01 Jan 1970 00:00:01 GMT; Path=/;';
  }

  function deleteCookies() {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      var eqPos = cookie.indexOf("=");
      var nombre = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
      nombre = nombre.trim();
      document.cookie = nombre + "=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;";
    }
  }

function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function initial(){
  loadMenuByRol();
  getUserName();
  checkCookie();
}

function checkCookie() {
  loadMenuByRol();
  getUserName();
  let user = getCookie("uid");
  console.log("user id:" + user);
  if (user != "") {
      showAndHide();
  } else {
      window.location.href="http://fcv.onecloud.cl:8080/login";
  }
}

function showAndHide() {
  
  var x = document.getElementById("contenido");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function loadMenuByRol() {
  let main = document.getElementById("main_menu");
  let cli = document.getElementById("mod_clinicas");
  let vet = document.getElementById("mod_veterinarios");
  let tut = document.getElementById("mod_tutores");
  let pac = document.getElementById("mod_pacientes");
  let att = document.getElementById("mod_atenciones");
  let vac = document.getElementById("mod_vacunaciones");
  let vacs = document.getElementById("mod_vacunas");
  let rec = document.getElementById("mod_recetas");
  let t_age = document.getElementById("tit_agenda");
  let age = document.getElementById("mod_agenda");
  let t_esp = document.getElementById("tit_especies");
  let esp = document.getElementById("mod_especies");
  let raz = document.getElementById("mod_razas");
  let t_usr = document.getElementById("tit_usuarios");
  let usr = document.getElementById("mod_usuarios");

  let rol = getCookie("rol_id");
  switch (rol) {
    case "1": //super admin
      // cli.style.display = "initial";
      // vet.style.display = "initial";
      // tut.style.display = "initial";
      // pac.style.display = "initial";
      // att.style.display = "initial";
      // vac.style.display = "initial";
      // vacs.style.display = "initial";
      // rec.style.display = "initial";
      // t_age.style.display = "initial";
      // age.style.display = "initial";
      // t_esp.style.display = "initial";
      // esp.style.display = "initial";
      // raz.style.display = "initial";
      // t_usr.style.display = "initial";
      // usr.style.display = "initial";
      break;
    case "2": // admin clinica
      cli.style.display = "none";
      break;
    case "3": // veterinario
      cli.style.display = "none";
      vet.style.display = "none";
      tut.style.display = "none";
      t_usr.style.display = "none";
      usr.style.display = "none";
      break;
    case "4":  // recepcionista
      cli.style.display = "none";
      vet.style.display = "none";
      att.style.display = "none";
      vac.style.display = "none";
      vacs.style.display = "none";
      rec.style.display = "none";
      t_usr.style.display = "none";
      usr.style.display = "none";
      break;
    default:
      cli.style.display = "none";
      vet.style.display = "none";
      tut.style.display = "none";
      pac.style.display = "none";
      att.style.display = "none";
      vac.style.display = "none";
      vacs.style.display = "none";
      rec.style.display = "none";
      t_age.style.display = "none";
      age.style.display = "none";
      t_esp.style.display = "none";
      esp.style.display = "none";
      raz.style.display = "none";
      t_usr.style.display = "none";
      usr.style.display = "none";
      break;
  };
}


function getUserName() { 
  let nombre = getCookie("pnombre");
  let apellido = getCookie("appaterno");
  let clinica = getCookie("clinica");
  var e = document.getElementById("user_name");
  e.textContent = nombre + " " + apellido;

  var idRol = getCookie("rol_id");
  var c = document.getElementById("nombre_clinica");
  if (idRol != 1) { 
    c.textContent = clinica;
  } else {
    c.textContent = "SuperAdmin";
  }
}

function vetListFilter() {
  let idClinica = getCookie("id_clinica");
}