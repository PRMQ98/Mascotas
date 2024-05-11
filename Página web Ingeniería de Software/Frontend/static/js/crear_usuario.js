document.getElementById('crearUsuarioForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene el envío normal del formulario

    const dpi = document.getElementById('dpi').value;

    // Validar que DPI contiene sólo números y tiene una longitud de hasta 13 caracteres
    if (!/^\d{1,13}$/.test(dpi)) {
        alert('El DPI debe contener solo números y no más de 13 dígitos.');
        return; // Detiene la función si la validación falla
    }

    // Recoge los valores del formulario
    const usuarioData = {
        nombres: document.getElementById('nombres').value,
        apellidos: document.getElementById('apellidos').value,
        dpi: dpi,
        direccion: document.getElementById('direccion').value,
        numeroTelefono: document.getElementById('numeroTelefono').value,
        correoElectronico: document.getElementById('correoElectronico').value,
    };

    // Llamada fetch para crear el usuario
    fetch('http://localhost:2024/crear_usuario', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(usuarioData),
    })
    .then(response => response.json())
    .then(data => alert('Usuario creado exitosamente'))
    .catch((error) => {
        console.error('Error:', error);
        alert('Error al crear el usuario');
    });
});
