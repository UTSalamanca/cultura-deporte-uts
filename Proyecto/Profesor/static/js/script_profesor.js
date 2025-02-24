
// Tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})


document.addEventListener("DOMContentLoaded", function () {
    const dia = document.getElementById("dia");
    const contenedor_resultado = document.getElementById("resultado");
    const alumnos = document.getElementById('alumnos');

    function actualizarResultado() {
        const diaSeleccionado = dia.value;

        if (diaSeleccionado !== "Seleccionar día") {
            alumnos.innerHTML = '...';
            contenedor_resultado.innerHTML = `<div class="text-muted text-center">Cargando datos...</div>`;

            fetch(`?dia=${diaSeleccionado}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();  // Cambiar a .json() para respuesta JSON
                })
                .then(data => {
                    console.log('JSON recibido:', data);
                    contenedor_resultado.innerHTML = data.html;  // Inserta el HTML
                    alumnos.innerHTML = data.alumnos;           // Actualiza el contador
                })
                .catch(error => {
                    console.error('Hubo un problema con la solicitud AJAX:', error);
                    contenedor_resultado.innerHTML = `
                    <div class="alert alert-danger text-center">
                        <strong>Error:</strong> No se pudieron cargar los datos. Intenta más tarde.
                    </div>`;
                });

        } else {
            contenedor_resultado.innerHTML = `
            <div class="container d-flex flex-column justify-content-center align-items-center">
                <h4>Por favor, selecciona un día para cargar la asistencia.</h4>
                <img class="border rounded" src="{{ mapache_docente }}" width="300" alt="Docente">
            </div>`;
            alumnos.innerHTML = "---";
        }
    }

    dia.addEventListener("change", actualizarResultado);
});



document.addEventListener("DOMContentLoaded", function () {
    // Obtener la altura total de la ventana
    var windowHeight = window.innerHeight;
    console.log('altura total' + windowHeight)
    // Obtener la altura del nav
    var tamaño_nav = document.getElementById('nav').offsetHeight;
    console.log('tamaño nav:' + tamaño_nav)
    var tamaño_barra = document.getElementById('barra').offsetHeight;
    console.log('tamaño_barra:' + tamaño_barra)
    // Calcular la altura sobrante (restando la altura del nav)
    var remainingHeight = windowHeight - tamaño_nav - tamaño_barra - 18;
    console.log('calculo:' + remainingHeight)
    // Establecer la altura sobrante al div #resultado
    var resultado = document.getElementById('resultado');
    resultado.style.height = remainingHeight + 'px'; // Ajustar la altura

    console.log("Altura sobrante: " + remainingHeight + "px");
});


document.addEventListener("DOMContentLoaded", function () {
    const tabla = document.getElementById("table");

    if (tabla) {
        tabla.addEventListener("input", function (event) {
            const celda = event.target;
            if (celda.tagName === "TD") {
                celda.classList.add("modificada"); 
            }
        });
    }
});

function capturarCambios() {
    const tabla = document.querySelector("table");
    const filas = tabla.querySelectorAll("tr");
    const datos = [];

    filas.forEach((fila, index) => {
        if (index === 0) return; // Omitir encabezado
        const celdas = fila.querySelectorAll("td");
        const filaData = {
            matricula: celdas[0].innerText,
            nombre: celdas[1].innerText,
            carrera: celdas[2].innerText,
            grado: celdas[3].innerText,
            grupo: celdas[4].innerText,
            horas: celdas[5].innerText,
            estatus: celdas[6].innerText,
            seguimiento: celdas[7].innerText,
            modificada: Array.from(celdas).some(celda => celda.classList.contains("modificada"))
        };
        datos.push(filaData);
    });

    return datos;
}


function guardarCambios() {
    const datos = capturarCambios().filter(fila => fila.modificada); // Solo filas modificadas
    const dia = document.getElementById("dia").value;

    if (datos.length === 0) {
        alert("No hay cambios para guardar.");
        return;
    }

    fetch("/profesor/guardar_cambios/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            dia: dia,
            alumnos: datos,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            alert("Datos guardados correctamente.");
            // Limpia las marcas de celdas modificadas
            document.querySelectorAll("td.modificada").forEach(celda => celda.classList.remove("modificada"));
        })
        .catch((error) => {
            console.error("Error al guardar los datos:", error);
        });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
