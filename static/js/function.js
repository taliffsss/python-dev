(function() {
	'use strict';
	window.addEventListener('load', function() {
		var form = document.getElementById('needs-validation');
		form.addEventListener('submit', function(event) {
			if (form.checkValidity() === false) {
				event.preventDefault();
				event.stopPropagation();
			}
			form.classList.add('was-validated');
		}, false);
	}, false);
})();

$("#btnLogin").click(function(event) {

	//Fetch form to apply custom Bootstrap validation
	var form = $("#formLogin")
	if (form[0].checkValidity() === false) {
		event.preventDefault()
		event.stopPropagation()
	}
	form.addClass('was-validated');
});

$(function () {
	$('[data-toggle="tooltip"]').tooltip()
})