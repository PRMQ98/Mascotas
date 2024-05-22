document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:2024/mascotas/adoptadas')
        .then(response => response.json())
        .then(mascotas => {
            const contenedor = document.getElementById('listaMascotasAdoptadas');
            mascotas.forEach(mascota => {
                const div = document.createElement('div');
                div.className = 'mascota';

                const imageUrl = mascota.FotografiaURL.startsWith('http') ? mascota.FotografiaURL : `http://localhost:2024/mascotasimages/${mascota.FotografiaURL}`;

                const detalles = `
                    <h2>${mascota.Nombre}</h2>
                    <p><strong>Tipo:</strong> ${mascota.Tipo}</p>
                    <p><strong>Raza:</strong> ${mascota.Raza}</p>
                    <p><strong>Edad (meses):</strong> ${mascota.Edad}</p>
                    <p><strong>Adoptante:</strong> ${mascota.Nombres} ${mascota.Apellidos}</p>
                    <p><strong>Correo:</strong> ${mascota.CorreoElectronico}</p>
                    <p><strong>Teléfono:</strong> ${mascota.NumeroTelefono}</p>
                    <img src="${imageUrl}" alt="Imagen de ${mascota.Nombre}" style="width:100%; max-height:300px;">
                    <button onclick="verPDF(${mascota.MascotaID})">Ver</button>
                `;
                div.innerHTML = detalles;
                contenedor.appendChild(div);
            });
        })
        .catch(error => console.error('Error al cargar las mascotas adoptadas:', error));
});

function verPDF(mascotaId) {
    window.open(`http://localhost:2024/descargar_pdf_mascota/${mascotaId}`, '_blank');
}
