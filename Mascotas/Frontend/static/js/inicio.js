document.addEventListener("DOMContentLoaded", function() {
    const sidebarMenu = document.getElementById("sidebarMenu");
    const logoutButton = document.getElementById("logoutButton");
    const menus = JSON.parse(localStorage.getItem("menus") || "[]");

    const menuMapping = {
        "Inicio": "/inicio",
        "Agregar Mascotas": "/gestion-de-mascotas",
        "Gestión de Formularios": "/gestion-de-formularios",
        "Vista de Formularios": "/vista-de-formularios",
        "Actualizar Catálogo": "/actualizar-catalogo",  
        "Ver catálogo": "/ver-catalogo"
    };

    sidebarMenu.innerHTML = '';
    sidebarMenu.appendChild(logoutButton);

    menus.forEach(menuText => {
        const menuButton = document.createElement("button");
        menuButton.textContent = menuText;
        menuButton.className = "menuButton";
        menuButton.onclick = function() {
            if (menuMapping[menuText]) {
                window.location.href = menuMapping[menuText];
            } else {
                console.error("No mapping found for: " + menuText);
            }
        };
        sidebarMenu.insertBefore(menuButton, logoutButton);
    });

    logoutButton.addEventListener('click', function(event) {
        event.preventDefault();
        fetch('/logout', {
            method: 'POST',  
            headers: {
                'Content-Type': 'application/json'  
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            window.location.href = '/'; 
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error cerrando sesión, por favor intente de nuevo.'); 
        });
    });
    
});
