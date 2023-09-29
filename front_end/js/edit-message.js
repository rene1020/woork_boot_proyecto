// http://127.0.0.1:5000/messages/
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const message_id = urlParams.get('message_id');

window.addEventListener("load", function () {
    load_message(message_id);
});

document.getElementById("authForm").addEventListener("submit", function (event) {
    event.preventDefault();
    editMessage()
});

function load_message(message_id) {
    const url = `http://127.0.0.1:5000/messages/${message_id}`;
    
    fetch(url, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (response.status === 200) {
            return response.json().then(data => {
                inputMsg = document.getElementById("message_body")
                inputMsg.value = data.message_body

                const returnButton = document.getElementById("return");
                returnButton.addEventListener("click", function() {
                    window.location.href = `../index.html`;
                });

            });
        } else {
            return response.json().then(data => {
                alert(data.error.description);
            });
        }
    })
    .catch(error => {
        alert("An error occurred.");
    });
}

function editMessage() {
    const data = {
        message_body: document.getElementById("message_body").value,
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
        if (response.status === 200) {
            return response.json().then((data) => {
            window.location.href = `../index.html`;
            });
        } else {
            return response.json().then((data) => {
            alert(data.error.description);
            });
        }
        })
        .catch((error) => {
        });
    }