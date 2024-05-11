document.addEventListener('DOMContentLoaded', async function() {
    const contenedor = document.getElementById('listaMascotas');
    try {
        const response = await fetch('http://localhost:2024/mascotas');
        const mascotas = await response.json();

        for (const mascota of mascotas) {
            const div = document.createElement('div');
            div.className = 'mascota';

            const imagen = new Image();
            imagen.alt = `Imagen de ${mascota.Nombre}`;
            imagen.src = mascota.FotografiaURL.startsWith('http') ? mascota.FotografiaURL : `http://localhost:2024${mascota.FotografiaURL}`;
            imagen.onload = () => div.appendChild(imagen); 

            const detalles = ['Nombre', 'Tipo', 'Raza', 'Edad', 'Estado'].map(key => {
                const p = document.createElement('p');
                p.textContent = `${key}: ${mascota[key]}`;
                return p;
            });

            detalles.forEach(detalle => div.appendChild(detalle));

            if (mascota.Estado === 'No Disponible') {
                const publicarButton = document.createElement('button');
                publicarButton.textContent = 'Publicar';
                publicarButton.addEventListener('click', async () => {
                    try {
                        const response = await fetch(`http://localhost:2024/mascotas/publicar/${mascota.MascotaID}`, { method: 'POST' });
                        const data = await response.json();
                        console.log(data.mensaje);
                        detalles.find(p => p.textContent.startsWith('Estado')).textContent = 'Estado: Disponible';
                        publicarButton.remove();
                    } catch (error) {
                        console.error('Error al publicar la mascota:', error);
                        alert('Error al publicar la mascota. Intente nuevamente.');
                    }
                });
                div.appendChild(publicarButton);
            }

            contenedor.appendChild(div);
        }
    } catch (error) {
        console.error('Error al cargar las mascotas:', error);
        alert('Error al cargar las mascotas. Intente nuevamente.');
    }
});
