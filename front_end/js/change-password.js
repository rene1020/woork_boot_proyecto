document.getElementById("authForm").addEventListener("submit", function (event) {
    event.preventDefault();
    change_pass()
});


function change_pass() {
    let old_password = document.getElementById("current_password").value
    let new_password = document.getElementById("new_password").value
    let confirm_password = document.getElementById("confirm_new_password").value

    if (new_password == confirm_password) {
        const data = {
            old_password: old_password,
            new_password: new_password
        }
        const url = `http://127.0.0.1:5000/auth/profile/edit_password`;
    
            fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            credentials: 'include'
        })
        .then(response => {
            if (response.status === 200) {
                return response.json().then(data => {
                    alert(data.message)
                    window.location.href = "profile.html";
            })
            } else {
                return response.json().then(data => {
                    alert(data.error.description);
                });
            }
        })
        .catch(error => {
            alert("Ocurrió un error.");
        });
    }
    else {
        alert("Debes confirmar tu nueva contraseña");
    }
    };