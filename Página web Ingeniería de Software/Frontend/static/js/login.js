document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const dpi = document.getElementById("dpi").value;

    fetch('http://localhost:2024/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: email, password: dpi }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loginMessage").innerText = data.message;
        if (data.user) {
            localStorage.setItem('UsuarioID', data.user.UsuarioID); 
            localStorage.setItem("menus", JSON.stringify(data.menus));
            window.location.href = "/inicio"; 
        }
    })
    
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById("loginMessage").innerText = 'Error al intentar iniciar sesión.';
    });
});
