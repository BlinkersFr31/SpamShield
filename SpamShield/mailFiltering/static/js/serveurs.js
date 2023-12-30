$(document).ready(function(){
	new DataTable('#serveursTable');
});

function showServeur(id) {
	window.open("/mailFiltering/"+id, _self)
}