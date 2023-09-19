
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


// Animación de flash messages
setTimeout(function () {
    var flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        flashMessages.classList.add('fade-out');
        setTimeout(function () {
            flashMessages.remove();
        }, 500); 
    }
}, 2000); 


// Confirmación delete
function ConfirmDelete() {
    var respuesta = confirm("Deseas eliminar este elemento?");
    if (respuesta == true) {
        return true;
    } else {
        return false;
    }
}


document.addEventListener("DOMContentLoaded", function () {
    const guardarButton = document.getElementById("guardar-button");

    // Escucha el evento keydown en el botón de "Guardar"
    guardarButton.addEventListener("keydown", function (event) {
      // Verifica si la tecla presionada es "Enter" (código 13)
      if (event.keyCode === 13) {
        // Activa el evento de clic en el botón de "Guardar"
        guardarButton.click();
      }
    });
  });

  
 
