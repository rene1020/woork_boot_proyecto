// Esto se ejecuta al cargar la pagina
window.addEventListener("load", function () {
  getProfileName();
  load_user_servers();
});

if (document.getElementById("cancel-btn")) {
  document.getElementById("cancel-btn").addEventListener("click", function () {
    window.location.href = "../index.html";
  });
}

function newServerForm() {
  window.location.href = "../pages/create_server.html";
}

function goToProfile() {
  window.location.href = "../pages/profile.html";
}

function goToLogin() {
  window.location.href = "../pages/login.html";
}

function goSearch() {
  window.location.href = "../pages/search_servers.html";
}

if (document.getElementById("authForm")) {
  document
    .getElementById("authForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      createServer();
    });
}

function createServer() {
  const data = {
    server_name: document.getElementById("server_name").value,
    server_description: document.getElementById("server_description").value,
  };
  fetch("http://127.0.0.1:5000/server", {
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
          window.location.href = "../index.html";
        });
      } else {
        return response.json().then((data) => {
          if (errorData.error) {
            document.getElementById("message").innerHTML =
              data.error.description;
          }
        });
      }
    })
    .catch((error) => {
      document.getElementById("message").innerHTML = "Ocurrio un error";
    });
}

function getProfileName() {
  const url = "http://127.0.0.1:5000/auth/profile";

  fetch(url, {
    method: "GET",
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json().then((data) => {
          document.getElementById("profile-card").innerText = data.username;
        });
      } else {
        // Redirige al usuario a la página de inicio de sesión en caso de error
        window.location.href = "../pages/login.html";
      }
    })
    .catch((error) => {
      document.getElementById("message").innerHTML = "Ocurrió un error.";
    });
}

function load_user_servers() {
  if (window.location.pathname === "/index.html") {
    fetch("http://127.0.0.1:5000/users/servers", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    })
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          throw new Error("Server responded with an error status.");
        }
      })
      .then((data) => {
        const serverList = document.getElementById("server-list");

        if (data.servers.length === 0) {
          // Si el usuario no se ha unido a ningún servidor, muestra un mensaje
          const noServersMessage = document.createElement("div");
          noServersMessage.textContent = "Aún no te has unido a un servidor";
          noServersMessage.classList.add("no-servers-message");
          document.body.appendChild(noServersMessage);

          // Puedes agregar instrucciones adicionales para buscar o crear servidores aquí
          const instructionsMessage = document.createElement("div");
          instructionsMessage.textContent =
            "Intenta buscar uno o crea uno propio.";
          instructionsMessage.classList.add("instructions-message");
          document.body.appendChild(instructionsMessage);
        } else {
          data.servers.forEach((server) => {
            const serverDiv = document.createElement("div");
            serverDiv.classList.add("svr");

            const uServerDiv = document.createElement("div");
            uServerDiv.classList.add("u-server");

            const IconImg = document.createElement("img");
            IconImg.src = "../img/server.png";
            IconImg.id = "search-icon";

            const serverNameP = document.createElement("div");
            serverNameP.classList.add("svr-name");
            serverNameP.textContent = server.server_name;

            // Agrega un evento de clic al div
            serverDiv.addEventListener("click", function () {
              const server_id = server.server_id;
              cleanScreen();
              // Llama a otra función y pasa el server_id
              get_channels(server_id);
            });

            uServerDiv.appendChild(IconImg);
            serverDiv.appendChild(uServerDiv);
            serverDiv.appendChild(serverNameP);

            serverList.appendChild(serverDiv);
          });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        document.getElementById("message").innerHTML = "Ocurrió un error";
      });
  }
}

function get_channels(server_id) {
  const channelListDiv = document.createElement("div");
  channelListDiv.id = "channel-list";

  const addChannelDiv = document.createElement("div");
  addChannelDiv.id = "add-channel";

  const addButton = document.createElement("button");
  addButton.id = "btn-new-channel";
  addButton.textContent = "Agregar Canal";

  addButton.addEventListener("click", function () {
    newChannelForm(server_id);
  });

  addChannelDiv.appendChild(addButton);

  document.body.appendChild(channelListDiv);
  document.body.appendChild(addChannelDiv);

  get_channels_in_server(server_id);
}

