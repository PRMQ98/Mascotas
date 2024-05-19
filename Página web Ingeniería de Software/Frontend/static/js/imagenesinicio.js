document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:2024/imagenesinicio')
        .then(response => response.json())
        .then(imagenes => {
            const slider = document.getElementById('INICIO');
            const puntosContainer = document.getElementById('puntos');
            let indiceImagen = 0;

            function cambiarImagenAleatoria() {
                if (slider && imagenes.length > 0) {
                    let nuevoIndice = Math.floor(Math.random() * imagenes.length);
                    while (nuevoIndice === indiceImagen) {
                        nuevoIndice = Math.floor(Math.random() * imagenes.length);
                    }

                    const img = document.createElement('img');
                    img.src = `http://localhost:2024/imagenesinicio/${imagenes[nuevoIndice]}`;
                    img.style.width = '100%';
                    img.style.opacity = 0;

                    img.addEventListener('load', () => {
                        slider.innerHTML = '';
                        slider.appendChild(img);
                        setTimeout(() => {
                            img.style.opacity = 1;
                        }, 100);

                        Array.from(puntosContainer.children).forEach((punto, index) => {
                            if (index === nuevoIndice) {
                                punto.classList.add('activo');
                            } else {
                                punto.classList.remove('activo');
                            }
                        });

                        indiceImagen = nuevoIndice;
                    });
                }
            }

            function cambiarImagenPorIndice(index) {
                if (slider && imagenes.length > 0 && index >= 0 && index < imagenes.length) {
                    const img = document.createElement('img');
                    img.src = `http://localhost:2024/imagenesinicio/${imagenes[index]}`;
                    img.style.width = '100%';
                    img.style.opacity = 0;

                    img.addEventListener('load', () => {
                        slider.innerHTML = '';
                        slider.appendChild(img);
                        setTimeout(() => {
                            img.style.opacity = 1;
                        }, 100);

                        Array.from(puntosContainer.children).forEach((punto, idx) => {
                            if (idx === index) {
                                punto.classList.add('activo');
                            } else {
                                punto.classList.remove('activo');
                            }
                        });

                        indiceImagen = index;
                    });
                }
            }

            cambiarImagenAleatoria();

            setInterval(cambiarImagenAleatoria, 6000);

            imagenes.forEach((imagen, index) => {
                const punto = document.createElement('li');
                punto.addEventListener('click', () => {
                    cambiarImagenPorIndice(index);
                });
                puntosContainer.appendChild(punto);
            });

            puntosContainer.children[indiceImagen].classList.add('activo');
        })
        .catch(error => console.error('Error al cargar las imágenes:', error));
});
