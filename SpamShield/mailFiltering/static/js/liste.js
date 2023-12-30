$(document).ready(function(){
	new DataTable('#messagesTable');
});

function checkAllMsgs() {
	$( "input[name='messagesChck']" ).prop('checked',$("#checkAllMsgs").prop('checked'));
}

function showMessageForServeur() {
	window.open("/mailFiltering/" + $( "select[name='serveur']" ).val(), "_self");
}