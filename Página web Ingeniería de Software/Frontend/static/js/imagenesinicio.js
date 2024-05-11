document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:2024/imagenesinicio')
        .then(response => response.json())
        .then(imagenes => {
            const slider = document.getElementById('INICIO');
            const puntosContainer = document.getElementById('puntos');
            let indiceImagen = 0;

            function cambiarImagenAleatoria() {
                if (slider && imagenes.length > 0) {
                    const nuevoIndice = Math.floor(Math.random() * imagenes.length);
                    if (nuevoIndice !== indiceImagen) {
                        const img = document.createElement('img');
                        img.src = `http://localhost:2024/imagenesinicio/${imagenes[nuevoIndice]}`;
                        img.style.width = '100%';  
                        img.style.opacity = 0;  
                        slider.innerHTML = ''; 
                        slider.appendChild(img);

                        indiceImagen = nuevoIndice;

                        setTimeout(() => {
                            img.style.opacity = 1;
                        }, 100); 
                        Array.from(puntosContainer.children).forEach((punto, index) => {
                            if (index === indiceImagen) {
                                punto.classList.add('activo');
                            } else {
                                punto.classList.remove('activo');
                            }
                        });
                    }
                }
            }

            cambiarImagenAleatoria();

            setInterval(cambiarImagenAleatoria, 6000);

            imagenes.forEach((imagen, index) => {
                const punto = document.createElement('li');
                punto.addEventListener('click', () => {
                    indiceImagen = index;
                    cambiarImagenAleatoria();
                });
                puntosContainer.appendChild(punto);
            });
        })
        .catch(error => console.error('Error al cargar las imágenes:', error));
});