function get_channels_in_server(server_id) {
  const url = `http://127.0.0.1:5000/tchannels?server_id=${server_id}`;

  fetch(url, {
    method: "GET",
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json().then((data) => {
          const channelListDiv = document.getElementById("channel-list");
          channelListDiv.innerHTML = "";

          if (data.channels && data.channels.length > 0) {
            data.channels.forEach((channel) => {
              const channelDiv = document.createElement("div");
              channelDiv.classList.add("channel");

              const channelNameP = document.createElement("p");
              channelNameP.classList.add("channel_name");
              channelNameP.textContent = `# ${channel.channel_name}`;

              // Agregar un evento click para cambiar el estado activo del canal
              channelDiv.addEventListener("click", function () {
                cleanChatbox();
                open_channel_chatbox(channel.channel_id);

                // Quitar la clase 'active' de todos los canales
                const allChannels = document.querySelectorAll(".channel");
                allChannels.forEach((ch) => {
                  ch.classList.remove("active");
                });

                // Agregar la clase 'active' al canal actual
                channelDiv.classList.add("active");
              });

              channelDiv.appendChild(channelNameP);
              channelListDiv.appendChild(channelDiv);
            });
          } else {
            // Si no hay canales, muestra un mensaje
            const noChannelsMessage = document.createElement("p");
            noChannelsMessage.textContent = "No hay canales";
            noChannelsMessage.classList.add("no-channels-message"); // Agrega la clase CSS
            channelListDiv.appendChild(noChannelsMessage);
          }
        });
      } else {
        // Manejo de error específico para cuando la solicitud no sea exitosa
        throw new Error("No se pudo obtener la lista de canales.");
      }
    })
    .catch((error) => {
      // Muestra el mensaje de error en la consola para depuración
      console.error(error);

      // Ahora, en lugar de mostrar el mensaje de error genérico, puedes realizar un manejo específico para el caso en que no haya canales.
      const channelListDiv = document.getElementById("channel-list");
      channelListDiv.innerHTML = "";

      const noChannelsMessage = document.createElement("p");
      noChannelsMessage.textContent = "No hay canales";
      noChannelsMessage.classList.add("no-channels-message"); // Agrega la clase CSS
      channelListDiv.appendChild(noChannelsMessage);
    });
}

function newChannelForm(server_id) {
  // Crear el div principal con clase "create-channel-screen"
  const createChannelScreenDiv = document.createElement("div");
  createChannelScreenDiv.classList.add("create-channel-screen");

  // Crear el div con clase "container"
  const containerDiv = document.createElement("div");
  containerDiv.classList.add("container");

  // Crear el título h1 con id "title"
  const titleH1 = document.createElement("h1");
  titleH1.id = "title";
  titleH1.textContent = "Nuevo Canal";

  // Crear el formulario con id "authForm"
  const form = document.createElement("form");
  form.id = "authForm";

  // Crear el div con clase "form-field"
  const formFieldDiv = document.createElement("div");
  formFieldDiv.classList.add("form-field");

  // Crear la etiqueta "label"
  const label = document.createElement("label");
  label.setAttribute("for", "channel_name");
  label.textContent = "Nombre:";

  // Crear el input con clase "input-box" y los atributos necesarios
  const input = document.createElement("input");
  input.classList.add("input-box");
  input.setAttribute("type", "text");
  input.setAttribute("name", "channel_name");
  input.setAttribute("id", "channel_name");
  input.setAttribute("required", true);

  // Crear el botón "Crear" con tipo "submit" y id "auth-btn"
  const submitButton = document.createElement("button");
  submitButton.setAttribute("type", "submit");
  submitButton.id = "auth-btn";
  submitButton.textContent = "Crear";

  // Crear el botón "Cancelar" con id "cancel-btn"
  const cancelButton = document.createElement("button");
  cancelButton.id = "cancel-btn";
  cancelButton.textContent = "Cancelar";

  // Agregar eventos de clic a los botones
  submitButton.addEventListener("click", onCrearButtonClick);
  cancelButton.addEventListener("click", onCancelarButtonClick);

  // Función que se ejecuta cuando se hace clic en el botón "Crear"
  function onCrearButtonClick(event) {
    event.preventDefault(); // Evita que el formulario se envíe si está dentro de un formulario
    // Agrega aquí el código que deseas ejecutar cuando se hace clic en "Crear"
    createChannel(server_id);
  }

  // Función que se ejecuta cuando se hace clic en el botón "Cancelar"
  function onCancelarButtonClick() {
    // Agrega aquí el código que deseas ejecutar cuando se hace clic en "Cancelar"
    window.location.href = "../index.html";
  }

  // Crear el div con id "message"
  const messageDiv = document.createElement("div");
  messageDiv.id = "message";

  // Agregar los elementos al formulario y al div principal
  formFieldDiv.appendChild(label);
  formFieldDiv.appendChild(input);
  form.appendChild(formFieldDiv);
  form.appendChild(submitButton);
  form.appendChild(cancelButton);
  containerDiv.appendChild(titleH1);
  containerDiv.appendChild(form);
  containerDiv.appendChild(messageDiv);
  createChannelScreenDiv.appendChild(containerDiv);

  // Insertar el div principal en el body
  document.body.appendChild(createChannelScreenDiv);
}

