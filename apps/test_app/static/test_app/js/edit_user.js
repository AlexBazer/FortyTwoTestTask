$(document).ready(function() { 
    // bind 'myForm' and provide a simple callback function 
    var options = {
        dataType: 'json',
        success: function(responseText, statusText, xhr, $form){
            console.log(responseText);
        }
    }
    $('#edit-user-form').ajaxForm(options); 
}); 