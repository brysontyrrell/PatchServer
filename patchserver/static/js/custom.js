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
	$.ajax(
	{
		type: "GET",
		url: '../jamf/v1/software',
		dataType: "json",
		cache: false,
		success: function (data) {
			data.sort(compare);
			if (data.length > 0) {
				$.each(data, function (i, item) {
					var date = new Date(item.lastModified);
					var options = {
						weekday: "long", year: "numeric", month: "short",
						day: "numeric", hour: "2-digit", minute: "2-digit"
					};
					var table_row = '<tr>' +
						'<td>' + item.id + '</td>' +
						'<td>' + item.name + '</td>' +
						'<td>' + item.publisher + '</td>' +
						'<td>' + item.currentVersion + '</td>' +
						'<td>' + date.toLocaleString('en-us', options) + '</td>' +
						'<td>' +
						'    <button class="btn-info btn-xs" onclick="window.location.href=\'../jamf/v1/patch/' + item.id + '\'">' +
						'        <span class="glyphicon glyphicon-eye-open"></span>' +
						'    </button>' +
						'</td>' +
                        '<td>' +
						'    <button id="' + item.id + '" class="btn-danger btn-xs" onclick="indexDeletePatch(this.id)">' +
						'        <span class="glyphicon glyphicon-remove"></span>' +
						'    </button>' +
                        '</td>' +
						'</tr>';
					$('#patch-list > tbody:last-child').append(table_row);
				});
			} else {
				var table_row =
					'<tr><td colspan="7">' +
					'<h3 style="text-align: center; font-style: italic;">No Patch Definitions Found</h3>' +
					'</td></tr>';
				$('#patch-list > tbody:last-child').append(table_row);
			}
		},

		error: function (msg) {
			alert(msg.responseText);
		}
	});
}

function listWebhooks() {
	$.ajax(
	{
		type: "GET",
		url: '../api/v1/webhooks',
		dataType: "json",
		cache: false,
		success: function (data) {
			if (data.length > 0) {
				$.each(data, function (i, item) {
					var table_row = '<tr>' +
						'<td>' + item.enabled + '</td>' +
						'<td>' + item.send_definition + '</td>' +
						'<td>' + item.url + '</td>' +
						'<td>' +
						'    <button class="btn-info btn-xs" onclick="window.location.href=\'../api/v1/webhooks/' + item.id + '\'">' +
						'        <span class="glyphicon glyphicon-eye-open"></span>' +
						'    </button>' +
						'</td>' +
                        '<td>' +
						'    <button id="' + item.id + '" class="btn-danger btn-xs" onclick="indexDeleteWebhook(this.id)">' +
						'        <span class="glyphicon glyphicon-remove"></span>' +
						'    </button>' +
                        '</td>' +
						'</tr>';
					$('#webhook-list > tbody:last-child').append(table_row);
				});
			} else {
				var table_row =
					'<tr><td colspan="7">' +
					'<h3 style="text-align: center; font-style: italic;">No Webhooks Have Been Configured</h3>' +
					'</td></tr>';
				$('#webhook-list > tbody:last-child').append(table_row);
			}
		},

		error: function (msg) {
			alert(msg.responseText);
		}
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