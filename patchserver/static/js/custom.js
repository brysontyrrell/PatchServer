/**
 * Created by brysontyrrell on 8/1/17.
 */

function compare(a,b) {
	if (a.id < b.id)
		return -1;
	if (a.id > b.id)
		return 1;
	return 0;
}


function ConvertFormToJSON(form){
    var array = jQuery(form).serializeArray();
    var json = {};

    jQuery.each(array, function() {
        json[this.name] = this.value || '';
    });

    return json;
}


// https://gist.github.com/kmaida/6045266
function ConvertTimestamp(timestamp) {
  var d = new Date(timestamp * 1000),	// Convert the passed timestamp to milliseconds
		yyyy = d.getFullYear(),
		mm = ('0' + (d.getMonth() + 1)).slice(-2),	// Months are zero based. Add leading 0.
		dd = ('0' + d.getDate()).slice(-2),			// Add leading 0.
		hh = d.getHours(),
		h = hh,
		min = ('0' + d.getMinutes()).slice(-2),		// Add leading 0.
		ampm = 'AM',
		time;

	if (hh > 12) {
		h = hh - 12;
		ampm = 'PM';
	} else if (hh === 12) {
		h = 12;
		ampm = 'PM';
	} else if (hh === 0) {
		h = 12;
	}

	// ie: 2013-02-18, 8:35 AM
	time = yyyy + '-' + mm + '-' + dd + ' ' + h + ':' + min + ' ' + ampm;

	return time;
}


/**
 * Functions for index.html
 */
function listSoftwareTitles() {

    $('#patch-list').DataTable({
        "paging": false,
        "searching": false,
        "bInfo": false,
        "language": {
            "zeroRecords": "No Patch Definitions Found"
        },
        "ajax": {
            "url": "jamf/v1/software",
            "dataSrc": ""
        },
        "columnDefs": [
            { "targets": 0, "data": "id" },
            {
                "targets": 1,
                "orderable": false,
                "data": "id",
                "render": function ( data, type, row, meta ) {
                    return '<button class="btn btn-info btn-xs" onclick="window.location.href=\'../jamf/v1/patch/' + data + '\'">' +
                           '<span class="glyphicon glyphicon-eye-open"></span></button>';
                }
            },
            { "targets": 2, "orderable": false, "data": "name" },
            { "targets": 3, "data": "publisher" },
            { "targets": 4, "data": "currentVersion" },
            {
                "targets": 5,
                "orderable": false,
                "data": "id",
                "render": function ( data, type, row, meta ) {
                    return '<button id="' + data + '" class="btn btn-success btn-xs" onclick="">' +
						    '<span class="glyphicon glyphicon-chevron-up"></span></button>';
                }
            },
            { "targets": 6, "data": "lastModified" },
            {
                "targets": 7,
                "orderable": false,
                "data": "id",
                "render": function ( data, type, row, meta ) {
                    return '<button id="' + data + '" class="btn btn-danger btn-xs" onclick="indexDeletePatch(this.id)">' +
						    '<span class="glyphicon glyphicon-remove"></span></button>';
                }
            }
        ]
    });

}

function listWebhooks() {

	$('#webhook-list').DataTable({
        "paging": false,
        "searching": false,
        "bInfo": false,
        "language": {
            "zeroRecords": "No Webhooks Have Been Configured"
        },
        "ajax": {
            "url": "api/v1/webhooks",
            "dataSrc": ""
        },
        "columnDefs": [
            { "targets": 0, "data": "url" },
            { "targets": 1, "orderable": false, "data": "verify_ssl" },
            { "targets": 2, "orderable": false, "data": "send_definition" },
            { "targets": 3, "data": "enabled" },
            {
                "targets": 4,
                "orderable": false,
                "data": "id",
                "render": function ( data, type, row, meta ) {
                    return '<button id="' + data + '" class="btn btn-danger btn-xs" onclick="indexDeleteWebhook(this.id)">' +
						    '<span class="glyphicon glyphicon-remove"></span></button>';
                }
            }
        ]
    });

}


//function indexAddPatch() {
//	var registerForm = $('#addPatchForm');
//
//	registerForm.on('submit', function (event) {
//		//stop submit the form, we will post it manually.
//		event.preventDefault();
//		var jsonData = ConvertFormToJSON(registerForm);
//		$("#addPatchFormSubmit").prop("disabled", true);
//
//		$.ajax({
//			type: "POST",
//			url: "../api/v1/title",
//			dataType: 'json',
//			contentType: "application/json",
//			data: JSON.stringify(jsonData),
//			cache: false,
//			success: function (data) {
//				console.log("SUCCESS: ", data);
//				window.location.href = '../';
//			},
//			error: function (e) {
//				console.log("ERROR: ", e);
//				console.log("ERROR MSG: ", e.responseText);
//				window.location.href = '../';
//			}
//		});
//	});
//}


function indexDeletePatch(name_id) {
    $.ajax({
        type: 'DELETE',
        url: "../api/v1/title/" + name_id + '?redirect=true',
        cache: false,
        success: function (data) {
            window.location.href = '../';
        },
        error: function (e) {
            console.log("ERROR: ", e);
            console.log("ERROR MSG: ", e.responseText);
            window.location.href = '../';
        }
    });
}

function indexDeleteWebhook(id) {
    $.ajax({
        type: 'DELETE',
        url: "../api/v1/webhooks/" + id + '?redirect=true',
        cache: false,
        success: function (data) {
            console.log('SUCCESS');
            window.location.href = '../';
        },
        error: function (e) {
            console.log("ERROR: ", e);
            console.log("ERROR MSG: ", e.responseText);
            window.location.href = '../';
        }
    });
}