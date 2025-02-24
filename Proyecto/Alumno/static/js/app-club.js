function toggleBox(boxId) {
    var box = document.getElementById(boxId);

    if (box.classList.contains('expanded')) {
        // Si el recuadro ya está expandido, lo cerramos
        box.classList.remove('expanded');
        // Ocultamos el contenido inmediatamente al cerrar
        var content = box.querySelector('.box-content');
        content.style.display = 'none';
    } else {
        // Cerrar cualquier recuadro que esté abierto
        var boxes = document.querySelectorAll('.box');
        boxes.forEach(function(otherBox) {
            otherBox.classList.remove('expanded');
            var otherContent = otherBox.querySelector('.box-content');
            otherContent.style.display = 'none'; // Ocultamos el contenido de los otros recuadros
        });

        // Expandir el recuadro seleccionado
        box.classList.add('expanded');

        // Esperamos hasta que termine la transición para mostrar el contenido
        box.addEventListener('transitionend', function() {
            if (box.classList.contains('expanded')) {
                var content = box.querySelector('.box-content');
                content.style.display = 'block'; // Mostramos el contenido solo cuando la animación ha terminado
            }
        }, { once: true });
    }
}