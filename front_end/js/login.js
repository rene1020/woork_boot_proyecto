// Verificar si el usuario ya está autenticado antes de cargar la página de inicio de sesión
window.addEventListener("DOMContentLoaded", function () {
  checkAuthentication();
});

document
  .getElementById("authForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    login();
  });

function checkAuthentication() {
  fetch("http://127.0.0.1:5000/auth/profile", {
    method: "GET",
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 200) {
        // El usuario ya está autenticado, redirige a la página de perfil
        window.location.href = "profile.html";
      }
    })
    .catch((error) => {
      // Error al verificar la autenticación
      console.error(error);
    });
}

function login() {
  const data = {
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
  };
  fetch("http://127.0.0.1:5000/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json().then((data) => {
          window.location.href = "profile.html";
        });
      } else {
        return response.json().then((data) => {
          if (data.error) {
            document.getElementById("message").innerHTML =
              data.error.description;
          }
        });
      }
    })
    .catch((error) => {
      document.getElementById("message").innerHTML = "Ocurrió un error";
    });
}
