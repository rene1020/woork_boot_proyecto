// Esto se ejecuta al cargar la pagina
window.addEventListener("load", function () {
    let queryString = window.location.search;
    let urlParams = new URLSearchParams(queryString);
    let serverName = urlParams.get('server_name');
    let serverId = urlParams.get('server_id');

    invitation(serverName, serverId)
    // alert(`Nombre: ${serverName} . Id: ${serverId}`)
});

function invitation(name, id) {
    const serverTitle = document.getElementById("title");
    serverTitle.textContent = name

    const returnBtn = document.getElementById("return");
    returnBtn.addEventListener("click", () => {
        window.location.href = `../index.html`;
    })

    const joinBtn = document.getElementById("join");
    joinBtn.addEventListener("click", () => {
        fetch(`http://127.0.0.1:5000/users/join?server_id=${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
            })
            .then(response => {
                if (response.status === 201) {
                    return response.json().then(data => {
                        alert(`Te has unido al servidor ${name}`);
                        window.location.href = "../index.html";
                    });
                } else {
                    return response.json().then(data => {
                        if (data.error) {
                            data.error.description;
                        }
                    })
                }
            })
            .catch(error => {
                document.getElementById("message").innerHTML = "Ocurrio un error";
            });
        });

}