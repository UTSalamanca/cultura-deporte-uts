// Variables globales
let totalPuntos = 105;
let puntosObtenidos = 0;

// Mostrar/Ocultar el menú desplegable
function toggleDropdown() {
  const dropdown = document.getElementById("dropdown-content");
  dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

// Filtrar cuatrimestre
function filtrarCuatrimestre() {
  const cuatrimestres = document.querySelectorAll(".semana");
  const seleccionCuatrimestre = document.querySelector('input[name="cuatrimestre"]:checked').value;

  // Ocultar todas las semanas inicialmente
  cuatrimestres.forEach(semana => {
    semana.style.display = "none";
  });

  // Mostrar semanas del cuatrimestre seleccionado
  const semanasSeleccionadas = document.querySelectorAll(`.cuatrimestre-${seleccionCuatrimestre}`);
  semanasSeleccionadas.forEach(semana => {
    semana.style.display = "flex";
  });

  calcularPuntos();
  closeDropdown();
}

// Calcular puntos obtenidos
function calcularPuntos() {
  puntosObtenidos = 0;
  const semanasVisibles = document.querySelectorAll(".semana[style*='flex']");

  semanasVisibles.forEach(semana => {
    puntosObtenidos += parseInt(semana.getAttribute("data-puntos"), 10);
  });

  document.getElementById("indicador-puntos").textContent = `${puntosObtenidos}/${totalPuntos}`;
}

// Cerrar el menú desplegable
function closeDropdown() {
  const dropdown = document.getElementById("dropdown-content");
  dropdown.style.display = "none";
}

// Inicialización al cargar
window.onload = calcularPuntos;