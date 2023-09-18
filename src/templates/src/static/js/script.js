
/* Motor de búsqueda */

document.getElementById("search-input").addEventListener("input", function() {
    performSearch();
});

function performSearch() {
    var searchText = document.getElementById("search-input").value.toLowerCase();
    var table = document.getElementById("table-inventario");
    var rows = table.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var rowVisible = false;

        /* Convertimos toda la búsqueda a minúscula */
        for (var j = 0; j < cells.length; j++) {
            var cellText = cells[j].textContent.toLowerCase();

            /* Quita la columna acciones para que no se 
            consideren los enlaces "Editar" y eliminar */
            if (j !== cells.length - 1) {
                if (cellText.includes(searchText)) {
                    rowVisible = true;
                    break;
                }
            }
        }

        if (i === 0) {
            // Mostramos siempre el encabezado
            rows[i].style.display = "";
        } else {
            // Ocultar o mostrar filas de datos según la búsqueda
            rows[i].style.display = searchText === "" || rowVisible ? "" : "none";
        }
    }
}
