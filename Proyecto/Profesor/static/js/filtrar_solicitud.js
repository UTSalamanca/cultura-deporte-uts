const filtroEstado = document.getElementById("filtro_estado");
      const filtroGrupo = document.getElementById("filtro_grupo");
      const filtroNombre = document.getElementById("filtro_nombre");
      const filtroFecha = document.getElementById("filtro_fecha");
      const tablaSolicitudes = document.getElementById("tabla_solicitudes").getElementsByTagName("tbody")[0];

      // Filtrar las solicitudes
      function filtrarSolicitudes() {
        const filas = tablaSolicitudes.getElementsByTagName("tr");

        for (let i = 0; i < filas.length; i++) {
          let fila = filas[i];
          let estado = fila.cells[4].textContent;
          let grupo = fila.cells[3].textContent;
          let nombre = fila.cells[1].textContent;
          let fecha = fila.cells[5].textContent;

          let mostrar = true;

          // Filtro por estado
          if (filtroEstado.value && estado !== filtroEstado.value) {
            mostrar = false;
          }

          // Filtro por grupo
          if (filtroGrupo.value && !grupo.toLowerCase().includes(filtroGrupo.value.toLowerCase())) {
            mostrar = false;
          }

          // Filtro por nombre
          if (filtroNombre.value && !nombre.toLowerCase().includes(filtroNombre.value.toLowerCase())) {
            mostrar = false;
          }

          // Filtro por fecha
          if (filtroFecha.value && fecha !== filtroFecha.value) {
            mostrar = false;
          }

          if (mostrar) {
            fila.style.display = "";
          } else {
            fila.style.display = "none";
          }
        }
      }

      // Agregar evento de escucha para los filtros
      filtroEstado.addEventListener("change", filtrarSolicitudes);
      filtroGrupo.addEventListener("input", filtrarSolicitudes);
      filtroNombre.addEventListener("input", filtrarSolicitudes);
      filtroFecha.addEventListener("change", filtrarSolicitudes);