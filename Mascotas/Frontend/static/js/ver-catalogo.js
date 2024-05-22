document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:2024/mascotas/disponibles')
        .then(response => response.json())
        .then(mascotas => {
            const contenedor = document.getElementById('listaMascotas');
            mascotas.forEach(mascota => {
                const div = document.createElement('div');
                div.className = 'mascota';

                const imagen = document.createElement('img');
                imagen.alt = `Imagen de ${mascota.Nombre}`;
                imagen.src = mascota.FotografiaURL.startsWith('http') ? mascota.FotografiaURL : `http://localhost:2024/mascotasimages/${mascota.FotografiaURL}`;
                div.appendChild(imagen);

                const nombre = document.createElement('h2');
                nombre.textContent = mascota.Nombre;
                div.appendChild(nombre);

                const tipo = document.createElement('p');
                tipo.textContent = `Tipo: ${mascota.Tipo}`;
                div.appendChild(tipo);

                const raza = document.createElement('p');
                raza.textContent = `Raza: ${mascota.Raza}`;
                div.appendChild(raza);

                const edad = document.createElement('p');
                edad.textContent = `Edad: ${mascota.Edad}`;
                div.appendChild(edad);

                const adoptarButton = document.createElement('button');
                adoptarButton.textContent = 'Adoptar';
                adoptarButton.addEventListener('click', function() {
                    const usuarioId = localStorage.getItem('UsuarioID');
                    fetch(`http://localhost:2024/mascotas/adoptar/${mascota.MascotaID}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ usuarioId: usuarioId })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.mensaje);
                        alert("Mascota adoptada exitosamente!");
                        div.remove();
                    })
                    .catch(error => console.error('Error al adoptar la mascota:', error));
                });
                div.appendChild(adoptarButton);

                contenedor.appendChild(div);
            });
        })
        .catch(error => console.error('Error al cargar las mascotas:', error));
});
