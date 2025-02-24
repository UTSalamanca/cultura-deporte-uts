// Obtener elementos
const cloud = document.getElementById("cloud");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span");
const cambiar = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");

// Verificar estado de la barra lateral desde localStorage
const barraEstado = localStorage.getItem('barraEstado'); // "minimizado" o "maximizado"
const sidebarEstado = localStorage.getItem('sidebarEstado'); // "abierto" o "cerrado"

// Aplicar el estado guardado al cargar la página
if (barraEstado === 'minimizado') {
    barraLateral.classList.add('mini-barra-lateral');
    spans.forEach((span) => span.classList.add('oculto'));
} else if (barraEstado === 'maximizado') {
    barraLateral.classList.remove('mini-barra-lateral');
    spans.forEach((span) => span.classList.remove('oculto'));
}

if (sidebarEstado === 'abierto') {
    barraLateral.classList.add('max-barra-lateral');
    menu.children[0].style.display = "none";
    menu.children[1].style.display = "block";
} else if (sidebarEstado === 'cerrado') {
    barraLateral.classList.remove('max-barra-lateral');
    menu.children[0].style.display = "block";
    menu.children[1].style.display = "none";
}

// Manejar el clic en el menú para abrir/cerrar la barra lateral
menu.addEventListener("click", () => {
    barraLateral.classList.toggle("max-barra-lateral");
    if (barraLateral.classList.contains("max-barra-lateral")) {
        menu.children[0].style.display = "none";
        menu.children[1].style.display = "block";
        localStorage.setItem('sidebarEstado', 'abierto'); // Guardar estado como abierto
    } else {
        menu.children[0].style.display = "block";
        menu.children[1].style.display = "none";
        localStorage.setItem('sidebarEstado', 'cerrado'); // Guardar estado como cerrado
    }
});

// Manejar el cambio de modo oscuro
cambiar.addEventListener("click", () => {
    let body = document.body;
    body.classList.toggle("dark-mode");
    circulo.classList.toggle("prendido");
});

// Manejar el clic en el ícono de la nube para minimizar/maximizar la barra lateral
cloud.addEventListener("click", () => {
    barraLateral.classList.toggle("mini-barra-lateral");
    spans.forEach((span) => {
        span.classList.toggle("oculto");
    });
    // Guardar estado de la barra lateral (mini o maximizada)
    if (barraLateral.classList.contains("mini-barra-lateral")) {
        localStorage.setItem('barraEstado', 'minimizado');
    } else {
        localStorage.setItem('barraEstado', 'maximizado');
    }
});
