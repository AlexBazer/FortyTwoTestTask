$(document).ready(function() { 
    // bind 'myForm' and provide a simple callback function 
    var options = {
        dataType: 'json',
        beforeSubmit:  function(formData, $form, options){
            $form.css('position', 'relative');
            $cover = $('<span class="cover">').css({
                position: 'absolute',
                top:0,
                left:0,
                right:0,
                bottom:0,
                'background-color':'white',
                opacity: 0.6
            })
            $cover.append('<span class="spinner">');
            $form.append($cover);
        },
        success: function(data, statusText, xhr, $form){
            $('#id_photo ~ .thumbnail img').attr('src', data.fields.photo);
            // Remove cover
            $form.find('.cover').remove();
            // Create success message
            $message = $('<span class="text-success">').text('Changes have been saved');
            // Append congradulation
            $form.find('hr').before($message);
            // Hide and delet it
            $message.fadeOut(5000, function() {
                $message.remove();
            });
        },
        error: function(data, statusText, xhr, $form){
            $form.find('.cover').remove();
            // Create success message
            $message = $('<span class="text-danger">').text(statusText);
            // Append congradulation
            $form.find('hr').before($message);
            // Hide and delet it
            $message.fadeOut(5000, function() {
                $message.remove();
            });

        }

    }
    $('#edit-user-form').ajaxForm(options); 
}); 