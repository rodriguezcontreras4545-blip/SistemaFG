document.addEventListener("DOMContentLoaded", function() {
    const productoSelect = document.getElementById("id_producto");
    if (!productoSelect) return;

    // Buscar directamente los inputs por su ID nativo de Django
    const inputGeneracion = document.getElementById("id_generacion");
    const inputProcesador = document.getElementById("id_procesador");
    const inputVelocidad = document.getElementById("id_velocidad");

    // Encontrar el contenedor Bootstrap (.form-group) de cada uno
    const contenedorGeneracion = inputGeneracion ? inputGeneracion.closest('.form-group') : null;
    const contenedorProcesador = inputProcesador ? inputProcesador.closest('.form-group') : null;
    const contenedorVelocidad = inputVelocidad ? inputVelocidad.closest('.form-group') : null;

    function verificarProducto() {
        const valor = productoSelect.value;

        if (valor === "MONITOR") {
            // Ocultar usando la clase nativa de Bootstrap que maneja Jazzmin
            if (contenedorGeneracion) contenedorGeneracion.classList.add('d-none');
            if (contenedorProcesador) contenedorProcesador.classList.add('d-none');
            if (contenedorVelocidad)  contenedorVelocidad.classList.add('d-none');
        } else {
            // Mostrar para LAPTOP, CPU y AIO
            if (contenedorGeneracion) contenedorGeneracion.classList.remove('d-none');
            if (contenedorProcesador) contenedorProcesador.classList.remove('d-none');
            if (contenedorVelocidad)  contenedorVelocidad.classList.remove('d-none');
        }
    }

    // Escuchar cambios del operador y ejecutar inmediatamente al cargar
    productoSelect.addEventListener("change", verificarProducto);
    verificarProducto();
});