// ADJUST AJAX TO HANDLE CSRFTOKEN
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var markViewed;
jQuery(document).ready(function($) {
    var requests = []
    $.getJSON('/api/requests/').then(function(data){
        console.log(data);
        requests = data.concat(requests)
        renderTable();
    })
    
    var renderTable = function(){
        var $container = $('<table>');
        var $thead = $('<thead>').html('\
            <th>Timestamp</th>\
            <th>Request JSON</h>\
            <th>Viewed</th>\
        ');
        $container.append($thead);
        
        var $tbody = $('<tbody>');
        $.each(requests, function(index, val) {
            var $tr = $('<tr>');
            $tr.append($('<td>').html(val.timestamp));
            $tr.append($('<td>').html(val.data));
            $tr.append($('<td>').html(val.viewed?'viewed':'new'));
            $tbody.append($tr);
        });
        $container.append($tbody);
        $('#requests-table').html($container);
    }

    markViewed = function(){
        viewed_ids = requests.filter(function(index, elem) {return !elem.viewed}).
            map(function(elem, index){return elem.id});
        $.post('/api/requests/',
            JSON.stringify({viewed_ids: viewed_ids}), 
            function(data, textStatus, xhr) {
                console.log(data);
            }, 'json');
    }
    // var pollRequests = function(){

    //     setTimeout(pollRequests, 2000);
        
    // }
});
