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
});
$(function () {
});

