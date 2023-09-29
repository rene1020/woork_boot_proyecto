// Verificar si el usuario ya está autenticado antes de cargar la página de registro
window.addEventListener("DOMContentLoaded", function () {
  checkAuthentication();
});

document
  .getElementById("authForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    register();
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

function register() {
  const data = {
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
  };
  fetch("http://127.0.0.1:5000/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 201) {
        return response.json().then((data) => {
          document.getElementById("message").innerHTML = data.message;
          window.location.href = "login.html";
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