function createChannel(server_id) {
  const data = {
    channel_name: document.getElementById("channel_name").value,
    server_id: server_id,
  };
  fetch("http://127.0.0.1:5000/tchannels", {
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
          alert(data.message);
          window.location.href = "../index.html";
        });
      } else {
        return response.json().then((data) => {
          alert(data.error.description);
        });
      }
    })
    .catch((error) => {
      alert("Ocurrio un error");
    });
}

function open_channel_chatbox(channel_id) {
  // Crear el contenedor principal con clase "chat-container"
  const chatContainerDiv = document.createElement("div");
  chatContainerDiv.classList.add("chat-container");

  // Crear el cuadro de chat con clase "chat-box" y id "chatBox"
  const chatBoxDiv = document.createElement("div");
  chatBoxDiv.classList.add("chat-box");
  chatBoxDiv.id = "chatBox";

  // Crear el campo de entrada de texto con tipo "text" y id "messageInput" con un atributo de marcador de posición (placeholder)
  const messageInput = document.createElement("input");
  messageInput.setAttribute("type", "text");
  messageInput.id = "messageInput";
  messageInput.setAttribute("placeholder", "Escribe un mensaje...");

  // Crear el botón con id "sendBtn" y texto "Enviar" y agregar un evento de clic
  const sendButton = document.createElement("button");
  sendButton.id = "sendBtn";
  sendButton.textContent = "Enviar";
  sendButton.addEventListener("click", sendMessage);

  function sendMessage() {
    const inputField = document.getElementById("messageInput");
    const message = inputField.value.trim();

    // Get the user's username from the profile
    const username = document.getElementById("profile-card").innerText;

    const data = {
      message_body: message,
      channel_id: channel_id,
    };

    fetch("http://127.0.0.1:5000/messages", {
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
            cleanChatbox();
            open_channel_chatbox(channel_id);
            messageInput.value = ""; // Clear the input field
          });
        } else {
          return response.json().then((data) => {
            alert(data.error.name);
          });
        }
      })
      .catch((error) => {
        console.error("Error al enviar el mensaje:", error);
        alert("Ocurrió un error al enviar el mensaje");
      });
  }

  // Agregar todos los elementos al contenedor principal
  chatContainerDiv.appendChild(chatBoxDiv);
  chatContainerDiv.appendChild(messageInput);
  chatContainerDiv.appendChild(sendButton);

  // Insertar el contenedor principal en el cuerpo (body) del documento
  document.body.appendChild(chatContainerDiv);

  // Cargar los mensajes del canal correspondiente
  load_channel_messages(channel_id);
}

