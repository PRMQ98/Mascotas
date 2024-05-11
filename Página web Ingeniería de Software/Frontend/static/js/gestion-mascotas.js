document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('formMascota');
    form.addEventListener('submit', function(event) {
        event.preventDefault();  
        const formData = new FormData(form);
        fetch('http://127.0.0.1:2024/mascotas', {
            method: 'POST',
            body: formData  
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('HTTP error, status = ' + response.status);
            }
            return response.text();
        })
        .then(text => {
            try {
                const data = JSON.parse(text);
                if (data.mensaje) {
                    alert('Mascota registrada exitosamente');
                    form.reset(); 
                } else {
                    throw new Error(data.error || 'Error desconocido');
                }
            } catch (e) {
                throw new Error("Invalid JSON: " + text);
            }
        })
        .catch(error => {
            alert('Error al registrar la mascota: ' + error.message);
        });
    });
});
