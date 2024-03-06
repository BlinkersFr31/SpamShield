$(document).ready(function(){
	new DataTable('#messagesTable');
});

function checkAllMsgs() {
	$( "input[name='messagesChck']" ).prop('checked',$("#checkAllMsgs").prop('checked'));
}

function showMessageForServeur() {
	window.open("/mailFiltering/" + $( "select[name='serveur']" ).val(), "_self");
}

function actionForServeur() {
	var actionVal = $("#action")[0].value;
	var messagesChckVal = $( "input[name='messagesChck']:checked");
	var serveurId = $( "select[name='serveur']" ).val();
	var urlAjx = '/mailFiltering/gestionMails/' + serveurId;
	var jsonVal = JSON.stringify({ action: actionVal, mailsUID: messagesChckVal, domains: "" });
	$.ajax({
		type: 'POST',
		url: urlAjx,
		data: jsonVal,
		success: function(data) { alert('data: ' + data); },
		contentType: "application/json",
		dataType: 'json'
	});
}