function addMessage(username, message, date, message_id, channel_id) {
  const ch = channel_id;
  const fDate = new Date(date);
  const chatBox = document.getElementById("chatBox");
  const newMessage = document.createElement("div");
  newMessage.classList.add("message");

  const headerDiv = document.createElement("div");
  headerDiv.classList.add("header");

  const usernamePara = document.createElement("p");
  usernamePara.innerHTML = `<strong>${username}</strong>`;

  const datePara = document.createElement("p");
  datePara.innerHTML = `<strong>${fDate.getDate()}/${
    fDate.getMonth() + 1
  }/${fDate.getFullYear()} ${
    fDate.getHours() + 3
  }:${fDate.getMinutes()}</strong>`;

  headerDiv.appendChild(usernamePara);
  headerDiv.appendChild(datePara);

  const messageContent = document.createElement("p");
  messageContent.innerHTML = `${message}`;
  messageContent.classList.add("content");

  const editButton = document.createElement("button");
  editButton.textContent = "Editar";
  editButton.classList.add("edit-button");
  editButton.addEventListener("click", function () {
    window.location.href = `../pages/edit_message.html?message_id=${message_id}`;
  });

  const deleteButton = document.createElement("button");
  deleteButton.textContent = "Eliminar";
  deleteButton.classList.add("delete-button");
  deleteButton.addEventListener("click", function () {
    let msg_id = message_id;
    deleteMessage(msg_id);
    const parentElement = deleteButton.parentNode.parentNode;
    parentElement.remove();
  });

  const actionsDiv = document.createElement("div");
  actionsDiv.classList.add("actions");
  actionsDiv.appendChild(editButton);
  actionsDiv.appendChild(deleteButton);

  newMessage.appendChild(headerDiv);
  newMessage.appendChild(messageContent);
  newMessage.appendChild(actionsDiv);

  chatBox.appendChild(newMessage);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function deleteMessage(message_id) {
  fetch(`http://127.0.0.1:5000/messages/${message_id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 204) {
        return response.json().then((data) => {
          alert("Mensaje Editado");
        });
      } else {
        return response.json().then((data) => {
          alert(data.error.description);
        });
      }
    })
    .catch((error) => {
      // cleanChatbox()
    });
}

function editMessage(message_id) {
  const data = {
    message: document.getElementById("new_message").value,
  };
  fetch(`http://127.0.0.1:5000/messages/${message_id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 204) {
        return response.json().then((data) => {
          alert("Mensaje editado");
        });
      } else {
        return response.json().then((data) => {
          alert(data.error.description);
        });
      }
    })
    .catch((error) => {});
}

function cleanScreen() {
  // Eliminar el div con ID "channel-list" si existe
  const channelListDiv = document.getElementById("channel-list");
  if (channelListDiv) {
    channelListDiv.parentNode.removeChild(channelListDiv);
  }

  // Eliminar el div con ID "add-channel" si existe
  const addChannelDiv = document.getElementById("add-channel");
  if (addChannelDiv) {
    addChannelDiv.parentNode.removeChild(addChannelDiv);
  }

  // Eliminar todos los elementos con la clase "chat-container" y sus hijos
  const chatContainers = document.querySelectorAll(".chat-container");
  chatContainers.forEach(function (container) {
    container.parentNode.removeChild(container);
  });
}

function cleanChatbox() {
  // Eliminar todos los elementos con la clase "chat-container" y sus hijos
  const chatContainers = document.querySelectorAll(".chat-container");
  chatContainers.forEach(function (container) {
    container.parentNode.removeChild(container);
  });
}

function load_channel_messages(channel_id) {
  fetch(`http://127.0.0.1:5000/messages?channel_id=${channel_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json().then((data) => {
          if (data.messages != {}) {
            const messages = data.messages; // Supongamos que los mensajes están en data.messages
            const chatBox = document.getElementById("chatBox");

            // Limpia el chatbox antes de agregar los mensajes
            chatBox.innerHTML = "";

            // Agrega cada mensaje al chatbox usando la función addMessage
            messages.forEach((message) => {
              addMessage(
                message.username,
                message.message_body,
                message.creation_date,
                message.message_id,
                channel_id
              );
            });
          } else {
          }
        });
      } else {
        return response.json().then((data) => {
          if (errorData.error) {
            alert(data.error.description);
          }
        });
      }
    })
    .catch((error) => {
      
    });
}

