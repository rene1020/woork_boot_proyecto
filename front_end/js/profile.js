window.addEventListener('load', function () {
    getProfile();
});

document.getElementById("logout").addEventListener("click", logout);

document.getElementById("edit").addEventListener("click", edit_user);

document.getElementById("change_pass").addEventListener("click", change_pass);

document.getElementById("return").addEventListener("click", function() { window.location.href = "../index.html"; });

function getProfile() {
    const url = "http://127.0.0.1:5000/auth/profile";
    
    fetch(url, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (response.status === 200) {
            return response.json().then(data => {
                document.getElementById("username").innerText = data.username;
                get_image(data);
                document.getElementById("user_id").innerText = `#${data.user_id}`
                ;
                if (data.image)
                    new_route = data.image.replace("discord-clone-frontend", "")
                    document.getElementById("image").src = new_route.replace(/\\/g, "/")
        })
        } else {
            return response.json().then(data => {
                alert(data.error.description);
                window.location.href = "../login.html";
            });
        }
    })
    .catch(error => {
        alert("Ocurrió un error.");
    });
}

function logout() {
    const url = "http://127.0.0.1:5000/auth/logout";
    
    fetch(url, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (response.status === 200) {
            return response.json().then(data => {
                window.location.href = "login.html";
            });
        } else {
            return response.json().then(data => {
                document.getElementById("message").innerHTML = data.error.description;
            });
        }
    })
    .catch(error => {
        document.getElementById("message").innerHTML = "An error occurred.";
    });
}

function get_image(data) {
    const profilePic = document.getElementById("image");
    if (data.image) {
        profilePic.src = data.image;
    } else {
        profilePic.style.backgroundColor = "#282b31";
        profilePic.style.padding = "1px";
        profilePic.style.display = "flex";
        profilePic.style.alignItems = "center";
        profilePic.style.justifyContent = "center";
        profilePic.style.color = "white";
        profilePic.style.fontSize = "2rem";
        profilePic.alt = data.username[0].toUpperCase();
    }
}

function edit_user() {
    const userId = document.getElementById('user_id').textContent;
    window.location.href = `edit_profile.html?user_id=${userId.slice(1)}`;
}

function change_pass() {
    // const userId = document.getElementById('change_pass').textContent;
    window.location.href = `change_password.html`;
}