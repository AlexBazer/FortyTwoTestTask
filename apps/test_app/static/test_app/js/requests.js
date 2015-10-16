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

jQuery(document).ready(function($) {
    var requests = []
    var requestDataToShow = ['uri', 'method', 'remote_addr', 'user_agent']
    var renderTable = function(){
        // Rander table
        var $container = $('<table class="table table-striped">');
        var $thead = $('<thead>').html('\
        <tr>\
            <th class="h4"><strong>Timestamp</strong></th>\
            <th class="h4"><strong>Uri</strong></th>\
            <th class="h4"><strong>Method</strong></th>\
            <th class="h4"><strong>Remote Addess</strong></th>\
            <th class="h4"><strong>User Agent</strong></th>\
            <th class="h4"><strong>Viewed</strong></th>\
        </tr>\
        ');
        $container.append($thead);
        
        var $tbody = $('<tbody>');
        $.each(requests, function(index, elem) {
            var dataRuest = JSON.parse(elem.data);
            var $tr = $('<tr>');

            $tr.append($('<td>').html(elem.timestamp));
            requestDataToShow.map(function(elem, index){
                $tr.append($('<td>').html(dataRuest[elem]));
            });
            $tr.append($('<td>').html(elem.viewed?'viewed':'new'));
            $tbody.append($tr);
            // console.log(elem.viewed)
            if (!elem.viewed){
                $tr.css('font-weight','bold');
            }
        });
        $container.append($tbody);
        $('#requests-table').html($container);
        renderTitle();
    }

    var renderTitle = function(){
        // Render title - show number of new requests
        var new_els = requests.filter(function(elem, index) {return !elem.viewed});
        $('title').text('({{num_elem}}) new requests'.replace('{{num_elem}}', new_els.length));
    }

    var updateRequests = function(){
        // Get requests
        var last_timestamp = '';
        if (requests.length > 0){
            last_timestamp = requests[0].timestamp;
        }
        $.getJSON('/api/requests/', {timestamp: last_timestamp}).then(function(data){
            requests = data.concat(requests);
            renderTable();
        })
    }

    var markViewed = function(){
        // Send post rerquest to mark elements as viewd
        var viewed_els = requests.filter(function(elem, index) {return !elem.viewed});
        var viewed_ids = viewed_els.map(function(elem, index){return elem.id});
        if (viewed_els.length == 0){
            return;
        }
        
        $.post('/api/requests/',
            JSON.stringify({viewed_ids: viewed_ids}), 
            function(data, textStatus, xhr) {
                if(data.status == 'ok'){
                    // If server returned on than mark existed requests as viewed
                    viewed_els.map(function(elem, index){
                        elem.viewed = true;
                    });
                    renderTable();
                }
            });
    }
    var pollRequests = function(){
        if (document.hasFocus()){
            markViewed();
        }
        updateRequests();
        setTimeout(pollRequests, 5000);
    }
    // Start polling
    pollRequests();
});
