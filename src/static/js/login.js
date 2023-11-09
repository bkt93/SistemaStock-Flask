'use strict';

$(function() {

	// author badge :)
	

	$("input[type='password'][data-eye]").each(function(i) {
		var $this = $(this),
			id = 'eye-password-' + i,
			el = $('#' + id);

		$this.wrap($("<div/>", {
			style: 'position:relative',
			id: id
		}));

		$this.css({
			paddingRight: 60
		});
		$this.after($("<div/>", {
			html: 'Show',
			class: 'btn btn-primary btn-sm',
			id: 'passeye-toggle-'+i,
		}).css({
				position: 'absolute',
				right: 10,
				top: ($this.outerHeight() / 2) - 12,
				padding: '2px 7px',
				fontSize: 12,
				cursor: 'pointer',
		}));

		$this.after($("<input/>", {
			type: 'hidden',
			id: 'passeye-' + i
		}));

		var invalid_feedback = $this.parent().parent().find('.invalid-feedback');

		if(invalid_feedback.length) {
			$this.after(invalid_feedback.clone());
		}

		$this.on("keyup paste", function() {
			$("#passeye-"+i).val($(this).val());
		});
		$("#passeye-toggle-"+i).on("click", function() {
			if($this.hasClass("show")) {
				$this.attr('type', 'password');
				$this.removeClass("show");
				$(this).removeClass("btn-outline-primary");
			}else{
				$this.attr('type', 'text');
				$this.val($("#passeye-"+i).val());				
				$this.addClass("show");
				$(this).addClass("btn-outline-primary");
			}
		});
	});

	$(".my-login-validation").submit(function() {
		var form = $(this);
        if (form[0].checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
		form.addClass('was-validated');
	});
});


// Alertas!
// Cerrar la alerta al hacer clic en la "x"
document.querySelector('.btn-close').addEventListener('click', function () {
	document.querySelector('.alert').style.transition = 'opacity 0.5s'; // Agrega una transición
	document.querySelector('.alert').style.opacity = '0'; // Hace que la alerta se desvanezca
	setTimeout(function() {
		document.querySelector('.alert').remove(); // Elimina la alerta después de la transición
	}, 500); // 500 milisegundos = 0.5 segundos
});

// Cerrar automáticamente después de 3 segundos
setTimeout(function() {
	document.querySelector('.alert').style.transition = 'opacity 0.5s'; // Agrega una transición
	document.querySelector('.alert').style.opacity = '0'; // Hace que la alerta se desvanezca
	setTimeout(function() {
		document.querySelector('.alert').remove(); // Elimina la alerta después de la transición
	}, 500); // 500 milisegundos = 0.5 segundos
}, 3000); // 3000 milisegundos = 3 segundos