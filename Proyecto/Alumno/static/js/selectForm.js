document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM completamente cargado");  // Asegura que el DOM está listo

    const selectClub = document.getElementById('id_club');
    const selectHorario = document.getElementById('id_horario_club');
    const selectDia = document.getElementById('id_dia');

    // Verificamos si los elementos existen en el DOM
    if (selectClub && selectHorario && selectDia) {
        console.log("Elementos encontrados:", selectClub, selectHorario, selectDia);  // Verifica que los elementos existan

        // Filtrar horarios según el club seleccionado
        selectClub.addEventListener('change', function() {
            const clubId = selectClub.value;
            console.log("Club seleccionado:", clubId);  // Imprime el ID del club seleccionado
            
            if (clubId) {
                fetch(`/alumno/filtrar_horarios/${clubId}/`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("Horarios recibidos:", data.horarios);  // Imprime los horarios recibidos

                        // Limpiar opciones de horario y día
                        selectHorario.innerHTML = '<option value="">Seleccione un horario</option>';
                        selectDia.innerHTML = '<option value="">Seleccione un día</option>';

                        // Rellenar opciones de horarios
                        data.horarios.forEach(horario => {
                            const option = document.createElement('option');
                            option.value = horario.id;
                            option.textContent = `${horario.hora_inicio} - ${horario.hora_final}`;
                            selectHorario.appendChild(option);
                        });
                    })
                    .catch(error => console.error("Error al obtener horarios:", error));  // Imprime error si no se puede obtener los horarios
            } else {
                console.log("No se seleccionó ningún club");  // Si no se selecciona ningún club
            }
        });

        // Filtrar días según el horario seleccionado
        selectHorario.addEventListener('change', function() {
            const horarioId = selectHorario.value;
            console.log("Horario seleccionado:", horarioId);  // Imprime el ID del horario seleccionado

            if (horarioId) {
                fetch(`/alumno/filtrar_dias/${horarioId}/`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("Días recibidos:", data.dias);  // Imprime los días recibidos

                        // Limpiar opciones de día
                        selectDia.innerHTML = '<option value="">Seleccione un día</option>';

                        // Rellenar opciones de días
                        data.dias.forEach(dia => {
                            const option = document.createElement('option');
                            option.value = dia.id;
                            option.textContent = dia.dia;
                            selectDia.appendChild(option);
                        });
                    })
                    .catch(error => console.error("Error al obtener días:", error));  // Imprime error si no se puede obtener los días
            } else {
                console.log("No se seleccionó ningún horario");  // Si no se selecciona ningún horario
            }
        });

    } else {
        console.error("Uno o más elementos no existen en el DOM: 'id_club', 'id_horario_club', o 'id_dia'.");
    }
});
